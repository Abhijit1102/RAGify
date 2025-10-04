from src.db import Base, engine
from src.models import users, documents

def delete_all_tables():
    Base.metadata.drop_all(bind=engine)
    print("All tables dropped successfully!")

if __name__ == "__main__":
    delete_all_tables()
