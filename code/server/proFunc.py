from aStar import astar, viaPoints, findStrait
import numpy

nmap = numpy.array([(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
                    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1),
                    (1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
                    (1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1),
                    (1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1),
                    (1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1),
                    (1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1),
		            (1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1),
		            (1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1),
		            (1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1),
		            (1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1),
		            (1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1),
		            (1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1),
		            (1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1),
		            (1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1),
		            (1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1),
		            (1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1),
		            (1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1),
		            (1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
		            (1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1),
                    (1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1),
		            (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)])

def testCurrP(msg):
    return tuple(eval(msg))

def testCarStats(msg):
    return int(msg)

def testTarget(msg, viaPath, carP):
    msg = msg.replace(" ", "")
    dest = list(msg.split(','))
    if len(dest) < 2:
        return "Input missing some arguments, enter again..."
    if  not dest[0].isdigit() or not dest[1].isdigit():
        return "Either x or y is not a digit, enter again..."
    if (dest[0] == "" or dest[1] == ""):
        return "Either missing x or y, enter again..."

    for i in range(len(dest)):
        dest[i] = int(dest[i])
    
    goal = tuple(dest)
    if (goal[0] < 0 or goal[1] < 0) or (goal[0] > len(nmap) or goal[1] > len(nmap[1])):
        return "Out of map, enter again..."
    if nmap[goal[0]][goal[1]] == 1:
        return "Destination is a wall, enter again..."
    

    path = astar(nmap, carP, goal)
    print("path: ", path)

    nPath = findStrait(path)
    print("nPath: ", nPath)

    viaPath = viaPoints(nPath)
    print("viaPath: ", viaPath)

    if carP in viaPath:
        viaPath.remove(carP)

    return viaPath