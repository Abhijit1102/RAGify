from fastapi import UploadFile
from sqlalchemy.orm import Session
from src.models.documents import Document
from src.models.users import User
from src.utils.r2_utils import upload_to_r2, delete_from_r2
from src.utils.api_response import api_response

async def upload_document_to_r2(file: UploadFile, db: Session, current_user: User):
    try:
        uploaded_file = await upload_to_r2(file)

        new_doc = Document(
            file_name=uploaded_file["file_name"],
            file_type=uploaded_file["file_type"],
            url=uploaded_file["url"],        
            public_id=uploaded_file["key"],  
            user_id=current_user.id
        )
        db.add(new_doc)
        db.commit()
        db.refresh(new_doc)

        return api_response.success(
            data={
                "id": new_doc.id,
                "file_name": new_doc.file_name,
                "file_type": new_doc.file_type,
                "url": new_doc.url,
                "public_id": new_doc.public_id
            },
            message="File uploaded and saved successfully"
        )
    except Exception as e:
        return api_response.error(message=str(e), status_code=500)


def get_user_documents(db: Session, current_user: User):
    docs = db.query(Document).filter(Document.user_id == current_user.id).all()
    return [
        {
            "id": d.id,
            "file_name": d.file_name,
            "file_type": d.file_type,
            "url": d.url,
            "public_id": d.public_id
        }
        for d in docs
    ]

def delete_document_r2(db: Session, current_user: User, doc_id: int):
    doc = db.query(Document).filter(Document.id == doc_id, Document.user_id == current_user.id).first()
    if not doc:
        raise ValueError("Document not found")
    
    if not doc.public_id:
        raise ValueError("Cannot delete: public_id is empty")

    delete_from_r2(doc.public_id)
    db.delete(doc)
    db.commit()
    return True
