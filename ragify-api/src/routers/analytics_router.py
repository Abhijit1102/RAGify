from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict
from src.db import get_db
from src.models.users import User, RoleEnum
from src.models.documents import Document
from src.models.chunks import Chunk
from src.models.chat_message import ChatSession, ChatMessage
from src.auth.dependencies import get_current_user
from src.utils.api_response import api_response 

router = APIRouter(
    prefix="/admin/analytics",
    tags=["Admin Analytics"],
)


def get_current_admin(user: User = Depends(get_current_user)):
    """
    Ensure the current user is an admin
    """
    if user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to access this resource",
        )
    return user


@router.get("/")
def admin_dashboard(db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    """
    Returns analytics data for admin dashboard including per-user stats
    """
    # Total users
    total_users = db.query(User).count()
    total_admins = db.query(User).filter(User.role == RoleEnum.admin).count()
    total_regular_users = db.query(User).filter(User.role == RoleEnum.user).count()

    # Total documents
    total_documents = db.query(Document).count()

    # Documents per user
    documents_per_user = (
        db.query(User.username, func.count(Document.id).label("doc_count"))
        .outerjoin(Document, Document.user_id == User.id)
        .group_by(User.username)
        .all()
    )

    # Chat sessions per user
    chat_sessions_per_user = (
        db.query(User.username, func.count(ChatSession.id).label("session_count"))
        .outerjoin(ChatSession, ChatSession.user_id == User.id)
        .group_by(User.username)
        .all()
    )

    # Chat messages per user (optional)
    chat_messages_per_user = (
        db.query(User.username, func.count(ChatMessage.id).label("message_count"))
        .outerjoin(ChatSession, ChatSession.user_id == User.id)
        .outerjoin(ChatMessage, ChatMessage.session_id == ChatSession.id)
        .group_by(User.username)
        .all()
    )

    # Combine per-user stats
    per_user_stats = []
    for username, doc_count in documents_per_user:
        session_count = next((s_count for u_name, s_count in chat_sessions_per_user if u_name == username), 0)
        message_count = next((m_count for u_name, m_count in chat_messages_per_user if u_name == username), 0)
        per_user_stats.append({
            "username": username,
            "documents": doc_count,
            "chat_sessions": session_count,
            "chat_messages": message_count
        })

    # Total chat sessions & messages
    total_chat_sessions = sum(s for _, s in chat_sessions_per_user)
    total_chat_messages = sum(m for _, m in chat_messages_per_user)
    total_chunks = db.query(Chunk).count()

    data = {
        "users": {
            "total": total_users,
            "admins": total_admins,
            "regular_users": total_regular_users,
        },
        "per_user_stats": per_user_stats,
        "documents": {
            "total": total_documents,
        },
        "chat": {
            "total_sessions": total_chat_sessions,
            "total_messages": total_chat_messages,
        },
        "chunks": {
            "total": total_chunks
        },
    }

    return api_response.success(data=data, message="Admin analytics fetched successfully")
