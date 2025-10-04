import boto3
import os
from fastapi import UploadFile

R2_ENDPOINT = os.getenv("R2_URL")  
R2_PUBLIC_URL = os.getenv("R2_PUBLIC_URL")  
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY")
R2_SECRET_KEY = os.getenv("R2_SECRET_KEY")
R2_BUCKET = os.getenv("R2_BUCKET")

s3_client = boto3.client(
    "s3",
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY
)

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx", ".doc"}

def validate_file_extension(filename: str):
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"File type {ext} not allowed")
    return ext

async def upload_to_r2(file: UploadFile) -> dict:
    ext = validate_file_extension(file.filename)
    key = file.filename  

    s3_client.upload_fileobj(
        file.file,
        R2_BUCKET,
        key,
        ExtraArgs={"ContentType": file.content_type}
    )

    # Construct fully public URL
    url = f"{R2_PUBLIC_URL}/{key}"

    return {
        "url": url,
        "file_type": ext,
        "file_name": file.filename,
        "key": key
    }

def delete_from_r2(key: str):
    if not key:
        raise ValueError("Key is empty")
    s3_client.delete_object(Bucket=R2_BUCKET, Key=key)
