from sqlalchemy.orm import Session
from src.models.users import User, RoleEnum
from src.auth.security import hash_password, verify_password
from src.auth.jwt import create_access_token
import asyncio

async def register_user(db: Session, username: str, password: str, role: RoleEnum):
    def sync_register():
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            return None
        new_user = User(
            username=username,
            hashed_password=hash_password(password),
            role=role
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    return await asyncio.to_thread(sync_register)

async def authenticate_user(db: Session, username: str, password: str):
    def sync_auth():
        user = db.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.hashed_password):
            return None
        token = create_access_token({"sub": user.username, "role": user.role.value})
        return {"user": user, "token": token}

    return await asyncio.to_thread(sync_auth)
