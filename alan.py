from dotenv import load_dotenv
from flask import abort, Flask, request
from flask_cors import CORS, cross_origin
from flask_socketio import emit, SocketIO
from werkzeug.utils import secure_filename
import os
import boto3
from uuid import uuid4
import random
import requests
import mysql.connector
import openai

load_dotenv()

UPLOAD_FOLDER = ""
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)
cors = CORS(app)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
s3 = boto3.resource("s3")

openai.api_key = os.getenv('OPENAI_KEY')

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="alanbui",
#   password="uofthacks12!",
#   database="users"
# )

mydb = mysql.connector.connect(
  host=os.getenv('HOST'),
  user=os.getenv('USER'),
  password=os.getenv('PASSWORD'),
  database=os.getenv('DATABASE'),
  port=os.getenv('PORT')
)

mycursor = mydb.cursor()

def valid_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.post("/api/upload-images")
def upload_images():
    """POST endpoint that uploads the given images to the S3 bucket and SQL database."""
    
    if "images" not in request.files or "category" not in request.form:
        abort(400)
    
    images = request.files.getlist("images")
    category = request.form["category"]
    rows = []
    for _, image in enumerate(images):
        filename = secure_filename(image.filename)

        if not valid_image(filename):
            continue

        extension = filename.rsplit('.', 1)[1].lower()
        stored_filename = f"{uuid4()}.{extension}" # for S3, to ensure unique filename

        s3.Bucket(os.getenv("S3_BUCKET_NAME")).put_object(Key=stored_filename, Body=image)

        rows.append({
            "url": os.getenv("S3_BUCKET_BASE_URL") + stored_filename,
            # "url": stored_filename,
            "category": category,
            "id": random.randint(0, 2000000000) #change so no collision
        })

    
    # Add images to database
    for row in rows:
        sql = "INSERT INTO images (id, url, category) VALUES (%s, %s, %s)"
        val = (row['id'], row['url'],row['category'] )
        mycursor.execute(sql, val)

    mydb.commit()

    socketio.emit(f"add image {category}", {
        "images": [row["url"] for row in rows]
    })
    
    return {"success": True}

@app.post("/api/get-images")
def get_images():
    if "category" not in request.form:
        abort(400)
    
    category_id = int(request.form["category"])

    mycursor.execute(f"SELECT * FROM images WHERE category={category_id}")
    result = mycursor.fetchall()

    URL = 1
    image_urls = [image[URL] for image in result]

    mycursor.execute(f"SELECT * FROM categories WHERE id={category_id}")
    result = mycursor.fetchall()
    
    try:
        big_image_url = result[0][2]
        
    except:
        big_image_url = "https://upload.wikimedia.org/wikipedia/commons/4/49/A_black_image.jpg"

    return {
        "album_images": image_urls,
        "big_image": big_image_url
    }

@app.post("/api/create-category")
def create_category():
    if "user" not in request.form:
        abort(400)

    user = request.form["user"]
    if "image_name" in request.form:
        image_name = request.form["image_name"]
    
    category_id = random.randint(0, 2000000000)

    sql = "INSERT INTO categories (id, image_name, url, user) VALUES (%s, %s, %s, %s)"
    val = (category_id, "New Image", "", user)
    mycursor.execute(sql, val)

    # mydb.commit()
    
    return {"success": True, "id": category_id}


@app.post("/api/delete-image")
def delete_image():
    if "url" not in request.form or 'category' not in request.form:
        abort(400)

    image_url = request.form['url']
    category = request.form['category']

    sql = f"DELETE FROM images WHERE url='{image_url}'"
    mycursor.execute(sql)

    mydb.commit()
    print(f"delete image ${category}")
    socketio.emit(f"delete image {category}", {
        "url": image_url
    })
    
    return {"success": True}

@app.post("/api/get-mosaics")
def get_mosaics():
    if "user" not in request.form:
        abort(400)

    userid = request.form['user']

    sql = f"SELECT * FROM categories WHERE user='{userid}'"
    # val = (userid,)

    mycursor.execute(sql)
    # print(sql)
    result = mycursor.fetchall()

    ID = 0 #potentially wrong
    IMAGE_NAMES = 1
    URL = 2
    
    ids = [i[ID] for i in result]
    image_names = [i[IMAGE_NAMES] for i in result]
    urls = [i[URL] for i in result]

    return {
        "ids": ids,
        "image_names": image_names,
        "urls": urls
    }

@app.post('/api/generate-dalle')
def generate_dalle():
    category_id = request.form["category_id"]
    if "prompt" in request.form and request.form["prompt"] != "":
        user_prompt = request.form["prompt"]
        
        response = openai.Image.create(
            prompt=user_prompt,
            n=1,  # Number of images to generate
            size="1024x1024"  # Image size (can be "256x256", "512x512", or "1024x1024")
        )

        url = response['data'][0]['url']

        res = requests.get(url, stream=True)
        data = res.raw.read()

        stored_filename = f"{uuid4()}.png" # for S3, to ensure unique filename

        s3.Bucket(os.getenv("S3_BUCKET_NAME")).put_object(Key=stored_filename, Body=data)

        s3_url = os.getenv("S3_BUCKET_BASE_URL") + stored_filename

        sql = f"UPDATE categories SET url = '{s3_url}' WHERE id = '{category_id}'"

        # sql = f"UPDATE categories SET url = '{url}' WHERE id = '{category_id}'"

        mycursor.execute(sql)

        mydb.commit()

        return {"url": s3_url}

    return {"url": ""}

@app.post('/api/upload_big_image')
def upload_big():
    if "category_id" in request.form and "file" in request.files:
        category_id = request.form["category_id"]
        file = request.files.getlist('file')[0]

        extension = file.filename.rsplit('.', 1)[1].lower()
        stored_filename = f"{uuid4()}.{extension}" # for S3, to ensure unique filename

        s3.Bucket(os.getenv("S3_BUCKET_NAME")).put_object(Key=stored_filename, Body=file)

        url = os.getenv("S3_BUCKET_BASE_URL") + stored_filename

        sql = f"UPDATE categories SET url = '{url}' WHERE id = '{category_id}'"

        mycursor.execute(sql)
        mydb.commit()
        
        return {"url": url}
    
    return {"url": ""}

socketio = SocketIO(app, cors_allowed_origins=["http://localhost:5173", "http://localhost:5174"])

if __name__ == "__main__":
    print("RUNNING")
    socketio.run(app, port=5001,allow_unsafe_werkzeug=True)