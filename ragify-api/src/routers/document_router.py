# src/routers/document_router.py

import os
from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session
from src.auth.dependencies import get_current_user
from src.models.users import User
from src.db import get_db
from src.vector_db.dependencies import get_user_qdrant_manager
from src.utils.api_response import api_response
from src.utils.file_utils import save_upload_to_disk
from src.controllers.document_controller import (
    upload_document_to_r2,
    delete_document_r2,
    get_user_documents
)

router = APIRouter(prefix="/documents", tags=["Documents"])


# ---------------- Upload Document ----------------
@router.post("/upload/")
async def upload_document(
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    collection_manager = Depends(get_user_qdrant_manager)
):
    local_path = None
    try:
        # Save file locally
        local_path = save_upload_to_disk(file)
        print("File saved at:", local_path)

        # Upload to R2 + store embeddings/chunks
        doc_meta = await upload_document_to_r2(
            file=file,
            file_path=local_path,
            db=db,
            current_user=current_user,
            collection_manager=collection_manager
        )

        return api_response.success(data=doc_meta, message="Document uploaded and processed successfully")

    except Exception as e:
        return api_response.error(message=str(e), status_code=500)

    finally:
        # Remove local file
        if local_path and os.path.exists(local_path):
            os.remove(local_path)
            print("Local file deleted:", local_path)


# ---------------- Delete Document ----------------
@router.delete("/{doc_id}")
def delete_document(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    collection_manager = Depends(get_user_qdrant_manager)
):
    try:
        delete_document_r2(db=db, current_user=current_user, doc_id=doc_id, collection_manager=collection_manager)
        return api_response.success(message="Document deleted successfully")
    except Exception as e:
        return api_response.error(message=str(e), status_code=404)


# ---------------- List Documents ----------------
@router.get("/")
def list_documents(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        docs = get_user_documents(db=db, current_user=current_user)
        return api_response.success(data=docs, message=f"{len(docs)} document(s) found")
    except Exception as e:
        return api_response.error(message=str(e), status_code=500)
