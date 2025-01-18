import boto3
import cv2
from dotenv import load_dotenv
from flask import abort, Flask, request
from math import sqrt
import os
import requests
import shutil
from supabase import create_client
from uuid import uuid4
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

        if not valid_image(filename):
            continue

        extension = filename.rsplit('.', 1)[1].lower()
        stored_filename = f"{uuid4()}.{extension}" # for S3, to ensure unique filename

        file_path = os.path.join(app.config["UPLOAD_FOLDER"], stored_filename)

        s3.Bucket(os.getenv("S3_BUCKET_NAME")).put_object(Key=stored_filename, Body=image)

        # Save image locally temporarily (to open with OpenCV)
        image.save(file_path)

        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        mean = cv2.mean(img)[0] # The mean grayscale value of this image
        rows.append({
            "url": os.getenv("S3_BUCKET_BASE_URL") + stored_filename,
            "grayscale": mean,
            "category": category
        })

        # Delete temp file
        os.unlink(file_path)
    
    # Add images to database
    supabase.table("images").insert(rows).execute()
    
    return {"success": True}

@app.get("/api/get-images")
def get_images():
    if "category" not in request.args:
        abort(400)
    
    category_id = int(request.args["category"])
    
    sb_data = supabase.table("images").select("grayscale, url").eq("category", category_id).order("id", desc=False).execute().data
    available_images = list(map(lambda x: [x["grayscale"], x["url"]], sb_data))

    desired_image_url = supabase.table("categories").select("desired_image_url").eq("id", category_id).execute().data[0]["desired_image_url"]
    
    res = requests.get(desired_image_url, stream=True)
    temp_filename = desired_image_url.rsplit("/", 1)[1]
    with open(temp_filename, "wb") as f:
        res.raw.decode_content = True
        shutil.copyfileobj(res.raw, f)
    
    desired_image = cv2.imread(temp_filename)
    
    # Resize the desired image to be a square with a number of pixels <= the number of uploaded images
    max_size = int(sqrt(len(available_images))) # The side length
    max_length = max_size * max_size # The # of pixels
    rs = cv2.resize(desired_image, (max_size, max_size))

    # Sort the desired image pixels and the available images by grayscale value (while also storing each grayscale value's corresponding URL/index).
    sorted_desired = sorted([(val.item(), i) for i, val in enumerate(rs.flatten()[:max_length])], key=lambda x: x[0])
    sorted_available = sorted(available_images, key=lambda x: x[0])[:max_length]

    # Put the URLs of the available image in the appropriate order
    urls = [""] * (max_size * max_size)
    for _, i in sorted_desired:
        urls[i] = sorted_available[i][1]
    
    # Delete temp file
    os.unlink(temp_filename)
    
    return {
        "urls": urls,
        "size": max_size
    }

