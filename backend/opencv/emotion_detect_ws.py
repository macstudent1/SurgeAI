import cv2
import numpy as np
import base64
from fastapi import WebSocket
from deepface import DeepFace

clients = [] 

def base64_to_image(base64_str):
    """Convert base64 string to OpenCV image."""
    img_data = base64.b64decode(base64_str)
    np_arr = np.frombuffer(img_data, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

async def detect_emotion(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()  # Receive base64 image from frontend
            frame = base64_to_image(data)  # Convert base64 to OpenCV image
            
            try:
                # Emotion detection
                analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                emotion = analysis[0].get('dominant_emotion', 'Unknown')
            except:
                emotion = "Unknown"
            
            # Send detected emotion back to frontend
            await websocket.send_json({"emotion": emotion})
    
    except Exception as e:
        print("Error:", e)
    
    finally:
        clients.remove(websocket)

