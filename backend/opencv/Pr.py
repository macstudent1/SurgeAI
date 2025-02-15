import cv2
from deepface import DeepFace

# Initialize webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame")
        break

    try:
        # Perform emotion analysis
        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        
        if isinstance(analysis, list) and len(analysis) > 0:
            emotion = analysis[0].get('dominant_emotion', 'Unknown')
        else:
            emotion = "Unknown"

        print(f"Emotion: {emotion}")  # Print detected emotion

        # Display emotion on the frame
        cv2.putText(frame, f"Emotion: {emotion}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    except Exception as e:
        print("Error during emotion analysis:", e)

    # Show the webcam feed
    cv2.imshow("Emotion Detector", frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()


