from fastapi import APIRouter, Depends
from src.auth.dependencies import get_current_user
from src.utils.api_response import api_response

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/user")
def me(current_user=Depends(get_current_user)):
    return api_response.success(
        data={
            "username": current_user.username,
            "role": current_user.role.value  
        },
        message="User fetched successfully"
    )
