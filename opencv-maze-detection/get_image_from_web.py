import cv2
import numpy as np
import requests

# ESP32 URL

URL = "http://192.168.16.73"

# Face recognition and opencv setup
cap = cv2.VideoCapture(URL + ":81/stream")

while True:
    if cap.isOpened():
        ret, frame = cap.read()

        cv2.imshow("frame", frame)
        
        key=cv2.waitKey(5)
        if key==ord('q'):
            break
    
cv2.destroyAllWindows()