from sqlalchemy import Column, Integer, String, ForeignKey, Float, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from src.db import Base

class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    embedding = Column(ARRAY(Float), nullable=False)
    page_number = Column(Integer, nullable=True, index=True)
    file_name = Column(String, nullable=False, index=True)

    document_id = Column(
        Integer, 
        ForeignKey("documents.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )

    document = relationship("Document", back_populates="chunks")

    __table_args__ = (
        # Composite index for fast lookup of chunks from a specific file/document
        Index("ix_chunks_doc_file", "document_id", "file_name"),
    )
