import cv2
from picamera2 import Picamera2
import pandas as pd
from ultralytics import YOLO
import cvzone
import numpy as np
from gtts import gTTS
import os

# Initialize Picamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (320, 240)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# Load YOLO models and class lists
model1 = YOLO('yolov8n.pt')
model2 = YOLO('/home/anuj/model/best.pt')

my_file1 = open("coco.txt", "r")
data1 = my_file1.read()
class_list1 = data1.split("\n")

my_file2 = open("coconew.txt", "r")
data2 = my_file2.read()
class_list2 = data2.split("\n")

count = 0

while True:
    im = picam2.capture_array()
    
    count += 1
    if count % 3 != 0:
        continue
    
    # Choose which model to use
    if count % 2 == 0:
        model = model1
        class_list = class_list1
    else:
        model = model2
        class_list = class_list2
    
    results = model.predict(im)
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")
    
    for index, row in px.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])
        c = class_list[d]
        
        cv2.rectangle(im, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cvzone.putTextRect(im, f'{c}', (x1, y1), 1, 1)
        
        # Determine position
        frame_width = im.shape[1]
        object_center = (x1 + x2) // 2
        
        if object_center < frame_width // 3:
            position = "left"
        elif object_center < 2 * frame_width // 3:
            position = "middle"
        else:
            position = "right"
        
        # Text-to-Speech
        tts = gTTS(text=f'{c} on the {position}', lang='en')
        tts.save("label.mp3")
        os.system("mpg321 label.mp3")
        
cv2.destroyAllWindows()
