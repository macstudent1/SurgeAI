import asyncio
import websockets
import cv2
import base64
import numpy as np

async def send_image():
    uri = "ws://127.0.0.1:8000/ws"
    print("Attempting to connect to WebSocket...")
    
    async with websockets.connect(uri) as websocket:
        print("Connected. Sending image...")
        
        # Load and encode image
        img = cv2.imread("test_image.jpg")  # Replace with your test image path
        _, buffer = cv2.imencode(".jpg", img)
        img_base64 = base64.b64encode(buffer).decode("utf-8")
        
        await websocket.send(img_base64)
        response = await websocket.recv()
        print(f"Response: {response}")
        
asyncio.run(send_image())