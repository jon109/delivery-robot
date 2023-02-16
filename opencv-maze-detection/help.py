
import cv2
import numpy as np
from functions import *

# Load image, Gaussian blur, convert to hsv
cropped = cv2.imread("assets/grid_with_obsticle.png")
cropped_hsv = cv2.cvtColor(cropped,cv2.COLOR_BGR2HSV)
original = cropped.copy()

gray_cropped = cv2.cvtColor(cropped,cv2.COLOR_BGR2GRAY)

#detect squares inside the grid
_,result_tresh =cv2.threshold(gray_cropped,50,255,cv2.THRESH_BINARY_INV)
kernel = np.ones((30,30),np.uint8)
dilated2 = cv2.dilate(result_tresh,kernel,iterations = 1)
kernel = np.ones((30,30),np.uint8)
eroded= cv2.erode(dilated2,kernel,iterations=1)

#shape of maze
width = 6
height=6
cropped_of_cropped = 6

#seperate image to boxes
contours,_ = cv2.findContours(eroded, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
unordered_boxes = []
for i in range (len(contours)):
    c = contours[i]
    x,y,w,h = cv2.boundingRect(c)
    area = w*h
    if (area> 3000 and area <6000):
        unordered_boxes.append([x,y,w,h])
        print(i)

boxes=[]
for row in sort_boxes(unordered_boxes):
    for box in row:
        x,y,w,h = box
        boxes.append(cropped_hsv[y:y+h,x:x+w])
        cv2.rectangle(cropped,(x,y),(x+w,y+h),(0,255,0),1)

#each 
status = get_center_points_status(boxes)
points = generate_points(6,6)
graph = generate_graph(points,status)
print(graph)

#show all images
cv2.imshow("result_tresh", eroded)
cv2.imshow("image2", cropped)
#close window if you press a key
cv2.waitKey(0)
cv2.destroyAllWindows()