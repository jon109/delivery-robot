import cv2
import numpy as np

# Load image, Gaussian blur, convert to hsv
img = cv2.imread("assets/square.jpg")
original = img.copy()
mask = np.zeros(img.shape, dtype=np.uint8)
blur = cv2.GaussianBlur(img, (3,3), 0)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#mask for colors between the range  (60, 100, 20) -> (130, 360, 255)
thresh = cv2.inRange(hsv,(60, 100, 20), (130, 360, 255) )

#apply morphology -> removes noise from mask
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

#gets the biggest contour(outline)
contours = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]
for c in contours:
    area_thresh = 0
    area = cv2.contourArea(c)
    if area > area_thresh:
        area = area_thresh
        big_contour = c

#aproximates the contour with a 4 sided polygon
epsilon = 0.1*cv2.arcLength(big_contour,True)
approx = cv2.approxPolyDP(big_contour,epsilon,True)
cv2.drawContours(mask, [approx], 0, (255,255,255), 3)
cv2.drawContours(img, [approx], 0, (255,255,255), 3)

#gets the coordinates of the verticies   
mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
corners = cv2.goodFeaturesToTrack(mask, maxCorners=4, qualityLevel=0.5, minDistance=150)
for corner in corners:
    x,y = corner.ravel()
    cv2.circle(img,(int(x),int(y)),8,(255,120,255),-1)
    cv2.circle(mask,(int(x),int(y)),8,(255,120,255),-1)
    print("({}, {})".format(x,y))

#perspective transform -> birds eye view
pts1 = np.float32([corners[1], corners[3],
                    corners[0], corners[2]])
pts2 = np.float32([[0, 0], [800, 0],
                    [0, 400], [800, 400]])
matrix=cv2.getPerspectiveTransform(pts1,pts2)
result = cv2.warpPerspective(img,matrix,(800,400 ))

#show all images
cv2.imshow("tresh", thresh)
cv2.imshow("opening", opening)
cv2.imshow("result", result)
cv2.imshow("image", img)

#close window if you press a key
cv2.waitKey(0)
cv2.destroyAllWindows()