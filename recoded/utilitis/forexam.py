

import cv2
import numpy as np
from utilitis.functions import *

def image_process(img):

    opencv = 1

    # Create a copy of the image and an empty mask with the same shape 
    original = img.copy()
    mask_for_contours = np.zeros(img.shape, dtype=np.uint8)
    mask_for_corners = mask_for_contours.copy()

    # Gaussian blur and Draw edges in the image
    blur = cv2.GaussianBlur(img, (7, 7), 0)
    edge = cv2.Canny(blur, 10, 150)
    # Make edges more pronounced
    kernel = np.ones((3, 3), np.uint8)
    dilation = cv2.dilate(edge, kernel, iterations=1)

    # Gets the biggest contour(outline)
    contours = cv2.findContours(
        dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    area_thresh= 0
    for c in contours:
        area = cv2.contourArea(c)
        if area > area_thresh:
            area_thresh = area 
            big_contour = c

    # Aproximating biggest contour with a polygone
    epsilon = 0.03*cv2.arcLength(big_contour,True)
    approx = cv2.approxPolyDP(big_contour,epsilon,True)
    cv2.drawContours(mask_for_contours, [approx], 0, (255,255,255), 3)
    cv2.drawContours(img, [approx], 0, (255,255,255), 3)


    # Gets the position of the verticies of that contour
    mask_for_contours = cv2.cvtColor(mask_for_contours, cv2.COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(
        mask_for_contours, maxCorners=4, qualityLevel=0.05, minDistance=150)
    corners = np.squeeze(corners)
    for corner in corners:
        x, y = corner
        cv2.circle(img, (int(x), int(y)), 5, (255, 120, 255), -1)
        cv2.circle(mask_for_corners, (int(x), int(y)), 5, (255, 120, 255), -1)
    # Orders the points from top left to bottom right
    ordered_corners = sort_points(corners)


    # Perspective transform -> birds eye view of the section we want
    pts1 = np.float32([ordered_corners[0][0], ordered_corners[0][1],
                    ordered_corners[1][0], ordered_corners[1][1]])
    pts2 = np.float32([[0, 0], [525, 0],
                    [0, 500], [525, 500]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    cropped = cv2.warpPerspective(original, matrix, (525, 500))
    cropped_copy = cropped.copy()
    gray_cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    cropped_hsv = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)

    
    # Threshold to see only the black lines, and fill in chopped areas
    _, result_thresh = cv2.threshold(gray_cropped, 140, 255, cv2.THRESH_BINARY_INV)
    mask1 = cv2.inRange(cropped_hsv, (120, 20, 50), (255, 255, 255))
    mask2 = cv2.inRange(cropped_hsv, (0, 20, 50), (20, 255, 255))
    thresh2 = mask1 | mask2
    result_tresh =  cv2.bitwise_not(thresh2) & result_thresh
    kernel = np.ones((20, 20), np.uint8)
    dilated2 = cv2.dilate(result_tresh, kernel, iterations=1)
    eroded2 = cv2.erode(dilated2, kernel, iterations=1)


    # Get the contours in the image, get the rectangle around each countour and keep only the ones with the correct area
    contours_in_cropped, _ = cv2.findContours(
        eroded2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    unordered_boxes = []
    for i in range(len(contours_in_cropped)):
        c = contours_in_cropped[i]
        x, y, w, h = cv2.boundingRect(c)
        area = w*h
        if (area > 2300 and area < 6000):
            unordered_boxes.append([x, y, w, h])
            cv2.rectangle(cropped, (x, y), (x+w, y+h), (0, 255, 0), 1)

    # order the rectangels and creare the list of square slices that are sliced from cropped_hsv
    sorted_boxes = []
    boxes = []
    for row in sort_boxes(unordered_boxes):
        for box in row:
            sorted_boxes.append(box)
            x, y, w, h = box
            boxes.append(cropped_hsv[y:y+h, x:x+w])
            cv2.rectangle(cropped, (x, y), (x+w, y+h), (0, 255, 0), 1)
    # get center point status - creats dictionary that associates each middle cordinate of squares
    # with the movments its allowed to do e.g. east,west,north,south
    status = get_center_points_status(boxes)

    # generate graph - uses status to create a dictionary in wich
    # each corner point is associated with other corner points it can reach
    points = generate_points(6, 6)
    graph = generate_graph(points, status)



    # show images opencv
    if (opencv != 0):
        if (opencv == 1 or opencv == 2):
            cv2.imshow("original", original)
            cv2.imshow("edge", edge)
            cv2.imshow("mask_for_contours", mask_for_contours)
            cv2.imshow("mask_for_corners", mask_for_corners)
            cv2.imshow("image", img)
            cv2.imshow("cropped", cv2.resize(cropped_copy, (0, 0), fx=0.7, fy=0.7))
        if (opencv == 1 or opencv == 3):
            cv2.imshow("cropped", cv2.resize(cropped_copy, (0, 0), fx=0.7, fy=0.7))
            cv2.imshow("result_tresh", cv2.resize(
                result_tresh, (0, 0), fx=0.7, fy=0.7))
            cv2.imshow("end_result", cv2.resize(cropped, (0, 0), fx=0.7, fy=0.7))
            cv2.imshow("dsadasda", eroded2)
            cv2.imshow("dasdas", dilated2)
            #cv2.imshow("square", get_square())


    # close window if you press a key
    return graph