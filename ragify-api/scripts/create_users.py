from src.db import get_db, Base, engine
from src.models import User, RoleEnum, Document, Chunk  
from src.auth.security import hash_password

def init_db():
    """Ensure all tables exist in the database."""
    Base.metadata.create_all(bind=engine)

def create_users():
    """Create default users if they don’t already exist."""
    db_gen = get_db()
    db = next(db_gen)
    try:
        # Check if admin already exists
        admin_exist = db.query(User).filter(User.username == "admin@mail.com").first()

        if not admin_exist:
            admin = User(
                username="admin@mail.com",
                hashed_password=hash_password("adminpassword123"),  # Replace with secure password
                role=RoleEnum.admin,
                # No need to pass 'collection', default will be used
            )
            db.add(admin)

        # # Example for default user
        # user_exist = db.query(User).filter(User.username == "abhi@gmail.com").first()
        # if not user_exist:
        #     user = User(
        #         username="abhi@gmail.com",
        #         hashed_password=hash_password("userpassword123"),
        #         role=RoleEnum.user,
        #     )
        #     db.add(user)

        db.commit()
        print("✅ Users created successfully!")
        # Print collections to verify
        for u in db.query(User).all():
            print(f"{u.username} → collection: {u.collection}")

    finally:
        db_gen.close()

if __name__ == "__main__":
    init_db()
    create_users()
