from sqlalchemy import text
from src.db import get_db

def test_connection():
    db_gen = get_db()
    db = next(db_gen)  
    try:
        result = db.execute(text("SELECT 1")).fetchone()  
        print("Postgres Connection OK:", result[0] == 1)
    finally:
        db_gen.close()

if __name__ == "__main__":
    test_connection()
