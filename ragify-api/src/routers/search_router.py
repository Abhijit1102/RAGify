from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from src.auth.dependencies import get_current_user
from src.models.users import User
from src.vector_db.dependencies import get_user_qdrant_manager
from src.db import get_db
from src.controllers.search_controller import SearchController  # 👈 import here
from src.schemas.search_query import SearchQuery
router = APIRouter(prefix="/search", tags=["Search"])

@router.post("/")
def search_documents(
    body: SearchQuery = Body(...),
    current_user: User = Depends(get_current_user),
    collection_manager = Depends(get_user_qdrant_manager),
    db: Session = Depends(get_db)
):
    return SearchController.search_documents_ai(
        query=body.query,
        session_name=body.session_name,
        current_user=current_user,
        collection_manager=collection_manager,
        db=db
    )