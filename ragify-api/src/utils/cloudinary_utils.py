import os
from fastapi import UploadFile
from src.utils.cloudinary_client import cloudinary_upload

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx", ".doc"}

def validate_file_extension(filename: str):
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"File type {ext} not allowed")
    return ext

async def upload_to_cloudinary(file: UploadFile) -> dict:
    # Validate file type
    ext = validate_file_extension(file.filename)
    
    # PDFs/TXT open inline, DOC/DOCX download
    resource_type = "auto" if ext in {".pdf", ".txt"} else "raw"

    # Use a clean public_id (no extension)
    public_id = os.path.splitext(file.filename)[0]

    # Upload to Cloudinary
    result = cloudinary_upload(
        file.file,
        resource_type=resource_type,
        public_id=public_id
    )

    # Ensure URL is HTTPS
    secure_url = result.get("secure_url")
    if not secure_url:
        raise ValueError("Failed to upload file to Cloudinary")

    return {
        "url": secure_url,
        "file_type": ext,
        "file_name": file.filename,
        "public_id": public_id  # store for deletion later
    }
