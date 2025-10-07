import boto3
import os
from fastapi import UploadFile
from src.config import Config

s3_client = boto3.client(
    "s3",
    endpoint_url=Config.R2_URL,
    aws_access_key_id=Config.R2_ACCESS_KEY,
    aws_secret_access_key=Config.R2_SECRET_KEY
)

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx", ".doc"}

def validate_file_extension(filename: str):
    """Ensure file has an allowed extension."""
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"File type {ext} not allowed")
    return ext

async def upload_to_r2(file: UploadFile) -> dict:
    """Upload file to R2 bucket and return metadata."""
    ext = validate_file_extension(file.filename)
    key = file.filename

    s3_client.upload_fileobj(
        file.file,
        Config.R2_BUCKET,
        key,
        ExtraArgs={"ContentType": file.content_type}
    )

    url = f"{Config.R2_PUBLIC_URL}/{key}"

    return {
        "url": url,
        "file_type": ext,
        "file_name": file.filename,
        "key": key,
    }

def delete_from_r2(key: str):
    """Delete file from R2 bucket."""
    if not key:
        raise ValueError("Key is empty")
    s3_client.delete_object(Bucket=Config.R2_BUCKET, Key=key)
