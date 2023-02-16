
import cv2
import numpy as np
from functions import *
from manim_class import *
from shortest_path_1 import *
import serial
import time
import requests

# ESP32 URL
URL = "http://192.168.16.73"
AWB = True

# visuals control
# opencv - 0(dont show anything), 1(show everythng), 2(show first half, until cropped), 3(show only second half from cropped until end)
opencv = 1
# manim - 0(don't use manim), 1(only image of graph), 2(only animation of showing the solution)
manim = 0
# side_by_side show image of graph of manim next to cropped
# you must!!!! set opencv and manim to 0
side_by_side = False
# print_graph - print the graph to console true/flase
print_graph = False


# shape of maze
run = True
width = 6
height = 6
position = [0, 5]
goal = [6, 0]
currentDirection = 0

# start bluetooth communication
print("connecting to hc-06...")
# Set up serial connection
ser = serial.Serial(
    port="COM7",  # the port hc-06 is connected to
    baudrate=9600,  # Replace with the correct baud rate
)
# sends s (stands for start) to waits for an acknowledge from arduino
ser.write(b's')
while (ser.in_waiting == 0):
    pass
response = ser.read().decode('ascii').rstrip()
if (response == 'k'):
    print("bluetooth connection successful")
else:
    print("bluetooth connection failed")

while True:
    # waits for arduino to ask for directions
    #time.sleep(1)
    while (ser.in_waiting == 0):
        pass
    response = ser.read().decode('ascii').rstrip()
    # d stands for directions
    if (response == 'd'):
        # Load image: Face recognition and opencv setup
        cap = cv2.VideoCapture(URL + ":81/stream")
        r = 0
        while (not cap.isOpened()): 
            r += 1
        ret, img = cap.read()

        # Gaussian blur, convert to hsv
        img = cv2.resize(img, (0, 0), fx=0.3, fy=0.3)
        original = img.copy()
        mask_for_contours = np.zeros(img.shape, dtype=np.uint8)
        mask_for_corners = mask_for_contours.copy()

        # draws edges in the image
        blur = cv2.GaussianBlur(img, (7, 7), 0)
        edge = cv2.Canny(blur, 10, 150)
        # make edges more pronounced
        kernel = np.ones((5, 5), np.uint8)
        dilation = cv2.dilate(edge, kernel, iterations=1)

        # gets the biggest contour(outline)
        contours = cv2.findContours(
            dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]
        area_thresh= 0
        for c in contours:
            area = cv2.contourArea(c)
            if area > area_thresh:
                area_thresh = area 
                big_contour = c

        #aproximating biggest contour with a polygon
        epsilon = 0.05*cv2.arcLength(big_contour,True)
        approx = cv2.approxPolyDP(big_contour,epsilon,True)
        cv2.drawContours(mask_for_contours, [approx], 0, (255,255,255), 3)
        cv2.drawContours(img, [approx], 0, (255,255,255), 3)

        # gets the position of the verticies of that contour
        mask_for_contours = cv2.cvtColor(mask_for_contours, cv2.COLOR_BGR2GRAY)
        corners = cv2.goodFeaturesToTrack(
            mask_for_contours, maxCorners=4, qualityLevel=0.1, minDistance=150)
        corners = np.squeeze(corners)
        for corner in corners:
            x, y = corner
            cv2.circle(img, (int(x), int(y)), 5, (255, 120, 255), -1)
            cv2.circle(mask_for_corners, (int(x), int(y)), 5, (255, 120, 255), -1)
            print("({}, {})".format(x, y))
        ordered_corners = sort_points(corners)

        # perspective transform -> birds eye view of the section we want
        pts1 = np.float32([ordered_corners[0][0], ordered_corners[0][1],
                        ordered_corners[1][0], ordered_corners[1][1]])
        pts2 = np.float32([[0, 0], [525, 0],
                        [0, 500], [525, 500]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        cropped = cv2.warpPerspective(original, matrix, (525, 500))
        cropped_copy = cropped.copy()
        gray_cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        cropped_hsv = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)


        # treshold to see only the black lines, and fill in chopped areas
        _, result_tresh = cv2.threshold(gray_cropped, 100, 255, cv2.THRESH_BINARY_INV)
        kernel = np.ones((20, 20), np.uint8)
        mask1 = cv2.inRange(cropped_hsv, (170, 70, 50), (180, 255, 255))
        mask2 = cv2.inRange(cropped_hsv, (0, 70, 50), (10, 255, 255))
        thresh2 = mask1 | mask2
        result_tresh =  cv2.bitwise_not(thresh2) & result_tresh
        dilated2 = cv2.dilate(result_tresh, kernel, iterations=1)
        eroded2 = cv2.erode(dilated2, kernel, iterations=1)
        # get the contours in the image, get the rectangle around each countour and keep only the ones with the correct area
        contours_in_cropped, _ = cv2.findContours(
            eroded2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        unordered_boxes = []
        for i in range(len(contours_in_cropped)):
            c = contours_in_cropped[i]
            x, y, w, h = cv2.boundingRect(c)
            area = w*h
            if (area > 2000 and area < 6000):
                unordered_boxes.append([x, y, w, h])
                #cv2.rectangle(cropped, (x, y), (x+w, y+h), (0, 255, 0), 1)
        # order the rectangels and creare the list of square slices that are sliced from cropped_hsv
        boxes = []
        for row in sort_boxes(unordered_boxes):
            for box in row:
                x, y, w, h = box
                boxes.append(cropped_hsv[y:y+h, x:x+w])
                cv2.rectangle(cropped, (x, y), (x+w, y+h), (0, 255, 0), 1)

        # get center point status - creats dictionary that associates each middle cordinate of squares
        # with the movments its allowed to do e.g. east,west,north,south
        status = get_center_points_status(boxes)
        points = generate_points(6, 6)
        # generate graph - uses status to create a dictionary in wich
        # each corner point is associated with other corner points it can reach
        graph = generate_graph(points, status)

        #get the shortest path and translate results so arduino can understand them
        shortest_path = bfs(graph, position, goal)
        directions, currentDirection, position = moveSequence(position, currentDirection, shortest_path, goal)

        print(directions)

        # send the directions thorugh bluetooth to the arduino
        # length = ''
        length = bytes([len(directions)])
        ser.write(length)
        for i in range(len(directions)):
            ser.write(bytes([abs(directions[i])]))
            ser.write(b'1' if directions[i] > 0 else b'0')

        # visualizations and debugging
        # print the graph
        if (print_graph):
            for key, value in graph.items():
                print(key, ' : ', value)

        # manim
        if (manim != 0):
            scene = hello(graph, manim)
            scene.render()
            if (manim == 1):
                open_media_file('media\images\hello_ManimCE_v0.17.2.png')
            if (manim == 2):
                open_media_file("media\\videos\\1080p60\hello.mp4")

        # show images opencv
        if (opencv != 0):
            if (opencv == 1 or opencv == 2):
                cv2.imshow("original", original)
                cv2.imshow("edge", edge)
                cv2.imshow("mask_for_contours", mask_for_contours)
                cv2.imshow("mask_for_corners", mask_for_corners)
                cv2.imshow("image", img)
                cv2.imshow("cropped", cv2.resize(
                    cropped_copy, (0, 0), fx=0.7, fy=0.7))
            if (opencv == 1 or opencv == 3):
                cv2.imshow("cropped", cv2.resize(
                    cropped_copy, (0, 0), fx=0.7, fy=0.7))
                cv2.imshow("result_tresh", cv2.resize(
                    result_tresh, (0, 0), fx=0.7, fy=0.7))
                cv2.imshow("end_result", cv2.resize(
                    cropped, (0, 0), fx=0.7, fy=0.7))
                cv2.imshow("square", get_square())

        if (side_by_side and opencv == 0 and manim == 0):
            cv2.imshow("cropped", cv2.resize(cropped_copy, (0, 0), fx=1, fy=1))
            scene = hello(graph, 1)
            scene.render()
            open_media_file('media\images\hello_ManimCE_v0.17.2.png')

        cv2.waitKey(0)
        cv2.destroyAllWindows()
