import cv2
import time
from collections import Counter
from deepface import DeepFace

# Initialize webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

emotion_list = []
start_time = time.time()
duration = 20

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

        emotion_list.append(emotion)
       # print(f"Emotion: {emotion}")  # Print detected emotions

        # Display emotion on the frame
        cv2.putText(frame, f"Emotion: {emotion}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    except Exception as e:
        print("Error during emotion analysis:", e)

    # Show the webcam feed
    cv2.imshow("Emotion Detector", frame)

    if time.time()-start_time> duration:
        break

    # Exit if 'q' is pressed
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

# Determine the final detected emotion that is most common from the list of emotions in the array
if emotion_list:
    final_detected_emotion = Counter(emotion_list).most_common(1)[0][0]
    print(f"Final detected emotion: {final_detected_emotion}")
else:
     final_detected_emotion = "Unable to detect emotion"
#test


