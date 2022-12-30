import cv2
import numpy as np
from imutils import contours as cont

def sort_contours(contours=[]):
    for c in contours:
        area = cv2.contourArea(c)
        if (area>100 and area<60000):
            valid_area_contours.append(c)

    (cnts, _) = cont.sort_contours(valid_area_contours, method="top-to-bottom")

    # Take each row of 6 and sort from left-to-right
    row = []
    ordered=[]
    for (i, c) in enumerate(cnts, 1):
        row.append(c)
        if i % 6 == 0:  
            (cnts, _) = cont.sort_contours(row, method="left-to-right")
            ordered.append(cnts)
            row = []
    return ordered

# Load image, Gaussian blur, convert to hsv
img = cv2.imread("assets/20221229125134.jpg")
original = img.copy()
mask = np.zeros(img.shape, dtype=np.uint8)

#draws edges in the image 
blur = cv2.GaussianBlur(img, (7,7), 0)
edge = cv2.Canny(blur, 10, 150)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#make edges more pronounced
kernel = np.ones((7,7),np.uint8)
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
"""
#gets the coordinates of the verticies   
mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
corners = cv2.goodFeaturesToTrack(mask, maxCorners=4, qualityLevel=0.01, minDistance=150)
for corner in corners:
    x,y = corner.ravel()
    cv2.circle(img,(int(x),int(y)),8,(255,120,255),-1)
    cv2.circle(mask,(int(x),int(y)),8,(255,120,255),-1)
    print("({}, {})".format(x,y))

#perspective transform -> birds eye view of the section we want
pts1 = np.float32([corners[3], corners[2],
                    corners[1], corners[0]])
pts2 = np.float32([[0, 0], [525, 0],
                    [0, 500], [525, 500]])
matrix=cv2.getPerspectiveTransform(pts1,pts2)
cropped = cv2.warpPerspective(img,matrix,(525,500 ))
gray_cropped = cv2.cvtColor(cropped,cv2.COLOR_BGR2GRAY)

#detect squares inside the grid
_,result_tresh =cv2.threshold(gray_cropped,50,255,cv2.THRESH_BINARY_INV)
kernel = np.ones((3,3),np.uint8)
dilated2 = cv2.dilate(result_tresh,kernel,iterations = 1)

#shape of maze
width = 6
height=6

#seperate image to boxes
valid_area_contours=[]
contours_of_squares,_ = cv2.findContours(dilated2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
sorted_contours = sort_contours(contours_of_squares)
boxes =[]
# Draw text
for i in range (36):
    rows,columns = i%6,i//6 
    c = sorted_contours[rows][columns]
    x,y,w,h = cv2.boundingRect(c)
    cv2.rectangle(cropped,(x,y),(x+w,y+h),(0,255,0),2)
    boxes.append(cropped[y:y+h,x:x+w])
"""
#show all images
cv2.imshow("edge", dilation)
#cv2.imshow("result_tresh", result_tresh)
cv2.imshow("image", img)
#cv2.imshow("image2", cropped)
#close window if you press a key
cv2.waitKey(0)
cv2.destroyAllWindows()