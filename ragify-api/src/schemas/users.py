from typing import Optional
from pydantic import BaseModel
from src.models.users import RoleEnum

class RegisterSchema(BaseModel):
    username: str
    password: str
    role: Optional[RoleEnum] = RoleEnum.user   

class LoginSchema(BaseModel):
    username: str
    password: str
