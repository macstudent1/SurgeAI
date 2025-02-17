from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.context import CryptContext
from starlette.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine, get_db
from database import create_user, get_user_by_email, get_user_by_username
from fastapi import FastAPI, WebSocket
from opencv.emotion_detect_ws import detect_emotion
import cv2
import numpy as np
from deepface import DeepFace
from fastapi.websockets import WebSocketDisconnect

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
    except Exception as e:
        print(e)
        print("Error: Username or email already exists")
    
    try:
        user.password = get_password_hash(user.password)
        user_id = create_user(db, user)
        print("User created successfully")
    except Exception as e:
        print(e)
        print("Error creating user")
    
    return user_id

# Login
@app.post("/login")
def login(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    try: 
        if db_user and verify_password(user.password, db_user.password):
            print("Logged In Successfully")
            return db_user.id
        else:
            print("Login Failed")
            return "Login Failed"
    except Exception as e:
        print(e)
        print("Error logging in")
        
        
# Websocket
@app.websocket("/ws") # This tries to detect emotion from opencv folder, detect emotion implementation (Not working)
async def websocket_endpoint(websocket: WebSocket):
    await detect_emotion(websocket)

@app.websocket("/emotion") # This tries to detect emotion directly from server (also Not working)
async def emotion_socket(websocket: WebSocket):
    await websocket.accept()
    emotion_list = []
    
    try:
        while True:
            # Receive the frame
            frame = await websocket.receive_bytes()
            nparr = np.frombuffer(frame, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Perform emotion analysis
            try:
                analysis = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
                emotion = analysis[0].get('dominant_emotion', 'Unknown')
                await websocket.send_text(emotion)  # Send emotion back to client
                break  # After sending the emotion, exit the loop

            except Exception as e:
                await websocket.send_text(f"Error: {str(e)}")
                break  # Exit on error
                
    except Exception as e:
        print(f"Error during WebSocket connection: {str(e)}")
    finally:
        await websocket.close()  # Close the WebSocket connection after sending the response

# Connect to Spotify
@app.get("/connect_spotify")
def connect_spotify(request: Request):
    # Unimplemented
    return "Connect Spotify"

