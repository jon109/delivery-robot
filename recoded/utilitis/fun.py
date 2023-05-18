import cv2
import numpy as np
import requests
from utilitis.process import *
from utilitis.shortest_path_1 import *
import serial
import imutils
import time

# visuals control
# opencv - 0(dont show anything), 1(show everythng), 2(show first half, until cropped), 3(show only second half from cropped until end)
opencv = 1
# print_graph - print the graph to console true/flase
print_graph = True
#allow maze debugging
maze_debbuger = False

# Android-Cam IP
url = "http://192.168.20.21:8080/shot.jpg"

position = [0,0]
destination = [0,0]

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

# Set state to 1 - app will be able to send data
response = requests.post('http://jon10.pythonanywhere.com/state', json={'state': 1})
if response.status_code != 200:
    print('an error has occured when setting state')
else:
    print('state set to 1 (app can send destenation)')

# Set end to 0 - will run
response = requests.post('http://jon10.pythonanywhere.com/end', json={'end': 0})
if response.status_code != 200:
    print('an error has occured when setting end')
else:
    print('end set to 0')

while True:
    # Get destenation
    response = requests.get('http://jon10.pythonanywhere.com/get_number')
    if response.status_code == 200:
        number = int(response.json()['number'])
    else:
        print('Error retrieving number')
    
    # While app hasn't entered a destenation, wait for it do so
    while (number == -1):
        # If user presses end break the program
        response = requests.get('http://jon10.pythonanywhere.com/end')
        if response.status_code == 200:
            end = int(response.json()['end'])
            if (end==1):
                break
        else:
            print('Error retrieving number')
        
        # Try to see if destenation was updated
        response = requests.get('http://jon10.pythonanywhere.com/get_number')
        if response.status_code == 200:
            number = int(response.json()['number'])
        else:
            print('Error retrieving number')
        time.sleep(0.1)
    
    # If user presses end break the program
    response = requests.get('http://jon10.pythonanywhere.com/end')
    if response.status_code == 200:
        end = int(response.json()['end'])
        if (end==1):
            break
    
    # Set the destenation
    destination[0], destination[1] = (number-1)%7,(number-1)//7
    print(f'The retrieved destination is ({destination[0]}, {destination[1]})')

    # Set the state to 0 - cannot send destenation now
    response = requests.post('http://jon10.pythonanywhere.com/state', json={'state': 0})
    if response.status_code != 200:
        print('an error has occured when setting state')
    else:
        print('state set to 0 (app cannot send destenation)')
    
    # Get image from phone
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    img = cv2.resize(img, (0, 0), fx=500/img.shape[1], fy=500/img.shape[1])

    graph, cropped =  image_process(img)
    shortest_path = bfs(graph, position, destination)
    directions, currentDirection, position = moveSequence(position, currentDirection, shortest_path, destination)

    # Send the directions thorugh bluetooth to the arduino
    length = bytes([len(directions)])
    ser.write(length)
    for i in range(len(directions)):
        ser.write(bytes([abs(directions[i])]))
        ser.write(b'1' if directions[i] > 0 else b'0')
        
    key=cv2.waitKey(0)
    
    while (ser.in_waiting == 0):
        pass
    response = ser.read().decode('ascii').rstrip()
    if (response == 'g'):
        print("robot finisehd the track")
        # Set state to 1 - let app send new destenation
        response = requests.post('http://jon10.pythonanywhere.com/state', json={'state': 1})
        if response.status_code != 200:
            print('an error has occured when setting state')
        else:
            print('state set to 1 (app can send destenation)')    

cv2.destroyAllWindows()
ser.close()