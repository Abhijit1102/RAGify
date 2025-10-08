from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship
from src.db import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False, index=True)     # for searching by name
    file_type = Column(String, nullable=False, index=True)     # for filtering by type
    url = Column(String, nullable=False, unique=True)          # URLs should be unique
    public_id = Column(String, nullable=False, unique=True)    # e.g., Cloudinary ID

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    user = relationship("User", back_populates="documents")

    chunks = relationship("Chunk", back_populates="document", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_documents_user_file", "user_id", "file_name"),  # composite index
    )
