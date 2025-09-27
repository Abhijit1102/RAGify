from pydantic import BaseModel
from src.models.users import RoleEnum

class RegisterSchema(BaseModel):
    username: str
    password: str
    role: RoleEnum = RoleEnum.user

class LoginSchema(BaseModel):
    username: str
    password: str