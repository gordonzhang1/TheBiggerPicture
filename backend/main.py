from flask import abort, Flask, request
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = ""
ALLOWED_EXTENSIONS = {"png", "jpg"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def valid_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.post("/api/upload-images")
def upload_images():
    if "images" not in request.files:
        abort(400)
    
    images = request.files.getlist("images")
    filenames = []

    for i, image in enumerate(images):
        filename = secure_filename(image.filename)
        filenames.append(filename)
        image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    
    return {"success": True}
