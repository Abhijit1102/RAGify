from sqlalchemy import create_engine, text
import os
from dotenv import load_env

load_env()

# Neon Postgres URL (example from Neon)
DATABASE_URL = os.getenv("POSTGRES_URI")  

# Create engine
engine = create_engine(DATABASE_URL)

# SQL statement to add public_id column
alter_table_sql = """
ALTER TABLE documents
ADD COLUMN public_id VARCHAR NOT NULL DEFAULT '';
"""

# Execute the SQL
with engine.connect() as conn:
    conn.execute(text(alter_table_sql))
    conn.commit()

print("Migration completed: public_id column added.")
