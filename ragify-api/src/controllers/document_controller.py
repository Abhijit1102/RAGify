import os
from fastapi import UploadFile
from sqlalchemy.orm import Session
from src.models.documents import Document
from src.models.chunks import Chunk
from src.models.users import User
from src.services.cloudflare_r2_service import upload_to_r2, delete_from_r2
from src.services.document_store_service import DocumentStore
import asyncio

# ---------------- Upload to R2 + DB + Vector ----------------
async def upload_document_to_r2(
    file: UploadFile,
    file_path: str,
    db: Session,
    current_user: User,
    collection_manager
) -> dict:
    import mimetypes

    mime_type, _ = mimetypes.guess_type(file.filename)
    file_type = mime_type or os.path.splitext(file.filename)[1].lstrip('.') or "unknown"

    # Upload to R2
    uploaded_file = await upload_to_r2(file)
    if not uploaded_file or not uploaded_file.get("url") or not uploaded_file.get("key"):
        raise ValueError("R2 upload failed")

    # Store in vector DB + SQL DB in background thread
    async def add_doc():
        doc_store = DocumentStore(user=current_user, collection_manager=collection_manager)
        document: Document = await doc_store.add_document(
            db=db,
            file_path=file_path,
            file_name=file.filename,
            extra_metadata={
                "file_type": file_type,
                "url": uploaded_file["url"],
                "public_id": uploaded_file["key"]
            }
        )
        return document

    document = await add_doc()

    return {
        "id": document.id,
        "file_name": document.file_name,
        "file_type": file_type,
        "url": uploaded_file["url"],
        "public_id": uploaded_file["key"]
    }

# ---------------- Process document in background ----------------
async def process_document_upload(file: UploadFile, file_path: str, db: Session, current_user: User, collection_manager):
    try:
        doc_meta = await upload_document_to_r2(
            file=file,
            file_path=file_path,
            db=db,
            current_user=current_user,
            collection_manager=collection_manager
        )
        print("Document processed:", doc_meta)
    finally:
        # Delete local file asynchronously
        if file_path and isinstance(file_path, str) and os.path.exists(file_path):
            await asyncio.to_thread(os.remove, file_path)
            print("Local file deleted:", file_path)

# ---------------- Delete Document ----------------
async def delete_document_r2(db: Session, current_user: User, doc_id: int, collection_manager) -> bool:
    def sync_delete():
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

    return await asyncio.to_thread(sync_delete)

# ---------------- List User Documents ----------------
async def get_user_documents(db: Session, current_user: User):
    def fetch_docs():
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

    return await asyncio.to_thread(fetch_docs)
