import cv2
import numpy as np

# Talk to Arduino
import serial
import time
import os
import urllib.request

model_path = "emotion-ferplus.onnx"

if not os.path.exists(model_path):
  print("Downloading ONNX model..")
  url =  "https://github.com/onnx/models/raw/main/validated/vision/body_analysis/emotion_ferplus/model/emotion-ferplus-8.onnx"
  urllib.request.urlretrieve(url, model_path)


# Initialization Debugging
print("Initializing AI components... please wait.")
print("Loading neural network into memory...")
# Load ONNX model directly into OpenCV's built-in deep learning engine
net = cv2.dnn.readNetFromONNX(model_path)
print("Neural network loaded successfully!")

emotion_labels = ['Neutral', 'Happy', 'Surprise', 'Sad', 'Anger','Disgust','Fear', 'Contempt']

# Hardware connection
try: 
  arduino = serial.Serial('/dev/cu.usbmodem114601', 9600, timeout=1)

  #Brief pause
  time.sleep(2)

except Exception as e:
  print(f"Could not connect to Arduino: {e}")
  arduino = None

# Capture primary webcam
print("Waking up camera...")
# --- DEBUG WEBCAM ACCESS ---
for i in range(5):
    temp_cap = cv2.VideoCapture(i)
    if temp_cap.isOpened():
        print(f"Webcam found at index {i}")
        temp_cap.release()
    else:
        print(f"No webcam at index {i}")
# Start with index 0, or change to 1/2 if index 0 failed
cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

last_emotion = ""

hold_duration = 2.0  # How many seconds to hold a non-neutral emotion
emotion_timer = 0.0  # Tracks the exact time we last saw a real emotion

print("Starting camera... press \"Q\" to quit")

# Video Loop
while True:
  ret, frame = cap.read()

  # Break loop if camera not found
  if not ret:
    break

  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  faces = face_cascade.detectMultiScale(gray, 1.3, 5)

  for (x, y, w, h) in faces:
    
    # 1. Add a 20% margin around the face so the AI can see your whole head
    margin = int(w * 0.2)
    
    # Make sure the margin doesn't accidentally go off the edge of the screen
    y1, y2 = max(0, y - margin), min(frame.shape[0], y + h + margin)
    x1, x2 = max(0, x - margin), min(frame.shape[1], x + w + margin)
    
    # Crop using the new expanded box
    face_roi = gray[y1:y2, x1:x2]

    # 2. Try passing raw pixels (scalefactor=1.0) instead of decimals
    blob = cv2.dnn.blobFromImage(face_roi, scalefactor=1.0, size=(64, 64))

    # Feed formatted blob into ONNX NN
    net.setInput(blob)
    outputs = net.forward()

    # 3. Flatten the output safely just in case the ONNX model returns a weird 3D array
    logits = outputs[0].flatten()
    max_index = np.argmax(logits)
    emotion = emotion_labels[max_index]

    current_time = time.time()

    if emotion != "Neutral":
       emotion_timer = current_time
    else:
       if(current_time - emotion_timer) < hold_duration:
          emotion = last_emotion


    # If the newly detected emotion is different from the last one we saw
    if emotion != last_emotion:
        print(f"Detected emotion: {emotion}")
        if arduino:
            arduino.write(f"{emotion}\n".encode('utf-8'))
        last_emotion = emotion

    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.putText(frame, last_emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

  # Open a window and show the video frame with all our drawings on top of it
  cv2.imshow("Live Emotion Tracker (ONNX)", frame)

  if cv2.waitKey(5) & 0xFF == ord('q'):
        break
  
#Turn off webcam
cap.release()

# Close the video window we opened
cv2.destroyAllWindows()

# If the Arduino was connected, close the communication port so it's free for other apps
if arduino:
    arduino.close()