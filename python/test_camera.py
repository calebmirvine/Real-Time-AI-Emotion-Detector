import cv2
print("Attempting to open camera...")
cap = cv2.VideoCapture(0, cv2.CAP_MSMF)
if cap.isOpened():
    print("Success! Camera is open.")
    ret, frame = cap.read()
    if ret:
        print("Success! Captured a frame.")
    cap.release()
else:
    print("Failed to open camera.")