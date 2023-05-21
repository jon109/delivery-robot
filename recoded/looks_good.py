import cv2
import numpy as np
import requests
from utilitis.process import *
from utilitis.shortest_path_1 import *
from utilitis.http_functions import *
#from utilitis.manim_class import * 
import serial
import imutils
import time

# visuals control
# opencv - 0(dont show anything), 1(show everythng), 2(show first half, until cropped), 3(show only second half from cropped until end)
opencv = 1
# manim - 0(don't use manim), 1(only image of graph), 2(only animation of showing the solution)
manim = 0
# side_by_side show image of graph of manim next to cropped
# you must!!!! set opencv and manim to 0
side_by_side = False
# print_graph - print the graph to console true/flase
print_graph = True
#allow maze debugging
maze_debbuger = False

# Android-Cam IP
url = "http://192.168.20.21:8080/shot.jpg"

#please set correct starting position
position = [0,0]
destination = [0,0]
# 0 - north, 90 - right, 180 - south, 270 - left
currentDirection = 180
# Set end to 0 - will run
post('end','end',0)


# Start bluetooth communication
print("connecting to hc-06...")
# Set up serial connection
ser = serial.Serial(
    port="COM7",  # The port hc-06 is connected to
    baudrate=9600, 
)
# Sends s (stands for start) to waits for an acknowledge from arduino
ser.write(b's')
while (ser.in_waiting == 0):
    pass
response = ser.read().decode('ascii').rstrip()
if (response == 'k'):
    print("bluetooth connection successful")
else:
    print("bluetooth connection failed")

#wait until get graph button pressed
get_graph = 0
img = None
while (get_graph==0):
    get_graph = get('get_graph','get_graph')
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    img = cv2.resize(img, (0, 0), fx=500/img.shape[1], fy=500/img.shape[1])
    cv2.imshow('Live_window', img)
    cv2.waitKey(1)
cv2.destroyAllWindows()

#get the graph
graph, cropped =  image_process(img, opencv, print_graph, maze_debbuger)

#in case there was an error in the image_proccesing
if (graph==-1):
    cv2.waitKey(0)
    cv2.destroyAllWindows()
while (graph ==-1):
    get_graph = get('get_graph','get_graph')
    while (get_graph==0):
        get_graph = get('get_graph','get_graph')
        img = cv2.imread(r"C:\Users\jonat\opencv\assets\fromphone.jpeg")
        img = cv2.resize(img, (0, 0), fx=400/img.shape[1], fy=400/img.shape[1])
        cv2.imshow('Live_window', img)
        cv2.waitKey(1)
    cv2.destroyAllWindows()
    graph, cropped =  image_process(img, opencv, print_graph, maze_debbuger)

# Set state to 1 - app will be able to send data
post('state','state',1)
while True:
    key=cv2.waitKey(1)
    if (key ==27):
        cv2.destroyAllWindows()
    destination[0],destination[1], end = wait_for_destination()
    if (end==1):
        break
    print(f'The retrieved destination is ({destination[0]}, {destination[1]})')
    # Set the state to 0 - cannot send destenation now
    post('state','state',0)
    shortest_path = bfs(graph, position, destination)
    directions, currentDirection = moveSequence(position, currentDirection, shortest_path, destination)
    shortest_path.insert(0,(position[0],position[1]))
    #run_manim(cropped, graph, shortest_path, manim, side_by_side, opencv)
    print(directions)    

    # Send the directions thorugh bluetooth to the arduino
    length = bytes([len(directions)])
    ser.write(length)
    for i in range(len(directions)):
        ser.write(bytes([abs(directions[i])]))
        ser.write(b'1' if directions[i] > 0 else b'0')
    
    #wait for arduino to send a confirmation that it has finished the course
    while (ser.in_waiting == 0):
        pass
    response = ser.read().decode('ascii').rstrip()
    if (response == 'g'):
        print("robot finisehd the track")
        # Set state to 1 - let app send new destenation
        post('state','state',1)
    position = destination.copy()  
ser.close()