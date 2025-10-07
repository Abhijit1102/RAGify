from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.models.chat_message import ChatSession, ChatMessage
from src.auth.dependencies import get_current_user
from src.models.users import User
from src.db import get_db
from src.schemas.chat import ChatSessionResponse, ChatMessageResponse
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["Chat"])

# Fetch all sessions for a user
@router.get("/sessions", response_model=List[ChatSessionResponse])
def get_user_chat_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sessions = (
        db.query(ChatSession)
        .filter(ChatSession.user_id == current_user.id)
        .order_by(ChatSession.created_at.desc())
        .all()
    )
    return sessions

# Fetch messages for a session
@router.get("/{session_id}/messages", response_model=List[ChatMessageResponse])
def get_chat_session_messages(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id, ChatSession.user_id == current_user.id)
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return session.messages

# Create a message (and session if needed)
class MessageCreate(BaseModel):
    content: str
    session_id: int | None = None  # optional for new session

@router.post("/messages/", response_model=ChatMessageResponse)
def post_message(
    msg: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Create new session if not provided
    if not msg.session_id:
        session = ChatSession(user_id=current_user.id)
        db.add(session)
        db.commit()
        db.refresh(session)
    else:
        session = db.query(ChatSession).filter(
            ChatSession.id == msg.session_id, ChatSession.user_id == current_user.id
        ).first()
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")

    # Set session_name from first message
    if not session.session_name:
        session.session_name = msg.content[:100]

    # Save message
    message = ChatMessage(
        session_id=session.id,
        role="user",
        content=msg.content
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    db.refresh(session)

    return message
