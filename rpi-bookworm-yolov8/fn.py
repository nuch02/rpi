import cv2
from picamera2 import Picamera2
import pandas as pd
from ultralytics import YOLO
import cvzone
import numpy as np
from gtts import gTTS
import os
import threading

# Global flag to control detection
detection_running = True

# Function to perform object detection and text-to-speech
def detect_and_speak():
    global detection_running
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (320, 240)  # Reduced resolution
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("preview")
    picam2.start()

    model = YOLO('yolov8n.pt')  # Ensure this is a lightweight model

    with open("coco.txt", "r") as my_file:
        class_list = my_file.read().split("\n")

    count = 0

    while detection_running:
        im = picam2.capture_array()
        
        count += 1
        if count % 6 != 0:  # Process every 6th frame
            continue
        
        results = model.predict(im)
        a = results[0].boxes.data
        px = pd.DataFrame(a).astype("float")
        
        for index, row in px.iterrows():
            x1, y1, x2, y2, _, d = map(int, row[:6])
            c = class_list[d]
            
            cv2.rectangle(im, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cvzone.putTextRect(im, f'{c}', (x1, y1), 1, 1)
            
            frame_width = im.shape[1]
            object_center = (x1 + x2) // 2
            
            if object_center < frame_width // 3:
                position = "left"
            elif object_center < 2 * frame_width // 3:
                position = "middle"
            else:
                position = "right"
            
            tts = gTTS(text=f'{c} on the {position}', lang='en')
            tts.save("label.mp3")
            os.system("mpg321 label.mp3")
            
        cv2.imshow("Camera", im)
        if cv2.waitKey(1) == ord('q'):
            break

    picam2.stop()
    cv2.destroyAllWindows()

# Function to start the detection in a separate thread
def start_detection():
    detection_thread = threading.Thread(target=detect_and_speak)
    detection_thread.daemon = True
    detection_thread.start()

# Start detection in the background
start_detection()
