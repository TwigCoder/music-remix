import os
import uuid
from pathlib import Path
from werkzeug.utils import secure_filename

UPLOAD_DIR = "uploads"
EXPORT_DIR = "export"

Path(UPLOAD_DIR).mkdir(exist_ok=True)
Path(EXPORT_DIR).mkdir(exist_ok=True)


def save_uploaded_file(uploaded_file):
    file_extension = uploaded_file.name.split(".")[-1].lower()
    file_name = f"{uuid.uuid4().hex}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, secure_filename(file_name))

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


def get_export_file_path(file_name="remixed_track.wav"):
    return os.path.join(EXPORT_DIR, secure_filename(file_name))


def clear_directory(directory):
    for file in Path(directory).glob("*"):
        file.unlink()


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
