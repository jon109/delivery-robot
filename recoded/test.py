import cv2
import numpy as np
import requests
from utilitis.process import *
from utilitis.shortest_path_1 import *
from utilitis.http_functions import *
#from utilitis.manim_class import *
import threading
import queue

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


#please set correct starting position
position = [0,0]
destination = [0,0]

# Set state to 1 - app will be able to send data
post('state','state',1)
# Set end to 0 - will run
post('end','end',0)

#wait until get graph button pressed
get_graph = 0
img = None
while (get_graph==0):
    get_graph = get('get_graph','get_graph')
    img = cv2.imread(r"C:\Users\jonat\opencv\assets\fromphone.jpeg")
    img = cv2.resize(img, (0, 0), fx=500/img.shape[1], fy=500/img.shape[1])
    cv2.imshow('Live_window', img)
    cv2.waitKey(1)
cv2.destroyAllWindows() 


q = queue.Queue()
image_thread = threading.Thread(target=process, args=(img,q))
image_thread.start()
while (q.empty()):
    pass
output = q.get()
graph, cropped = output[0], output[1]
while (graph ==-1):
    image_thread.join()
    while (get_graph==0):
        img = cv2.imread(r"C:\Users\jonat\opencv\assets\fromphone.jpeg")
        img = cv2.resize(img, (0, 0), fx=500/img.shape[1], fy=500/img.shape[1])
        cv2.imshow('Live_window', img)
    cv2.destroyAllWindows()
    thread = threading.Thread(target=process, args=(img,q))
    while (q.empty()):
        pass
    output = q.get()
    graph, cropped = output[0], output[1]

while True:
    print(position)
    destination[0],destination[1], end = wait_for_destination()
    print(position)
    if (end==1):
        break
    shortest_path = bfs(graph, position, destination)
    directions, currentDirection = moveSequence(position, currentDirection, shortest_path, destination)
    #run_manim(cropped, graph, shortest_path, manim, side_by_side, opencv)
    print(directions)
    position = destination.copy()
    print(position)