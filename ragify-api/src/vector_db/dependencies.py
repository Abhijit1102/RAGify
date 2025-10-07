from fastapi import Depends
from src.models.users import User
from src.vector_db.qdrant_manager import qdrant_manager
from src.auth.dependencies import get_current_user  

def get_user_qdrant_manager(user: User = Depends(get_current_user)):
    """
    FastAPI dependency that returns a user-specific Qdrant collection manager.
    Ensures the collection exists (creates if missing).
    """
    collection_name = user.collection
    manager = qdrant_manager.get_collection_manager(collection_name=collection_name)
    manager.create_collection()  
    return manager
