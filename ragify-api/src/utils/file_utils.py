import aiofiles
import os
from fastapi import UploadFile
from src.config import Config

async def save_upload_to_disk(file: UploadFile) -> str:
    os.makedirs(Config.UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(Config.UPLOAD_DIR, os.path.basename(file.filename))

    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read()
        await f.write(content)

    return os.path.abspath(file_path)
