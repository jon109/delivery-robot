import requests
import time
from utilitis.process import *
import queue

def post(location, variable, data):
    # Set state to 1 - app will be able to send data
    response = requests.post(f'http://jon10.pythonanywhere.com/{location}', json={f'{variable}': data})
    if response.status_code != 200:
        print(f'an error has occured when setting {variable}')

def get(location, variable):
    response = requests.get(f'http://jon10.pythonanywhere.com/{location}')
    if response.status_code == 200:
        number = int(response.json()[f'{variable}'])
        return number
    else:
        print(f'Error retrieving {variable}')

def wait_for_destination():
        # Get destenation
    number = get('get_number', 'number')
    
    # While app hasn't entered a destenation, wait for it do so
    while (number == -1):
        key=cv2.waitKey(1)
        if (key ==27):
            cv2.destroyAllWindows()
            
        # If user presses end break the program
        end = get('end', 'end')
        if (end==1):
            break

        # Try to see if destenation was updated
        number = get('get_number', 'number')
        time.sleep(0.1)
    
    # If user presses end break the program
    end = get('end', 'end')
    if (end==1):
        return 0,0,1 
    
    # Set the destenation
    destination = [0,0]
    destination[0], destination[1] = (number-1)%7,(number-1)//7

    # Set the state to 0 - cannot send destenation now
    return destination[0],destination[1], end

def process(img, q):
    graph, cropped =  image_process(img)
    print("done1")
    q.put([graph,cropped])
    print("done1")
    while True:
        key=cv2.waitKey(0)
        if (key ==27):
            break
    cv2.destroyAllWindows()