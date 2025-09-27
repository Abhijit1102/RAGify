from src.db import get_db, Base, engine
from src.models.users import User, RoleEnum
from src.auth.security import hash_password

# Create tables if not exists
Base.metadata.create_all(bind=engine)

def create_users():
    db_gen = get_db()
    db = next(db_gen)
    try:
        # Check if users already exist
        #user_exist = db.query(User).filter(User.username == "abhi@gmail.com").first()
        admin_exist = db.query(User).filter(User.username == "admin@mail.com").first()
        
        # if not user_exist:
        #     user = User(
        #         username="abhi@gmail.com",
        #         hashed_password=hash_password("userpassword123"),  # replace with actual password
        #         role=RoleEnum.user
        #     )
        #     db.add(user)
        
        if not admin_exist:
            admin = User(
                username="admin@mail.com",
                hashed_password=hash_password("adminpassword123"),  # replace with actual password
                role=RoleEnum.admin
            )
            db.add(admin)
        
        db.commit()
        print("Users created successfully!")
    finally:
        db_gen.close()

if __name__ == "__main__":
    create_users()
