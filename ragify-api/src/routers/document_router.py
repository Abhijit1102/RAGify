from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session
from src.auth.dependencies import get_current_user
from src.db import get_db
from src.models.users import User
from src.vector_db.dependencies import get_user_qdrant_manager
from src.utils.api_response import api_response
from src.utils.file_utils import save_upload_to_disk
from src.controllers.document_controller import process_document_upload, delete_document_r2, get_user_documents
import asyncio

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload/")
async def upload_document(
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    collection_manager = Depends(get_user_qdrant_manager)
):
    file_path = await save_upload_to_disk(file)

    # Fire and forget
    asyncio.create_task(
        process_document_upload(
            file=file,
            file_path=file_path,
            db=db,
            current_user=current_user,
            collection_manager=collection_manager
        )
    )

    return api_response.success(message="Upload started, processing in background.")

@router.delete("/{doc_id}")
async def delete_document(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    collection_manager = Depends(get_user_qdrant_manager)
):
    try:
        await delete_document_r2(db=db, current_user=current_user, doc_id=doc_id, collection_manager=collection_manager)
        return api_response.success(message="Document deleted successfully")
    except Exception as e:
        return api_response.error(message=str(e), status_code=404)

@router.get("/")
async def list_documents(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        docs = await get_user_documents(db=db, current_user=current_user)
        return api_response.success(data=docs, message=f"{len(docs)} document(s) found")
    except Exception as e:
        return api_response.error(message=str(e), status_code=500)
