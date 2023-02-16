import math

FORWARD = 0
RIGHT = 90
LEFT = -90
BACK = 180

def bfs(graph, start_list, end_list):
    start = (start_list[0],start_list[1])
    end = (end_list[0],end_list[1])
    size = 7
    node = start
    successors = []
    visited = []
    paths = {start: []}
    nextPath = []
    
    while (len(visited) < size ** 2):
        visited.append(node)
        for nextNode in graph[node]:
            if (nextNode not in visited) and (nextNode not in successors):
                successors.append(nextNode)
                nextPath = paths[node].copy()
                nextPath.append(nextNode)
                paths.update({nextNode: nextPath})
        if (len(successors) == 0):
            if (end in visited): return paths[end].copy()
            else: return -1
        else:
            node = successors.pop(0)
#print(bfs(start, end))


currentDirection = 0

def moveSequence(pos, currentDirection, path, end):
    if (path == -1): return -1
    seq = []
    nodeNum = len(path)
    seqLen = len(seq)-1
    i = 0
    for i in range(nodeNum):
        seqLen = len(seq)-1
        if (i == 0): prevLocation = pos
        else: prevLocation = location
        location = path[i]
        seq.append(nodeChange(currentDirection, prevLocation, location)[0])
        seq.append(nodeChange(currentDirection, prevLocation, location)[1])
        currentDirection += (seq[seqLen+1])
        currentDirection -= math.floor((currentDirection + 180) / 360) * 360
        if (currentDirection == -180): currentDirection = 180
        
        if ((i > 0) and (seq[seqLen+1]) == 0):
            seq.pop()
            seq.pop()
            seq[len(seq)-1] += 1
    pos = end
    return seq, currentDirection, pos


def nodeChange(direction, node1, node2):
    if ((node2[0] - node1[0] == 1 and direction == RIGHT) or (node2[1] - node1[1] == 1 and direction == BACK) or (node2[0] - node1[0] == -1 and direction == LEFT) or (node2[1] - node1[1] == -1 and direction == FORWARD)):
        return (FORWARD, 1)
    if ((node2[0] - node1[0] == 1 and direction == FORWARD) or (node2[1] - node1[1] == 1 and direction == RIGHT) or (node2[0] - node1[0] == -1 and direction == BACK) or (node2[1] - node1[1] == -1 and direction == LEFT)):
        return (RIGHT, 1)
    if ((node2[0] - node1[0] == 1 and direction == LEFT) or (node2[1] - node1[1] == 1 and direction == FORWARD) or (node2[0] - node1[0] == -1 and direction == RIGHT) or (node2[1] - node1[1] == -1 and direction == BACK)):
        return (BACK, 1)
    if ((node2[0] - node1[0] == 1 and direction == BACK) or (node2[1] - node1[1] == 1 and direction == LEFT) or (node2[0] - node1[0] == -1 and direction == FORWARD) or (node2[1] - node1[1] == -1 and direction == RIGHT)):
        return (LEFT, 1)