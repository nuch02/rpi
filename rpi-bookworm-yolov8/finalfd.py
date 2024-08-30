import cv2
from picamera2 import Picamera2
import pandas as pd
from ultralytics import YOLO
import cvzone
import numpy as np
from gtts import gTTS
import os

picam2 = Picamera2()
picam2.preview_configuration.main.size = (320,240)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()
model=YOLO('yolov8n.pt')
my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")
count=0
while True:
    im= picam2.capture_array()
    
    count += 1
    if count % 3 != 0:
        continue
    results=model.predict(im)
    a=results[0].boxes.data
    px=pd.DataFrame(a).astype("float")
    
    
    for index,row in px.iterrows():
#        print(row)
 
        x1=int(row[0])
        y1=int(row[1])
        x2=int(row[2])
        y2=int(row[3])
        d=int(row[5])
        c=class_list[d]
        
        cv2.rectangle(im,(x1,y1),(x2,y2),(0,0,255),2)
        cvzone.putTextRect(im,f'{c}',(x1,y1),1,1)
        
        frame_width = im.shape[1]
        object_center = (x1 + x2) // 2
        
        if object_center < frame_width // 3:
            position = "left"
        elif object_center < 2 * frame_width // 3:
            position = "middle"
            os.system("mpg321 /home/anuj/raspi/rpi-bookworm-yolov8/Beep.mp3")
            os.system("mpg321 /home/anuj/raspi/rpi-bookworm-yolov8/Beep.mp3")
            os.system("mpg321 /home/anuj/raspi/rpi-bookworm-yolov8/Beep.mp3")
        else:
            position = "right"
        
        # Text-to-Speech
        tts = gTTS(text=f'{c} on the {position}', lang='en')
        tts.save("label.mp3")
        os.system("mpg321 label.mp3")
        
    cv2.imshow("Camera", im)
    if cv2.waitKey(1)==ord('q'):
        break
cv2.destroyAllWindows()
