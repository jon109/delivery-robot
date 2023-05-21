import cv2
import numpy as np
import requests
from utilitis.process import *
from utilitis.shortest_path_1 import *
from utilitis.http_functions import *
from utilitis.manim_class import *

# visuals control
# opencv - 0(dont show anything), 1(show everythng), 2(show first half, until cropped), 3(show only second half from cropped until end)
opencv = 1
# manim - 0(don't use manim), 1(only image of graph), 2(only graph and solution)
manim = 2
# side_by_side show image of graph of manim next to cropped
# you must!!!! set opencv and manim to 0
side_by_side = False
# print_graph - print the graph to console true/flase
print_graph = False
#allow maze debugging
maze_debbuger = False


#please set correct starting position
position = [0,0]
destination = [0,0]
# 0 - north, 90 - right, 180 - south, 270 - left
currentDirection = 180
# Set end to 0 - will run
post('end','end',0)

#remove em
post('get_graph', 'get_graph',1)
post('store_number','number', 12)

#wait until get graph button pressed
get_graph = 0
img = None
while (get_graph==0):
    get_graph = get('get_graph','get_graph')
    img = cv2.imread(r"C:\Users\jonat\opencv\assets\fromphone.jpeg")
    img = cv2.resize(img, (0, 0), fx=400/img.shape[1], fy=400/img.shape[1])
    cv2.imshow('Live_window', img)
    cv2.waitKey(1)
cv2.destroyAllWindows() 


graph, cropped =  image_process(img, opencv, print_graph, maze_debbuger)
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
    print(f'The retrieved destination is ({destination[0]}, {destination[1]})')

    # Set the state to 0 - cannot send destenation now
    post('state','state',0)
    if (end==1):
        break
    shortest_path = bfs(graph, position, destination)
    directions, currentDirection = moveSequence(position, currentDirection, shortest_path, destination)
    shortest_path.insert(0,(position[0],position[1]))
    run_manim(cropped, graph, shortest_path, manim, side_by_side, opencv)
    print(directions)
    print(shortest_path)
    position = destination.copy()