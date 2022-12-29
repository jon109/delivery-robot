import cv2
import numpy as np
rows =3
columns=3

#if 75% of pixels in red range return true
def ColorMostlyRed(section):
    thresh = cv2.inRange(section,(160, 30, 20), (10, 255, 255))
    number_of_white_pix = np.sum(thresh == 255)
    number_of_black_pix = np.sum(thresh == 0)
    return number_of_white_pix/(number_of_white_pix+number_of_black_pix) > 0.75

#I presumed that the square to obsticle(width) ratio is 1 to 6
#sections should like this dict={portion1:(1.5,1.5), portion2:(2.5,1)...}
def get_center_points_status(sections={}):
    status={}
    for section in sections:
        x,_ = section.size
        t=1/6
        portionUp = section[0.5*x*(1-t):0.5*x*(1+t)][0:0.5*x*(1-t)]
        portionDown = section[0.5*x*(1-t):0.5*x*(1+t)][0.5*x*(1+t):x]
        portionRight = section[0.5*x*(1+t):x][0.5*x*(1-t):0.5*x*(1+t)]
        portionLeft = section[0:0.5*x*(1-t)][0.5*x*(1-t):0.5*x*(1+t)]
        status[sections[section]]=[ColorMostlyRed(portionRight), ColorMostlyRed(portionLeft) , ColorMostlyRed(portionUp), ColorMostlyRed(portionDown)]
    return sections


def CanMoveLeft(point,status):
    centerUp = (point[0]-0.5,point[1]+0.5)
    centerDown = (point[0]-0.5,point[1]-0.5)
    if(point[0]-0.5<0):
        return False
    if (centerUp[1]<0):
        return status[centerDown]
    if (centerDown[1]>columns): 
        return status[centerUp]
    return status[centerUp] and status[centerDown]


def CanMoveRight(point, status):
    centerUp = (point[0]+0.5,point[1]+0.5)
    centerDown = (point[0]+0.5,point[1]-0.5)
    if(point[0]+0.5>rows):
        return False
    if (centerUp[1]<0):
        return status[centerDown]
    if (centerDown[1]>columns):
        return status[centerUp]
    return status[centerUp] and status[centerDown]

def CanMoveUp(point, status):
    centerRight = (point[0]-0.5,point[1]+0.5)
    centerLeft = (point[0]-0.5,point[1]-0.5)
    if(point[1]-0.5<0):
        return False
    if (centerLeft[0]<0):
        return status[centerRight]
    if (centerRight[1]>rows):
        return status[centerLeft]
    return status[centerRight] and status[centerLeft]

def CanMoveDown(point, status):
    centerRight = (point[0]+0.5,point[1]+0.5)
    centerLeft = (point[0]+0.5,point[1]-0.5)
    if(point[1]+0.5<columns):
        return False
    if (centerLeft[0]<0):
        return status[centerRight]
    if (centerRight[1]>rows):
        return status[centerLeft]
    return status[centerRight] and status[centerLeft]

#                                        - cords of square - right - left  - up  -  down 
#status is dictionary of squares example: square {(1.5,1.5):[False, False, Falase, False]}
def get_graph(points,status):
    dict = {}
    for point in points:
        if (CanMoveLeft(point,status)):
            dict[point].append((point[0]-1,point[1]))
        if (CanMoveRight(point,status)):
            dict[point].append((point[0]+1,point[1]))
        if (CanMoveUp(point,status)):
            dict[point].append((point[0],point[1]+1))
        if (CanMoveDown(point,status)):
            dict[point].append((point[0],point[1]-1))

def generate_points(rows, columns):
    points=[]
    for i in range (rows+1):
        for j in range (columns+1):
            points.append=(i,j)
    return points

def generate_square_slices(img):
    pass
