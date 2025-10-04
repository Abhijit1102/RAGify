from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from src.db import get_db
from src.auth.dependencies import get_current_user
from src.models.users import User
from src.controllers.document_controller import upload_document_to_r2, get_user_documents, delete_document_r2

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload")
async def upload_file(
    document: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await upload_document_to_r2(document, db, current_user)

@router.get("/")
def list_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_documents(db, current_user)

@router.delete("/{doc_id}")
def remove_document(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        delete_document_r2(db, current_user, doc_id)
        return {"message": "Document deleted successfully"}
    except ValueError as e:
        return {"error": str(e)}
