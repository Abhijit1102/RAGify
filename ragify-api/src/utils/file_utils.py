import os
from fastapi import UploadFile

UPLOAD_DIR = "uploads"

def save_upload_to_disk(file: UploadFile) -> str:
    """
    Save uploaded file directly to /uploads directory and return absolute path.
    """
    # Ensure the upload folder exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Create a safe file path
    safe_filename = os.path.basename(file.filename)
    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    # Reset file pointer and write content to disk
    file.file.seek(0)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Return the absolute path of saved file
    abs_path = os.path.abspath(file_path)
    print(f"✅ File saved successfully at: {abs_path}")
    return abs_path
