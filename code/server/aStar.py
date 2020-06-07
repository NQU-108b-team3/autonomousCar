from heapq import heappush, heappop
import numpy

def heuristic(a, b):
    return ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** (1 / 2)

def astar(array, start, goal):
    neighbors = [(0,1),(0,-1),(1,0),(-1,0)]
    # neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

    close_set = set()
    came_from = {}
    gscore = {start:0}
    fscore = {start:heuristic(start, goal)}
    oheap = []

    heappush(oheap, (fscore[start], start))
    
    while oheap:
        current = heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            data.append(start)
            data.reverse()
            return data

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j            
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:                
                    if array[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    continue
            else:
                continue
                
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue
                
            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heappush(oheap, (fscore[neighbor], neighbor))
                
    if (start[0] == goal[0]) or (start[0] == goal[0]):
        return list([start, goal])

def findStrait(path):
    nPath = path.copy()
    for i in range(len(path)-1):
        p0 = (path[i][0] == path[i + 1][0] and path[i][0] == path[i - 1][0])
        p1 = (path[i][1] == path[i + 1][1] and path[i][1] == path[i - 1][1])
        if p0 or p1:
            nPath[i] = (-1, -1)
        else:
            pass
    return nPath

def viaPoints(nPath):
    count = 0
    for _ in range(len(nPath)):
        if nPath[count] == (-1, -1):
            nPath.pop(count)
        else:
            count += 1
    return nPath
