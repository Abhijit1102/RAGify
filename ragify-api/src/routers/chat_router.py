from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from src.controllers.chat_controller import ChatControllerAsync
from src.auth.dependencies import get_current_user
from src.models.users import User
from src.schemas.message_create import MessageCreate 
from src.db import get_db

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.get("/sessions")
async def get_user_chat_sessions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ChatControllerAsync.get_user_chat_sessions(db=db, current_user=current_user)

@router.get("/{session_id}/messages")
async def get_chat_session_messages(session_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ChatControllerAsync.get_chat_session_messages(db=db, current_user=current_user, session_id=session_id)

@router.post("/messages/")
async def post_message(msg: MessageCreate = Body(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ChatControllerAsync.post_message(db=db, current_user=current_user, content=msg.content, session_id=msg.session_id)
