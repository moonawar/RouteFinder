from queue import PriorityQueue
from algorithm.q_elmt import Elmt
from algorithm.route import Route                
        
def solve(matrix, start, finish, astar, astarMatrix = None):
    # Algoritma USC dan astar
    # set astar = false untuk USC
    # set astar true untuk astar            
    queue = PriorityQueue()
    queue.put(Elmt(Route(), start, 0, 0))
    found = False
    while not queue.empty() and not found:
        #get elmt
        temp = queue.get()
        if(temp.GetNode() in temp.GetRoute().GetBuffer()):
            continue
        
        newRoute = Route(temp.GetRoute())
        newRoute.addNode(temp.GetNode())
        if(temp.GetNode() == finish):
            found = True
            route = newRoute
        else:
            for i in getNeighbour(matrix, temp.GetNode()):
                new = Elmt(newRoute, i, matrix[temp.GetNode()][i] + temp.GetCost(), matrix[temp.GetNode()][i] + temp.GetCost() + (astarMatrix[i][finish] if astar else 0))
                queue.put(new)
    if(found):
        return route.GetBuffer(), temp.GetCost()
    else:
        return None, None

def createEuclidDistanceMatrix(arrayOfCoor):
    matrix = []
    for i in range(len(arrayOfCoor)):
        row = []
        for j in range(i, len(arrayOfCoor)):
            row.append(((arrayOfCoor[i][2]-arrayOfCoor[j][2])**2  + (arrayOfCoor[i][1]-arrayOfCoor[j][1])**2)**0.5)
        matrix.append(row)
    return matrix
            
        

def getNeighbour(matrix, node):
    array = []
    for i in range(len(matrix[node])):
        if matrix[node][i] != 0:
            array += [i]
    return array    