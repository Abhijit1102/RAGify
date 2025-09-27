from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.sql import func
from src.db import Base
import enum

class RoleEnum(str, enum.Enum):
    admin = "admin"
    user = "user"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    role = Column(Enum(RoleEnum), default=RoleEnum.user, nullable=True)
