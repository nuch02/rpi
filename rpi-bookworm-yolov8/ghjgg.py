import cv2
from picamera2 import Picamera2
import pandas as pd
from ultralytics import YOLO
import cvzone
import numpy as np
from gtts import gTTS
import os

# Initialize the Picamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (320, 240)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# Load your two models
model1 = YOLO('/home/anuj/raspi/rpi-bookworm-yolov8/yolov8n.pt')
model2 = YOLO('/home/anuj/merge/best.pt')

# Load class names
with open("coconew.txt", "r") as my_file:
    class_list = my_file.read().split("\n")

count = 0

while True:
    im = picam2.capture_array()
    
    count += 1
    if count % 3 != 0:
        continue
    
    frame_width = im.shape[1]
    
    # Run inference on the same image with both models
    results1 = model1.predict(im)
    results2 = model2.predict(im)
    
    # Extract detections from both results
    px1 = pd.DataFrame(results1[0].boxes.data).astype("float")
    px2 = pd.DataFrame(results2[0].boxes.data).astype("float")
    
    # Check if px2 is empty and handle accordingly
    if px2.empty:
        combined_detections = px1.values
    else:
        combined_detections = np.vstack((px1.values, px2.values))
    
    for row in combined_detections:
        x1, y1, x2, y2, _, d = map(int, row[:6])
        c = class_list[d]
        
        # Determine position
        center_x = (x1 + x2) // 2
        position = "left" if center_x < frame_width // 3 else "middle" if center_x < 2 * frame_width // 3 else "right"
        
        cv2.rectangle(im, (x1, y1), (x2, y2), (0, 0, 255), 2)
        text = f'{c} ({position})'
        cvzone.putTextRect(im, text, (x1, y1), 1, 1)
        
        # Text-to-speech using gTTS
        tts = gTTS(text=f'{c} on the {position}', lang='en')
        tts.save("label.mp3")
        os.system("mpg321 label.mp3")


cv2.destroyAllWindows()
