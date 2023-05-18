import cv2
import numpy as np
from utilitis.process import *
from utilitis.shortest_path_1 import *

# ESP32 URL

img = cv2.imread(r"C:\Users\jon\mystuff\opencv-test\assets\fromphone.jpeg")
img = cv2.resize(img, (0, 0), fx=600/img.shape[1], fy=600/img.shape[1])

while True:
        graph,_ =image_process(img, 1, True, False)
        shortest_path = bfs(graph, [6,0], [0,6])
        print(shortest_path)
        print(graph)
        key=cv2.waitKey(0)
        if key==ord('q'):
            break
    
cv2.destroyAllWindows()