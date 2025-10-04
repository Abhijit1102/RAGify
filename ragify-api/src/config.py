from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    # Server Configuration
    PORT = int(os.getenv("PORT", 8000))
    CLIENT_URL = os.getenv("CLIENT_URL", "http://localhost:5173")
    
    # MongoDB Configuration
    POSTGRES_URI = os.getenv(
        "POSTGRES_URI"
    )
    
    # Secret Keys
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

    # OPENAI 
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_CHAT_MODEL=  os.getenv("OPENAI_CHAT_MODEL")

    # CLOUDINARY
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")