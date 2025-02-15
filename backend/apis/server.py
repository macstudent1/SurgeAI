from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.context import CryptContext
from starlette.requests import Request
from fastapi.middleware.cors import CORSMiddleware

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

# Database Connection URL
DATABASE_URL = "postgresql://postgres:password@localhost:5432/surgeai"

# Database connection
def get_db():
    ...

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

# Create User
def create_user(db: Session, user: UserCreate):
    # Unimplemented
    db_user = None # Create user
    db.add(db_user)
    return db_user
    
# Signup
@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = None # Get user by email
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = None # Get user by username
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Calls Create User function
    
    return "Signs Up" 

# Login
@app.post("/login")
def login(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    db_user = None # Get user by email
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