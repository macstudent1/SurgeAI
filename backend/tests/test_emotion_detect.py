import asyncio
import websockets
import cv2
import base64
import numpy as np

async def send_image():
    uri = "ws://localhost:8000/emotion"
    print("Attempting to connect to WebSocket...")
    
    async with websockets.connect(uri) as websocket:
        print("Connected. Sending image...")

        # Load the test image from file
        img = cv2.imread("test_image.jpg")  # Make sure to provide the correct path to your test image
        
        if img is None:
            print("Error: Could not read the image file.")
            return

        # Encode the image as base64
        _, buffer = cv2.imencode(".jpg", img)
        img_base64 = base64.b64encode(buffer).decode("utf-8")

        # Send the base64-encoded image to WebSocket server
        await websocket.send(img_base64)
        
        # Receive response from the server (emotion data)
        response = await websocket.recv()
        print(f"Response: {response}")
        
        # Ensure we don't try to read again after receiving the response
        print("Closing WebSocket connection.")
        await websocket.close()

# Run the asyncio loop to send the image
asyncio.run(send_image())