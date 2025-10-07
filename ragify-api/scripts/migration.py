from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Import your database setup and models
from src.db import Base, engine
from src.models.users import User
from src.models.documents import Document
from src.models.chunks import Chunk
from src.models.chat_message import ChatSession, ChatMessage  # new models

# Load environment variables
load_dotenv()

# 1️⃣ Ensure base tables from models exist
Base.metadata.create_all(engine)
print("✅ Base tables created (users, documents, chunks, chat sessions).")

# 2️⃣ Custom SQL migrations
migration_sql = [
    # Add missing column to documents
    """
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM information_schema.columns
            WHERE table_name='documents' AND column_name='public_id'
        ) THEN
            ALTER TABLE documents ADD COLUMN public_id VARCHAR NOT NULL DEFAULT '';
        END IF;
    END $$;
    """,
    # Create chunks table (if not exists)
    """
    CREATE TABLE IF NOT EXISTS chunks (
        id SERIAL PRIMARY KEY,
        text TEXT NOT NULL,
        embedding DOUBLE PRECISION[],
        page_number INTEGER,
        file_name VARCHAR NOT NULL,
        document_id INTEGER REFERENCES documents(id) ON DELETE CASCADE
    );
    """,
    # Create chat_sessions table
    """
    CREATE TABLE IF NOT EXISTS chat_sessions (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE NOT NULL,
        session_name VARCHAR,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
    );
    """,
    # Create chat_messages table
    """
    CREATE TABLE IF NOT EXISTS chat_messages (
        id SERIAL PRIMARY KEY,
        session_id INTEGER REFERENCES chat_sessions(id) ON DELETE CASCADE NOT NULL,
        role VARCHAR NOT NULL,
        content TEXT NOT NULL,
        file_name VARCHAR,
        page_number INTEGER,
        score DOUBLE PRECISION,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
    );
    """
]

# 3️⃣ Execute the migrations
with engine.connect() as conn:
    for sql in migration_sql:
        conn.execute(text(sql))
    conn.commit()

print("✅ Migration completed successfully.")
