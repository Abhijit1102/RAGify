from src.db import Base, engine

# Import all models so they are registered with Base
from src.models.users import User, RoleEnum
from src.models.documents import Document
from src.models.chunks import Chunk
from src.models.chat_message import ChatSession, ChatMessage

def delete_all_tables():
    Base.metadata.drop_all(bind=engine)
    print("All tables dropped successfully!")

if __name__ == "__main__":
    delete_all_tables()
