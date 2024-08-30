import cv2 
import pytesseract
from picamera.array import PiRGBArray
from picamera2 import PiCamera2

camera = PiCamera2()
camera.resolution = (320, 240)
camera.framerate = 30

rawCapture = PiRGBArray(camera, size=(640, 480))

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	image = frame.array
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
	
	rawCapture.truncate(0)

	if key == ord("s"):
		text = pytesseract.image_to_string(image)
		print(text)
		cv2.imshow("Frame", image)
		cv2.waitKey(0)
		break

cv2.destroyAllWindows()