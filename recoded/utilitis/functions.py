import cv2
import numpy as np

rows = 6
columns = 6


def get_square():
    return square

# if 70% or more of the pixels are black then this section is mostly not red

def Percentage_of_black_to_total(section):
    mask1 = cv2.inRange(section, (170, 70, 50), (180, 255, 255))
    mask2 = cv2.inRange(section, (0, 70, 50), (10, 255, 255))
    thresh = mask1 | mask2
    number_of_white_pix = np.sum(thresh == 255)
    number_of_black_pix = np.sum(thresh == 0)
    return number_of_black_pix/(number_of_white_pix+number_of_black_pix)

def IsMostlyNotRed(section):
    return Percentage_of_black_to_total(section) > 0.8

# I presumed that the square to obsticle(width) ratio is 1 to 6
# sections should like this dict={portion1:(1.5,1.5), portion2:(2.5,1)...}

def maze_debug(cropped_1, squares_1, status_1):
    print("please take a look and write down the wrong tile number, if there are any\nwhen your finished press q")
    cropped = cropped_1.copy()
    cropped_copy = cropped_1.copy()
    squares = squares_1.copy()
    status = status_1
    for i in range(len(squares)):
        center_point_position = (i % rows + 0.5, i//columns + 0.5)
        freedom = status[center_point_position]
        x,y,w,h= squares[i]
        cv2.line(cropped, (x+w,int((2*y+h)/2)),(int((2*x+w)/2),int((2*y+h)/2)),(int(255*freedom[0]),int(255-(255*freedom[0])),int(255-(255*freedom[0]))),3)
        cv2.putText(cropped,f'{4*i}',(x+w-30,int((2*y+h)/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),1,cv2.LINE_AA)
        cv2.line(cropped, (x,int((2*y+h)/2)),(int((2*x+w)/2),int((2*y+h)/2)),(int(255*freedom[1]),int(255-(255*freedom[1])),int(255-(255*freedom[1]))),3)
        cv2.putText(cropped,f'{4*i+1}',(x-5,int((2*y+h)/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),1,cv2.LINE_AA)
        cv2.line(cropped, (int((2*x+w)/2),y),(int((2*x+w)/2),int((2*y+h)/2)),(int(255*freedom[2]),int(255-(255*freedom[2])),int(255-(255*freedom[2]))),3)
        cv2.putText(cropped,f'{4*i+2}',(int((2*x+w)/2-10),y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),1,cv2.LINE_AA)
        cv2.line(cropped, (int((2*x+w)/2),y+h),(int((2*x+w)/2),int((2*y+h)/2)),(int(255*freedom[3]),int(255-(255*freedom[3])),int(255-(255*freedom[3]))),3)
        cv2.putText(cropped,f'{4*i+3}',(int((2*x+w)/2-10),y+h-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),1,cv2.LINE_AA)
    cv2.imshow("original cropped image", cropped_copy)
    cv2.imshow("this maze", cropped)
    key = cv2.waitKey(0)
    if key==ord('q'):
        cv2.destroyAllWindows()
    print ("how many wrong tiles were there? (enter 0 if all was good)")
    val = int(input())
    if (val == 0):
        print("ok ending maze debug...")
        return 0
    sections = []
    for i in range(val):
        tile = (int(input(f"enter wrong tile({i+1}): ")))
        x,y,w,h= squares[tile//4]
        sections.append(cropped_copy[y:y+h, x:x+w])
    i=0
    for section in sections:
        section = cv2.resize(section, (0, 0), fx=400/section.shape[1], fy=400/section.shape[1])
        section_hsv = cv2.cvtColor(section, cv2.COLOR_BGR2HSV)
        t = 0.4
        x, y, _ = section.shape
        tx = t
        ty = tx*x/y
        cv2.rectangle(section, (int(0.5*x*(1-tx)), 0),
                          (int(0.5*x*(1+tx)), int(0.5*y*(1-ty))), (10, 255, 0), 2)
        cv2.rectangle(section, (int(0.5*x*(1-tx)), int(0.5*y*(1+ty))),
                          (int(0.5*x*(1+tx)), y), (50, 255, 0), 2)
        cv2.rectangle(section, (int(0.5*x*(1+tx)), int(0.5*y*(1-ty))),
                          (x, int(0.5*y*(1+ty))), (100, 255, 0), 2)
        cv2.rectangle(section, (0, int(0.5*y*(1-ty))),
                          (int(0.5*x*(1-tx)), int(0.5*y*(1+ty))), (150, 255, 0), 2)
        mask1 = cv2.inRange(section_hsv, (170, 70, 50), (180, 255, 255))
        mask2 = cv2.inRange(section_hsv, (0, 70, 50), (10, 255, 255))
        thresh = mask1 | mask2
        portionUp = section_hsv[0:int(0.5*y*(1-ty)),
                            int(0.5*x*(1-tx)):int(0.5*x*(1+tx))]
        portionDown = section_hsv[int(0.5*y*(1+ty)):y,
                              int(0.5*x*(1-tx)):int(0.5*x*(1+tx))]
        portionRight = section_hsv[int(0.5*y*(1-ty)):int(0.5*y*(1+ty)), int(0.5*x*(1+tx)):x]
        portionLeft = section_hsv[int(0.5*y*(1-ty)):int(0.5*y*(1+ty)), 0:int(0.5*x*(1-tx))]
        cv2.putText(section,f'{round(Percentage_of_black_to_total(portionRight),3)}',(int(x-75),int(y/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),1,cv2.LINE_AA)
        cv2.putText(section,f'{round(Percentage_of_black_to_total(portionLeft),3)}',(int(75),int(y/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),1,cv2.LINE_AA)
        cv2.putText(section,f'{round(Percentage_of_black_to_total(portionUp),3)}',(int(x/2),int(50)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),1,cv2.LINE_AA)
        cv2.putText(section,f'{round(Percentage_of_black_to_total(portionDown),3)}',(int(x/2),int(y-50)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),1,cv2.LINE_AA)
        cv2.imshow(f"square of tile({i+1})", section)
        cv2.imshow(f"thresh of square of tile({i+1})", thresh)
        i+=1
    key = cv2.waitKey(0)
    if key==ord('q'):
        cv2.destroyAllWindows()


def get_center_points_status(sections):
    status = {}
    t = 0.4
    for i in range(len(sections)):
        section = sections[i]
        x, y, _ = section.shape
        tx = t
        ty = tx*x/y
        if (i == 3):
            print("hello")
        portionUp = section[0:int(0.5*y*(1-ty)),
                            int(0.5*x*(1-tx)):int(0.5*x*(1+tx))]
        portionDown = section[int(0.5*y*(1+ty)):y,
                              int(0.5*x*(1-tx)):int(0.5*x*(1+tx))]
        portionRight = section[int(0.5*y*(1-ty)):int(0.5*y*(1+ty)), int(0.5*x*(1+tx)):x]
        portionLeft = section[int(0.5*y*(1-ty)):int(0.5*y*(1+ty)), 0:int(0.5*x*(1-tx))]
        center_point_position = i % rows + 0.5, i//columns + 0.5
        z= IsMostlyNotRed(portionDown)
        status[(center_point_position)] = [IsMostlyNotRed(portionRight), IsMostlyNotRed(
            portionLeft), IsMostlyNotRed(portionUp), IsMostlyNotRed(portionDown)]
        # for debug choose i to choose a specific square to focus on
        if (i == 21):
            cv2.rectangle(section, (int(0.5*x*(1-tx)), 0),
                          (int(0.5*x*(1+tx)), int(0.5*y*(1-ty))), (10, 255, 0), 1)
            cv2.rectangle(section, (int(0.5*x*(1-tx)), int(0.5*y*(1+ty))),
                          (int(0.5*x*(1+tx)), y), (50, 255, 0), 1)
            cv2.rectangle(section, (int(0.5*x*(1+tx)), int(0.5*y*(1-ty))),
                          (x, int(0.5*y*(1+ty))), (100, 255, 0), 1)
            cv2.rectangle(section, (0, int(0.5*y*(1-ty))),
                          (int(0.5*x*(1-tx)), int(0.5*y*(1+ty))), (150, 255, 0), 1)
            print(status[(center_point_position)])
            global square
            square = cv2.resize(cv2.cvtColor(
                section, cv2.COLOR_HSV2BGR), (0, 0), fx=3, fy=3)

    return status


def CanMoveLeft(point, MovementsAllowed):
    centerUp = (point[0]-0.5, point[1]-0.5)
    centerDown = (point[0]-0.5, point[1]+0.5)
    if (point[0]-0.5 < 0):
        return False
    if (centerUp[1] < 0):
        return MovementsAllowed[centerDown][2]
    if (centerDown[1] > columns):
        return MovementsAllowed[centerUp][3]
    return MovementsAllowed[centerUp][3] and MovementsAllowed[centerDown][2]


def CanMoveRight(point, MovementsAllowed):
    centerUp = (point[0]+0.5, point[1]-0.5)
    centerDown = (point[0]+0.5, point[1]+0.5)
    if (point[0]+0.5 > rows):
        return False
    if (centerUp[1] < 0):
        return MovementsAllowed[centerDown][2]
    if (centerDown[1] > columns):
        return MovementsAllowed[centerUp][3]
    return MovementsAllowed[centerUp][3] and MovementsAllowed[centerDown][2]


def CanMoveUp(point, MovementsAllowed):
    centerRight = (point[0]+0.5, point[1]-0.5)
    centerLeft = (point[0]-0.5, point[1]-0.5)
    if (point[1]-0.5 < 0):
        return False
    if (centerLeft[0] < 0):
        return MovementsAllowed[centerRight][1]
    if (centerRight[0] > rows):
        return MovementsAllowed[centerLeft][0]
    return MovementsAllowed[centerRight][1] and MovementsAllowed[centerLeft][0]


def CanMoveDown(point, MovementsAllowed):
    centerRight = (point[0]+0.5, point[1]+0.5)
    centerLeft = (point[0]-0.5, point[1]+0.5)
    if (point[1]+0.5 > columns):
        return False
    if (centerLeft[0] < 0):
        return MovementsAllowed[centerRight][1]
    if (centerRight[0] > rows):
        return MovementsAllowed[centerLeft][0]
    return MovementsAllowed[centerRight][1] and MovementsAllowed[centerLeft][0]

#                                        - cords of square - right - left  - up  -  down
# status is dictionary of squares example: square {(1.5,1.5):[False, False, Falase, False]}
# False - is not blocked, True - is blocked


def generate_graph(points, MovementsAllowed):
    dict = {}
    for point in points:
        dict[point] = []
        if (CanMoveLeft(point, MovementsAllowed)):
            dict[point].append((point[0]-1, point[1]))
        if (CanMoveRight(point, MovementsAllowed)):
            dict[point].append((point[0]+1, point[1]))
        if (CanMoveUp(point, MovementsAllowed)):
            dict[point].append((point[0], point[1]-1))
        if (CanMoveDown(point, MovementsAllowed)):
            dict[point].append((point[0], point[1]+1))
    return dict


def generate_points(rows, columns):
    points = []
    for i in range(rows+1):
        for j in range(columns+1):
            points.append((i, j))
    return points


def generate_slices(img, rows, columns):
    cropped = img[:-10,]


def sort_boxes(boxes_list):
    boxes = np.array(boxes_list)
    ordered = []
    a = sorted(boxes, key=lambda x: x[1])
    b = np.reshape(a, (rows, columns, 4))
    for arr in b:
        arr = arr.tolist()
        sort = sorted(arr, key=lambda x: x[0])
        ordered.append(sort)
    return ordered


def sort_points(points):
    ordered = []
    a = sorted(points, key=lambda x: x[1])
    b = np.reshape(a, (2, 2, 2))
    for arr in b:
        arr = arr.tolist()
        sort = sorted(arr, key=lambda x: x[0])
        ordered.append(sort)
    return ordered