from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy import Column, Integer, String

# Database Connection URL
DATABASE_URL = "postgresql://postgres:password@localhost:5432/surgeai"

# Database Engine
engine = create_engine(DATABASE_URL)

# Database Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database Base
Base = declarative_base()

# Ensure tables are created in the database
Base.metadata.create_all(bind=engine)

# Database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# Database Models
class User(Base):
    __tablename__ = "users"
    
    id =       Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String, unique=False, index=True)
    email =    Column(String, unique=True, index=True)

# Create User in Database
def create_user(db, user):
    db_user = User(username=user.username, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get User by Email
def get_user_by_email(db, email):
    return db.query(User).filter(User.email == email).first()

# Get User by Username
def get_user_by_username(db, username):
    return db.query(User).filter(User.username == username).first()
