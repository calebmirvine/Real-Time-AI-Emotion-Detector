# Real-Time AI Emotion Detector

This is a short practice project I built as a stepping stone into machine learning and hardware. The goal was to learn how to link a Python computer vision script with physical Arduino hardware, paving the way for more complex robotics projects down the line.

## Demo
[![Emotion Detector Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

## How It Works
A Python script captures webcam footage and feeds it into a lightweight **ONNX AI model** (FER+) to score 8 different emotions. The script applies a timer to smooth out the data, then sends the result over USB to an Arduino Mega, which updates an LCD screen and changes the color of an RGB LED.

*Note: The AI is very sensitive to exaggerated expressions. I found "Disgust" and "Contempt" extremely difficult to replicate consistently!*

## Tech Stack & Hardware
* **Code:** Python (OpenCV, NumPy, PySerial), C++ (Arduino Framework)
* **AI/ML:** ONNX (Open Neural Network Exchange), Haar Cascades
* **Hardware:** Arduino Mega 2560, 16x2 LCD Display, Common RGB LED, Webcam

## Quick Wiring
* **RGB LED:** Red `Pin 2`, Green `Pin 3`, Blue `Pin 4`
* **LCD:** RS `Pin 7`, EN `Pin 8`, D4 `Pin 9`, D5 `Pin 10`, D6 `Pin 11`, D7 `Pin 12`

## How to Run
1. Upload the C++ code to the Arduino using PlatformIO.
2. In your terminal, navigate to the Python folder and run: `pip install opencv-python numpy pyserial`
3. Update the `serial.Serial()` port in `main.py` to match your OS (e.g., `'COM3'` or `'/dev/cu.usbmodem...'`).
4. Run `python main.py`. Press `q` in the video window to safely quit.

## Model Reference
The facial expression recognition model used in this project is the **Emotion FER+** model, sourced from the official [ONNX Model Zoo](https://github.com/onnx/models). It uses the FER+ annotations to classify faces into 8 standard emotion categories.
