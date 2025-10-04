from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from src.schemas.users import RegisterSchema, LoginSchema
from src.db import get_db
from src.controllers import auth_controller
from src.utils.api_response import api_response

router = APIRouter(prefix="/auth", tags=["Auth"])

# --- Register Route ---
@router.post("/register")
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    user = auth_controller.register_user(db, data.username, data.password, data.role)
    if not user:
        return api_response.error(message="Username already exists", status_code=400)
    
    return api_response.success(
        data={"username": user.username, "role": user.role.value},
        message="User created successfully"
    )

# --- Login Route with HttpOnly Cookie ---
@router.post("/login")
def login(data: LoginSchema, response: Response, db: Session = Depends(get_db)):
    result = auth_controller.authenticate_user(db, data.username, data.password)
    if not result:
        return api_response.error(message="Invalid credentials", status_code=401)

    token = result["token"]

    return api_response.success(
    data={
        "username": result["user"].username,
        "role": result["user"].role.value,
        "token": result["token"]  
    },
    message="Login successful"
)
