import cv2
from picamera2 import Picamera2
import pandas as pd
from ultralytics import YOLO
import cvzone
import numpy as np
from gtts import gTTS
import os
from tkinter import *
from search import info
import threading

class Application:
    def __init__(self):
        self.win = Tk()
        self.win.geometry('320x50')
        self.win.title('Freedomtech Player')
        self.button = Button(self.win, text="Speak", command=self.switch_mode)
        self.button.pack()
        self.mode = "speak"
        self.picam2 = Picamera2()
        self.picam2.preview_configuration.main.size = (320, 240)
        self.picam2.preview_configuration.main.format = "RGB888"
        self.picam2.preview_configuration.align()
        self.picam2.configure("preview")
        self.model = YOLO('yolov8n.pt')
        self.my_file = open("coco.txt", "r")
        self.data = self.my_file.read()
        self.class_list = self.data.split("\n")
        self.count = 0

    def object_detection(self):
        self.picam2.start()
        while True:
            im = self.picam2.capture_array()
            self.count += 1
            if self.count % 3 != 0:
                continue
            results = self.model.predict(im)
            a = results[0].boxes.data
            px = pd.DataFrame(a).astype("float")
            for index, row in px.iterrows():
                x1 = int(row[0])
                y1 = int(row[1])
                x2 = int(row[2])
                y2 = int(row[3])
                d = int(row[5])
                c = self.class_list[d]
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
            if cv2.waitKey(1) == ord('q') or self.mode == "speak":
                break
        cv2.destroyAllWindows()
        self.picam2.stop()

    def switch_mode(self):
        if self.mode == "speak":
            self.button.config(text="Object Detection")
            self.mode = "object_detection"
            threading.Thread(target=self.object_detection).start()
        else:
            self.button.config(text="Speak")
            self.mode = "speak"
            info()

    def run(self):
        self.win.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()
