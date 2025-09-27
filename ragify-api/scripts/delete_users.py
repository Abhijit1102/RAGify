from src.db import get_db, Base, engine
from src.models.users import User

def delete_users():
    db_gen = get_db()
    db = next(db_gen)
    try:
        # Delete specific users
        db.query(User).filter(User.username.in_(["abhi@gmail.com", "admin@mail.com"])).delete(synchronize_session=False)
        db.commit()
        print("Users deleted successfully!")
    finally:
        db_gen.close()

if __name__ == "__main__":
    delete_users()
