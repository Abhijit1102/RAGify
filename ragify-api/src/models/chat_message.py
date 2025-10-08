from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Text,
    Float,
    Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.db import Base


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    session_name = Column(String, nullable=True, index=True)  # for searching sessions
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    user = relationship("User", back_populates="chat_sessions")
    messages = relationship(
        "ChatMessage",
        back_populates="session",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_chat_sessions_user_session", "user_id", "session_name"),
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(
        Integer,
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    role = Column(String, nullable=False, index=True)  # 'user' or 'bot'
    content = Column(Text, nullable=False)
    file_name = Column(String, nullable=True, index=True)
    page_number = Column(Integer, nullable=True, index=True)
    score = Column(Float, nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationship
    session = relationship("ChatSession", back_populates="messages")

    __table_args__ = (
        Index("ix_chat_messages_session_role", "session_id", "role"),
    )


# --- Add relationship to User model ---
from src.models.users import User

User.chat_sessions = relationship(
    "ChatSession",
    back_populates="user",
    cascade="all, delete-orphan"
)
