
import cv2
import numpy as np
from functions import *
from manim_class import *

#shape of maze
width = 6
height=6

# Load image, Gaussian blur, convert to hsv
img = cv2.imread("assets/grid1.jpg")
original = img.copy()
mask = np.zeros(img.shape, dtype=np.uint8)

#draws edges in the image 
blur = cv2.GaussianBlur(img, (7,7), 0)
edge = cv2.Canny(blur, 10, 150)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#make edges more pronounced
kernel = np.ones((5,5),np.uint8)
dilation = cv2.dilate(edge,kernel,iterations = 1)

#gets the biggest contour(outline)
contours = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]
for c in contours:
    area_thresh = 0
    area = cv2.contourArea(c)
    if area > area_thresh:
        area = area_thresh
        big_contour = c
cv2.drawContours(img, [big_contour], 0, (255,255,255), 3)
cv2.drawContours(mask, [big_contour], 0, (255,255,255), 3)

#gets the position of the verticies of that contour  
mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
corners = cv2.goodFeaturesToTrack(mask, maxCorners=4, qualityLevel=0.01, minDistance=150)
corners = np.squeeze(corners)
for corner in corners:
    x,y = corner
    cv2.circle(img,(int(x),int(y)),5,(255,120,255),-1)
    print("({}, {})".format(x,y))
ordered_corners = sort_points(corners)

#perspective transform -> birds eye view of the section we want
pts1 = np.float32([ordered_corners[0][0], ordered_corners[0][1],
                    ordered_corners[1][0], ordered_corners[1][1]])
pts2 = np.float32([[0, 0], [525, 0],
                    [0, 500], [525, 500]])
matrix=cv2.getPerspectiveTransform(pts1,pts2)
cropped = cv2.warpPerspective(original,matrix,(525,500 ))
gray_cropped = cv2.cvtColor(cropped,cv2.COLOR_BGR2GRAY)
cropped_hsv = cv2.cvtColor(cropped,cv2.COLOR_BGR2HSV)

#treshold to see only the black lines, and fill in chopped areas
_,result_tresh =cv2.threshold(gray_cropped,50,255,cv2.THRESH_BINARY_INV)
kernel = np.ones((30,30),np.uint8)
dilated2 = cv2.dilate(result_tresh,kernel,iterations = 1)
eroded2= cv2.erode(dilated2,kernel,iterations=1)

#get the contours in the image, get the rectangle around each countour and keep only the ones with the correct area  
contours_in_cropped,_ = cv2.findContours(eroded2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
unordered_boxes = []
for i in range (len(contours_in_cropped)):
    c = contours_in_cropped[i]
    x,y,w,h = cv2.boundingRect(c)
    area = w*h
    if (area> 3000 and area <6000):
        unordered_boxes.append([x,y,w,h])
#order the rectangels and creare the list of square slices that are sliced from cropped_hsv
boxes=[]
for row in sort_boxes(unordered_boxes):
    for box in row:
        x,y,w,h = box
        boxes.append(cropped_hsv[y:y+h,x:x+w])
        cv2.rectangle(cropped,(x,y),(x+w,y+h),(0,255,0),1)

#get center point status - creats dictionary that associates each middle cordinate of squares
#with the movments its allowed to do e.g. east,west,north,south
status = get_center_points_status(boxes)
points = generate_points(6,6)
#generate graph - uses status to create a dictionary in wich
# each corner point is associated with other corner points it can reach
graph = generate_graph(points,status)
print(graph)
# visualization section
scene = hello(graph)
scene.render()
dir=config.get_dir("media_dir").as_posix()
open_media_file('media\images\hello_ManimCE_v0.17.2.png')
# end 
#show all images
cv2.imshow("image", img)
cv2.imshow("image2", cropped)
#close window if you press a key
cv2.waitKey(0)
cv2.destroyAllWindows()