from sqlalchemy import create_engine, text
import os

# Neon Postgres URL (example from Neon)
DATABASE_URL = "postgresql://neondb_owner:npg_ctUy09PDkuqi@ep-plain-rain-a1xtnq4t-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"  

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
