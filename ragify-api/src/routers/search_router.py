from fastapi import APIRouter, Depends, Body
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.auth.dependencies import get_current_user
from src.models.users import User
from src.models.chat_message import ChatSession, ChatMessage
from src.vector_db.document_store import DocumentStore
from src.vector_db.dependencies import get_user_qdrant_manager
from src.utils.api_response import api_response
from src.llm.ai_generator import LLMGenerator
from src.db import get_db

router = APIRouter(prefix="/search", tags=["Search"])

class SearchQuery(BaseModel):
    query: str
    session_name: str | None = None  # optional session name

@router.post("/")
def search_documents_ai(
    body: SearchQuery = Body(...),
    current_user: User = Depends(get_current_user),
    collection_manager = Depends(get_user_qdrant_manager),
    db: Session = Depends(get_db)
):
    query = body.query.strip()
    if not query:
        return api_response.error(message="Invalid input query", status_code=400)

    try:
        # 1️⃣ Create a new chat session for this query
        chat_session = ChatSession(user_id=current_user.id, session_name=body.session_name)
        db.add(chat_session)
        db.commit()
        db.refresh(chat_session)

        # 2️⃣ Save user message
        user_msg = ChatMessage(
            session_id=chat_session.id,
            role="user",
            content=query
        )
        db.add(user_msg)
        db.commit()

        # 3️⃣ Query documents
        store = DocumentStore(user=current_user, collection_manager=collection_manager)
        docs = store.query(query_text=query, limit=5)

        if not docs:
            bot_msg = ChatMessage(
                session_id=chat_session.id,
                role="bot",
                content="No relevant documents found.",
                file_name=None,
                page_number=None,
                score=0.0
            )
            db.add(bot_msg)
            db.commit()
            return api_response.success(
                data=[{"text": "", "file_name": None, "page_number": None, "score": 0.0}],
                message="No relevant documents found"
            )

        # 4️⃣ Generate AI answer
        generator = LLMGenerator()
        ai_output = generator.generate(context=docs, query=query)

        if ai_output.get("error"):
            return api_response.error(
                message=ai_output["error"],
                status_code=ai_output.get("status_code", 500)
            )

        # 5️⃣ Save AI response
        bot_msg = ChatMessage(
            session_id=chat_session.id,
            role="bot",
            content=ai_output.get("text", ""),  # assuming generator returns text
            file_name=ai_output.get("file_name"),
            page_number=ai_output.get("page_number"),
            score=ai_output.get("score")
        )
        db.add(bot_msg)
        db.commit()

        return api_response.success(
            data=[ai_output],
            message=f"AI-generated answer based on {len(docs)} documents"
        )

    except Exception as e:
        db.rollback()
        return api_response.error(
            message="Failed to generate AI search results",
            status_code=500,
            details=str(e)
        )
