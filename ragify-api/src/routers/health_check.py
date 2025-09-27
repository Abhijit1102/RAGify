from fastapi import APIRouter
from src.utils.api_response import api_response

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/")
async def health_check():
    """
    Health check endpoint for monitoring.
    Returns 200 OK if API is running.
    """
    return api_response.success(message="RAGify API is healthy 🚀", data={"status": "ok"})
