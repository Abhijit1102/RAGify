from sqlalchemy import Column, Integer, String, Enum, event
from sqlalchemy.orm import relationship
import enum
from src.db import Base

class RoleEnum(str, enum.Enum):
    admin = "admin"
    user = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.user, nullable=True)

    # Indexed + unique
    collection = Column(String, unique=True, index=True, nullable=False)

    documents = relationship("Document", back_populates="user")


@event.listens_for(User, "before_insert")
def set_collection(mapper, connection, target):
    if not target.collection:
        target.collection = f"collection_{target.username}"
