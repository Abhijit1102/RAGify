# src/vector_db/document_store.py

from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from src.services.embedding_service import embedding_service
from src.models.documents import Document
from src.models.chunks import Chunk
from src.models.users import User
import uuid


class DocumentStore:
    def __init__(self, user: User, collection_manager=None):
        self.user = user
        self.collection = collection_manager
        if not self.collection:
            raise ValueError("Collection manager is required")
        self.collection.create_collection()

    def add_document(
        self,
        db: Session,
        file_path: str,
        file_name: str,
        extra_metadata: Optional[Dict] = None
    ) -> Document:
        """
        Process document: extract chunks, embeddings, store in vector DB,
        and save Document + Chunk records in SQL DB.
        """
        # Extract chunks
        chunks = embedding_service.process_document(file_path)
        texts = [c["text"] for c in chunks if c.get("text")]
        if not texts:
            raise ValueError("No text found in document")

        # Embed chunks
        embeddings = embedding_service.embed_text(texts)
        ids = [str(uuid.uuid4()) for _ in texts]

        # Insert into vector DB
        payloads = [
            {
                "text": chunks[i]["text"],
                "file_name": file_name,
                "page_number": chunks[i].get("page_number", 1),
                **(extra_metadata or {})
            }
            for i in range(len(chunks))
        ]
        self.collection.insert_data(vectors=embeddings, payloads=payloads, ids=ids)

        # Save Document metadata in DB
        document = Document(
            file_name=file_name,
            user_id=self.user.id,
            file_type=extra_metadata.get("file_type") if extra_metadata else "unknown",
            url=extra_metadata.get("url") if extra_metadata else None,
            public_id=extra_metadata.get("public_id") if extra_metadata else None
        )
        db.add(document)
        db.commit()
        db.refresh(document)

        # Save chunks in DB
        chunk_records = [
            Chunk(
                text=chunks[i]["text"],
                embedding=embeddings[i],
                page_number=chunks[i].get("page_number", 1),
                file_name=file_name,
                document_id=document.id
            )
            for i in range(len(chunks))
        ]
        db.add_all(chunk_records)
        db.commit()

        return document


    def query(self, query_text: str, limit: int = 5) -> List[Dict]:
        if not query_text.strip():
            return []

        query_vector = embedding_service.embed_text([query_text])[0]
        results = self.collection.search(query_vector=query_vector, limit=limit)

        return [
            {
                "text": r.payload.get("text", ""),
                "file_name": r.payload.get("file_name", ""),
                "page_number": r.payload.get("page_number", None),
                "score": getattr(r, "score", None)
            }
            for r in results
        ]
