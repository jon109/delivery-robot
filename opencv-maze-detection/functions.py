import cv2
import numpy as np

rows = 6
columns = 6

#if 70% or more of the pixels are black then this section is mostly not red 
def IsMostlyNotRed(section):
    mask1 = cv2.inRange(section,(170, 70, 50), (180, 255, 255))
    mask2 = cv2.inRange(section,(0, 70, 50), (10, 255, 255))
    thresh = mask1|mask2
    number_of_white_pix = np.sum(thresh == 255)
    number_of_black_pix = np.sum(thresh == 0)
    return number_of_black_pix/(number_of_white_pix+number_of_black_pix) > 0.7

#I presumed that the square to obsticle(width) ratio is 1 to 6
#sections should like this dict={portion1:(1.5,1.5), portion2:(2.5,1)...}
def get_center_points_status(sections):
    status={}
    t=0.4
    for i in range (len(sections)):
        section=sections[i]
        x,y,_=section.shape
        tx=t
        ty= tx*x/y
        portionUp=section[0:int(0.5*y*(1-ty)), int(0.5*x*(1-tx)):int(0.5*x*(1+tx))]
        portionDown = section[int(0.5*y*(1+ty)):y, int(0.5*x*(1-tx)):int(0.5*x*(1+tx))]
        portionRight =  section[int(0.5*y*(1-ty)):int(0.5*y*(1+ty)), int(0.5*x*(1+tx)):x]
        portionLeft = section[int(0.5*y*(1-ty)):int(0.5*y*(1+ty)), 0:int(0.5*x*(1-tx))]
        center_point_position = i%rows + 0.5, i//columns + 0.5 
        status[(center_point_position)]= [IsMostlyNotRed(portionRight), IsMostlyNotRed(portionLeft) , IsMostlyNotRed(portionUp), IsMostlyNotRed(portionDown)]
        """
        #for debug choose i to choose a specific square to focus on
        if (i==4)
        cv2.rectangle(section,(int(0.5*x*(1-tx)),0),(int(0.5*x*(1+tx)),int(0.5*y*(1-ty))),(10,255,255),1)
        cv2.rectangle(section,(int(0.5*x*(1-tx)),int(0.5*y*(1+ty))),(int(0.5*x*(1+tx)),y),(50,255,255),1)
        cv2.rectangle(section,(int(0.5*x*(1+tx)),int(0.5*y*(1-ty))),(x,int(0.5*y*(1+ty))),(100,255,255),1)
        cv2.rectangle(section,(0,int(0.5*y*(1-ty))),(int(0.5*x*(1-tx)),int(0.5*y*(1+ty))),(150,255,255),1)
        print(status[(center_point_position)])
        cv2.imshow(section, "debug")
        """
    return status



def CanMoveLeft(point,MovementsAllowed):
    centerUp = (point[0]-0.5,point[1]-0.5)
    centerDown = (point[0]-0.5,point[1]+0.5)
    if(point[0]-0.5<0):
        return False
    if (centerUp[1]<0):
        return MovementsAllowed[centerDown][2]
    if (centerDown[1]>columns): 
        return MovementsAllowed[centerUp][3]
    return MovementsAllowed[centerUp][3] and MovementsAllowed[centerDown][2]


def CanMoveRight(point, MovementsAllowed):
    centerUp = (point[0]+0.5,point[1]-0.5)
    centerDown = (point[0]+0.5,point[1]+0.5)
    if(point[0]+0.5>rows):
        return False
    if (centerUp[1]<0):
        return MovementsAllowed[centerDown][2]
    if (centerDown[1]>columns):
        return MovementsAllowed[centerUp][3]
    return MovementsAllowed[centerUp][3] and MovementsAllowed[centerDown][2]

def CanMoveUp(point, MovementsAllowed):
    centerRight = (point[0]+0.5,point[1]-0.5)
    centerLeft = (point[0]-0.5,point[1]-0.5)
    if(point[1]-0.5<0):
        return False
    if (centerLeft[0]<0):
        return MovementsAllowed[centerRight][1]
    if (centerRight[0]>rows):
        return MovementsAllowed[centerLeft][0]
    return MovementsAllowed[centerRight][1] and MovementsAllowed[centerLeft][0]

def CanMoveDown(point, MovementsAllowed):
    centerRight = (point[0]+0.5,point[1]+0.5)
    centerLeft = (point[0]-0.5,point[1]+0.5)
    if(point[1]+0.5>columns):
        return False
    if (centerLeft[0]<0):
        return MovementsAllowed[centerRight][1]
    if (centerRight[0]>rows):
        return MovementsAllowed[centerLeft][0]
    return MovementsAllowed[centerRight][1] and MovementsAllowed[centerLeft][0]

#                                        - cords of square - right - left  - up  -  down 
#status is dictionary of squares example: square {(1.5,1.5):[False, False, Falase, False]}
#False - is not blocked, True - is blocked
def generate_graph(points, MovementsAllowed):
    dict = {}
    for point in points:
        dict[point]=[]
        if (CanMoveLeft(point,MovementsAllowed)):
            dict[point].append((point[0]-1,point[1]))
        if (CanMoveRight(point,MovementsAllowed)):
            dict[point].append((point[0]+1,point[1]))
        if (CanMoveUp(point,MovementsAllowed)):
            dict[point].append((point[0],point[1]-1))
        if (CanMoveDown(point,MovementsAllowed)):
            dict[point].append((point[0],point[1]+1))
    return dict

def generate_points(rows, columns):
    points=[]
    for i in range (rows+1):
        for j in range (columns+1):
            points.append((i,j))
    return points

def generate_slices(img, rows,columns):
    cropped = img [:-10,]

def sort_boxes(boxes_list):
    boxes = np.array(boxes_list)
    ordered=[]
    a = sorted(boxes, key=lambda x : x[1])
    b = np.reshape(a,(rows,columns,4))
    for arr in b:
        arr=arr.tolist()
        sort = sorted(arr, key=lambda x : x[0])
        ordered.append(sort)
    return ordered

def sort_points(points):
    ordered = []
    a = sorted(points, key=lambda x : x[1]) 
    b = np.reshape(a,(2,2,2))
    for arr in b:
        arr=arr.tolist()
        sort = sorted(arr, key=lambda x : x[0])
        ordered.append(sort)
    return ordered