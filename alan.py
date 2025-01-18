from dotenv import load_dotenv
from flask import abort, Flask, request
from flask_socketio import emit, SocketIO
from werkzeug.utils import secure_filename
import os
import boto3
from uuid import uuid4
import random
import mysql.connector

load_dotenv()

UPLOAD_FOLDER = ""
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
s3 = boto3.resource("s3")

mydb = mysql.connector.connect(
  host="localhost",
  user="alanbui",
  password="uofthacks12!",
  database="users"
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
            "id": random.randint(0, 1000000000) #change so no collision
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
    big_image_url = result[0][2]

    return {
        "album_images": image_urls,
        "big_image": big_image_url
    }

socketio = SocketIO(app)

if __name__ == "__main__":
    socketio.run(app, port=5001)