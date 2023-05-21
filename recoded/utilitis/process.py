import cv2
import numpy as np
from utilitis.functions import *

def image_process(img, opencv = 1, print_graph= False, maze_debbuger= False):

    # Load image, Gaussian blur, convert to hsv
    original = img.copy()
    mask_for_contours = np.zeros(img.shape, dtype=np.uint8)
    mask_for_corners = mask_for_contours.copy()

    # Draw edges in the image
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
        #print("({}, {})".format(x, y)) #to print cords of the points
    if (len(corners) != 4):
        cv2.imshow("original image", original)
        cv2.imshow("edges", edge)
        cv2.imshow("dilation of edges", dilation )
        cv2.imshow("biggest contour", mask_for_contours)
        cv2.imshow("corners", mask_for_corners)
        cv2.imshow("image with corners and contour", img)
        cv2.moveWindow("original image",0 ,0)
        cv2.moveWindow("edges",0,img.shape[0])
        cv2.moveWindow("dilation of edges",0,2*img.shape[0])
        cv2.moveWindow("biggest contour",400 ,0)
        cv2.moveWindow("corners",400,img.shape[0])
        cv2.moveWindow("image with corners and contour",400,2*img.shape[0])
        print("couldn't find the 4 corners, possible problems are:\n1. not all 4 points are in frame\n2. edges of square got mixed up with other objects\n3. check for light from windows\n")
        return -1, -1
    # Orders the points from top left to bottom right
    ordered_corners = sort_points(corners)


    # Perspective transform -> birds eye view of the section we want
    pts1 = np.float32([ordered_corners[0][0], ordered_corners[0][1],
                    ordered_corners[1][0], ordered_corners[1][1]])
    pts2 = np.float32([[0, 0], [525, 0],
                    [0, 500], [525, 500]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    cropped = cv2.warpPerspective(original, matrix, (525, 500))
    cropped = cv2.resize(cropped, (0, 0), fx=img.shape[1]/cropped.shape[1], fy=img.shape[1]/cropped.shape[1])
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
    
   
    if (len(unordered_boxes) != 36):
        cv2.imshow("original image",original)
        cv2.imshow("image with corners and contour",img)
        cv2.imshow("cropped image",cropped)
        cv2.imshow("threshold before dilation and erosion",result_tresh)
        cv2.imshow("after dilation",dilated2)
        cv2.imshow("after erosion",eroded2)
        cv2.imshow("edges", edge)
        cv2.imshow("dilation of edges", dilation )
        cv2.imshow("biggest contour", mask_for_contours)
        cv2.imshow("corners", mask_for_corners)
        cv2.moveWindow("original image",0 ,0)
        cv2.moveWindow("image with corners and contour",0,img.shape[0])
        cv2.moveWindow("threshold before dilation and erosion",0,2*img.shape[0])
        cv2.moveWindow("after dilation",400 ,0)
        cv2.moveWindow("after erosion",400,cropped.shape[0]+40)
        cv2.moveWindow("edges",800 ,0)
        cv2.moveWindow("edges",800,img.shape[0])
        cv2.moveWindow("dilation of edges",800,2*img.shape[0])
        cv2.moveWindow("biggest contour",1200 ,0)
        cv2.moveWindow("corners",1200,img.shape[0])
        print("couldn't recognize 36 squares, here are some problems that can occur:\n1. was able to recognize 4 points, but they are bad\n2. dilation might have amplified noise")
        print("if it is a corner problem please check the following:\n1. not all 4 points are in frame\n2. edges of square got mixed up with other objects\n3. check for light from windows\n")
        return -1,-1
    
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
    if (maze_debbuger == True):
        maze_debug(cropped_copy,sorted_boxes,status)

    points = generate_points(6, 6)
    # generate graph - uses status to create a dictionary in wich
    # each corner point is associated with other corner points it can reach
    graph = generate_graph(points, status)

    #visualizations and debugging
    # print the graph
    if (print_graph):
        for key, value in graph.items():
            print(key, ' : ', value)


    # show images opencv
    if (opencv != 0):
        if (opencv == 1 or opencv == 2):
            cv2.imshow("original", original)
            cv2.imshow("edge", edge)
            cv2.imshow("mask_for_contours", mask_for_contours)
            cv2.imshow("mask_for_corners", mask_for_corners)
            cv2.imshow("image", img)
            cv2.imshow("cropped", cropped_copy)
            cv2.moveWindow("original",0 ,0)
            cv2.moveWindow("edge",0,img.shape[0])
            cv2.moveWindow("mask_for_contours",0,2*img.shape[0])
            cv2.moveWindow("mask_for_corners",400 ,0)
            cv2.moveWindow("image",400,img.shape[0])
            cv2.moveWindow("cropped",400,2*img.shape[0])
        if (opencv == 1 or opencv == 3):
            cv2.imshow("cropped", cropped_copy)
            cv2.imshow("result_tresh", result_tresh)
            cv2.imshow("eroded", eroded2)
            cv2.imshow("dilated", dilated2)
            cv2.imshow("square", get_square())
            cv2.imshow("end_result", cropped)
            cv2.moveWindow("cropped",400,2*img.shape[0])
            cv2.moveWindow("result_tresh",800 ,0)
            cv2.moveWindow("dilated",800,cropped.shape[0]+40)
            cv2.moveWindow("eroded",1200,0)
            cv2.moveWindow("end_result",1200 ,cropped.shape[0]+40)
            cv2.moveWindow("square",1650 ,cropped.shape[0]//2)
    return graph, cropped_copy