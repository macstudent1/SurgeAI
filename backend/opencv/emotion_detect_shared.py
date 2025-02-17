import numpy as np
import cv2
import time
from collections import Counter
from deepface import DeepFace
# Initialize webcam

def detect_emotion(frame):
    nparr = np.frombuffer(frame, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Perform emotion analysis
    try:
        analysis = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
        emotion = analysis[0].get('dominant_emotion', 'Unknown')
        return emotion

    except Exception as e:
        print(f"Error: {str(e)}")
        return "Error"

    # Perform emotion analysis
    analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
    
    if isinstance(analysis, list) and len(analysis) > 0:
        emotion = analysis[0].get('dominant_emotion', 'Unknown')
    else:
        emotion = "Unknown"

    return emotion


