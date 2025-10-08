from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from src.schemas.users import RegisterSchema, LoginSchema
from src.db import get_db
from src.controllers.auth_controller import register_user, authenticate_user
from src.utils.api_response import api_response
from src.models.users import RoleEnum, User
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.auth.jwt import decode_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

# --- Register Route ---
@router.post("/register")
async def register(data: RegisterSchema, db: Session = Depends(get_db)):
    user = await register_user(db, data.username, data.password, data.role)
    if not user:
        return api_response.error(message="Username already exists", status_code=400)
    
    return api_response.success(
        data={"username": user.username, "role": user.role.value},
        message="User created successfully"
    )

# --- Login Route ---
@router.post("/login")
async def login(data: LoginSchema, db: Session = Depends(get_db)):
    result = await authenticate_user(db, data.username, data.password)
    if not result:
        return api_response.error(message="Invalid credentials", status_code=401)

    return api_response.success(
        data={
            "username": result["user"].username,
            "role": result["user"].role.value,
            "token": result["token"]
        },
        message="Login successful"
    )

# --- Current User Dependency ---
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        return api_response.error(message="Invalid token", status_code=401)
    
    def get_user_sync():
        return db.query(User).filter(User.username == payload["sub"]).first()
    
    user = await asyncio.to_thread(get_user_sync)
    if not user:
        return api_response.error(message="User not found", status_code=401)
    
    return user
