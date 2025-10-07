import os
import mimetypes
from fastapi import UploadFile
from sqlalchemy.orm import Session
from src.models.documents import Document
from src.models.chunks import Chunk
from src.models.users import User
from src.utils.r2_utils import upload_to_r2, delete_from_r2
from src.vector_db.document_store import DocumentStore


async def upload_document_to_r2(
    file: UploadFile,
    file_path: str,
    db: Session,
    current_user: User,
    collection_manager
) -> dict:
    """
    Upload a file to R2, extract chunks, embed, store in vector DB,
    and save metadata in SQL DB (documents + chunks tables)
    """
    try:
        # Detect file type
        mime_type, _ = mimetypes.guess_type(file.filename)
        file_type = mime_type or os.path.splitext(file.filename)[1].lstrip('.') or "unknown"

        # Upload to R2
        uploaded_file = await upload_to_r2(file)
        if not uploaded_file or not uploaded_file.get("url") or not uploaded_file.get("key"):
            raise ValueError("R2 upload failed")

        # Process document: chunks + embeddings + vector DB + SQL DB
        doc_store = DocumentStore(user=current_user, collection_manager=collection_manager)
        document: Document = doc_store.add_document(
            db=db,
            file_path=file_path,
            file_name=file.filename,
            extra_metadata={"file_type": file_type, "url": uploaded_file["url"], "public_id": uploaded_file["key"]}
        )

        # Return document metadata
        return {
            "id": document.id,
            "file_name": document.file_name,
            "file_type": file_type,
            "url": uploaded_file["url"],
            "public_id": uploaded_file["key"]
        }

    except Exception as e:
        raise e


def delete_document_r2(db: Session, current_user: User, doc_id: int, collection_manager) -> bool:
    """
    Delete a document + its chunks from both vector DB and SQL DB + R2
    """
    from src.models.documents import Document

    doc: Document = db.query(Document).filter(
        Document.id == doc_id, Document.user_id == current_user.id
    ).first()

    if not doc:
        raise ValueError("Document not found")
    if not doc.public_id:
        raise ValueError("Cannot delete: public_id is empty")

    # Remove from vector DB
    collection_manager.delete_by_file_name(doc.file_name)

    # Remove from R2
    delete_from_r2(doc.public_id)

    # Remove from chunks table
    db.query(Chunk).filter(Chunk.document_id == doc.id).delete()

    # Remove from documents table
    db.delete(doc)
    db.commit()

    return True


def get_user_documents(db: Session, current_user: User) -> list[dict]:
    """
    List all documents for a user
    """
    docs = db.query(Document).filter(Document.user_id == current_user.id).all()
    return [
        {
            "id": d.id,
            "file_name": d.file_name,
            "file_type": getattr(d, "file_type", "unknown"),
            "url": getattr(d, "url", ""),
            "public_id": getattr(d, "public_id", "")
        }
        for d in docs
    ]
