from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    # Server Configuration
    PORT = int(os.getenv("PORT", 8000))
    CLIENT_URL = os.getenv("CLIENT_URL", "http://localhost:5173")
    
    # POSTGRES
    POSTGRES_URI = os.getenv("POSTGRES_URI")

    # Secret Keys
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL")
    OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")
    OPENAI_EMBEDDING_DIMENSION = os.getenv("OPENAI_EMBEDDING_DIMENSION")

    # Cloudflare R2
    R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY")
    R2_SECRET_KEY = os.getenv("R2_SECRET_KEY")
    R2_URL = os.getenv("R2_URL")
    R2_BUCKET = os.getenv("R2_BUCKET")
    R2_PUBLIC_URL = os.getenv("R2_PUBLIC_URL")

    # Qdrant
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    QDRANT_URL = os.getenv("QDRANT_URL")
