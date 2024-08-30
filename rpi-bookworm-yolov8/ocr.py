import easyocr
from gtts import gTTS
from PIL import Image
import os
import re
from picamera2 import Picamera2

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Initialize Picamera2
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()

# Capture image from camera
frame = picam2.capture_array()
picam2.stop()

# Save the captured image
image_path = 'captured_image.jpg'
Image.fromarray(frame).save(image_path)

# Perform OCR using EasyOCR
result = reader.readtext(image_path, detail=0, allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')

# Combine text into a single string
text_comb = ' '.join(result)

# Use regex to keep only a-z and A-Z characters
filtered_text = re.sub(r'[^a-zA-Z\s]', '', text_comb)

print(filtered_text)

# Convert text to speech
sound = gTTS(filtered_text)
sound.save('trans.mp3')

# Play the audio using mpg321 (install with: sudo apt-get install mpg321)
os.system('mpg321 trans.mp3')
