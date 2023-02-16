import cv2
import numpy as np

# Load image, Gaussian blur, convert to hsv
img = cv2.imread("assets/20221229125145.jpg")
original = img.copy()
mask = np.zeros(img.shape, dtype=np.uint8)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
_,tresh =cv2.threshold(gray,30,255,cv2.THRESH_BINARY_INV)
kernel = np.ones((4,4),np.uint8)
dilation = cv2.dilate(tresh,kernel,iterations = 1)

contours = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]
for c in contours:
    
    area_thresh = 0
    area = cv2.contourArea(c)
    if area > area_thresh:
        area = area_thresh
        big_contour = c
cv2.drawContours(img, [big_contour], 0, (255,255,255), 1)
#cv2.drawContours(mask, [big_contour], 0, (255,255,255), 3)
"""
mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
corners = cv2.goodFeaturesToTrack(mask, maxCorners=4, qualityLevel=0.1, minDistance=150)
for corner in corners:
    x,y = corner.ravel()
    cv2.circle(img,(int(x),int(y)),8,(255,120,255),-1)
    cv2.circle(mask,(int(x),int(y)),8,(255,120,255),-1)
    print("({}, {})".format(x,y))
"""

epsilon = 0.1*cv2.arcLength(big_contour,True)
approx = cv2.approxPolyDP(big_contour,epsilon,True)
cv2.drawContours(mask, [approx], 0, (255,255,255), 3)
cv2.drawContours(img, [approx], 0, (255,255,255), 3)

mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
corners = cv2.goodFeaturesToTrack(mask, maxCorners=4, qualityLevel=0.1, minDistance=0)
for corner in corners:
    x,y = corner.ravel()
    cv2.circle(img,(int(x),int(y)),8,(255,120,255),-1)
    cv2.circle(mask,(int(x),int(y)),8,(255,120,255),-1)
    print("({}, {})".format(x,y))

pts1 = np.float32([corners[3], corners[2],
                    corners[1], corners[0]])
pts2 = np.float32([[0, 0], [525, 0],
                    [0, 500], [525, 500]])
matrix=cv2.getPerspectiveTransform(pts1,pts2)
result = cv2.warpPerspective(original,matrix,(525,500 ))

#show all images
cv2.imshow("yo",result)
cv2.imshow("bold",dilation)
cv2.imshow("tresh",tresh)
cv2.imshow("image", img)

#close window if you press a key
cv2.waitKey(0)
cv2.destroyAllWindows()