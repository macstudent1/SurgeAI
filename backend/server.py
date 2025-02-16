from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.context import CryptContext
from starlette.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine, get_db
from database import create_user, get_user_by_email, get_user_by_username

app = FastAPI()

# CORS
allowed_origins = [
  "...",  # The domain of our React frontend
]

# Middleware
app.add_middleware(
  CORSMiddleware,
  allow_origins=allowed_origins,  # Allow requests from our allowed origins (...our frontend)
  allow_credentials=True,
  allow_methods=["*"],  # Allow all HTTP methods
  allow_headers=["*"],  # Allow all headers
)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    email: str
    username: str
    password: str
    
# Hash password
def get_password_hash(password):
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
    
# Routes
@app.get("/")
def read_root():
    return {"Backend": "Working"}

# Signup
@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    try: 
        db_user = get_user_by_email(db, user.email)
        print(db_user)
    except:
        print("Error: Username or email already exists")
    
    try:
        user.password = get_password_hash(user.password)
        test = create_user(db, user)
    except Exception as e:
        print("Error creating user")
        print(e)
    
    return test

# Login
@app.post("/login")
def login(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    return "Logs In"

# Connect to Spotify
@app.get("/connect_spotify")
def connect_spotify(request: Request):
    # Unimplemented
    return "Connect Spotify"

