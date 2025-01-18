import os
from uuid import uuid4

import boto3
from dotenv import load_dotenv
from flask import abort, Flask, request
from flask_socketio import SocketIO
from supabase import create_client
from werkzeug.utils import secure_filename

load_dotenv()

UPLOAD_FOLDER = ""
ALLOWED_EXTENSIONS = {"png", "jpg"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

s3 = boto3.resource("s3")
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_API_KEY"))

def valid_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.post("/api/upload-images")
def upload_images():
    """POST endpoint that uploads the given images to the S3 bucket and Supabase database."""
    
    if "images" not in request.files or "category" not in request.form:
        abort(400)
    
    images = request.files.getlist("images")
    category = request.form["category"]
    rows = []

    for _, image in enumerate(images):
        filename = secure_filename(image.filename)

        # if not valid_image(filename):
        #     continue

        extension = filename.rsplit('.', 1)[1].lower()
        stored_filename = f"{uuid4()}.{extension}" # for S3, to ensure unique filename

        s3.Bucket(os.getenv("S3_BUCKET_NAME")).put_object(Key=stored_filename, Body=image)

        rows.append({
            "url": os.getenv("S3_BUCKET_BASE_URL") + stored_filename,
            "grayscale": 0,
            "category": category
        })
    
    # Add images to database
    supabase.table("images").insert(rows).execute()

    socketio.emit(f"add image {category}", {
        "images": [row["url"] for row in rows]
    })
    
    return {"success": True}

@app.get("/api/get-images")
def get_images():
    if "category" not in request.args:
        abort(400)
    
    category_id = int(request.args["category"])
    
    images_data = supabase.table("images").select("url").eq("category", category_id).order("id", desc=False).execute().data
    image_urls = [image.url for image in images_data]

    big_image_url = supabase.table("categories").select("desired_image_url").eq("id", category_id).execute().data[0]["desired_image_url"]
    
    return {
        "album_images": image_urls,
        "big_image": big_image_url
    }

@app.delete("/api/delete-images")
def delete_images():
    if "urls" not in request.json:
        abort(400)
    
    supabase.table("images").delete().in_("url", request.json["urls"]).execute()

    return {"success": True}

socketio = SocketIO(app)

if __name__ == "__main__":
    socketio.run(app, port=5001)