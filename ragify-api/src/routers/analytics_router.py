from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db import get_db
from src.models.users import User, RoleEnum
from src.controllers.admin_analytics_controller import AdminAnalyticsController
from src.auth.dependencies import get_current_user  
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
    return AdminAnalyticsController.get_dashboard_data(db)
