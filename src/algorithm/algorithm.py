from queue import PriorityQueue
from algorithm.QELMT import Elmt
from algorithm.route import Route
import shlex
import copy
import math

def getMinimumSpanningTree(matrix):
    #Create a copy of matrix and transform it into minimum spanning tree adjecancy matrix
    MST = [[0 for i in range(len(matrix))] for j in range(len(matrix))]
    nodeAccessed = [False for i in range(len(matrix))]
    edge = 0
    nodeAccessed[0] = True
    while edge < len(matrix) -1:
        min = math.inf
        a = 0
        b = 0
        for i in range(len(nodeAccessed)):
            for j in range(len(nodeAccessed)):
                if (matrix[i][j] < min) and  (nodeAccessed[i] ^ nodeAccessed[j]) and matrix[i][j] != 0:
                    min = matrix[i][j]
                    a = i
                    b = j 
        nodeAccessed[a] = True
        nodeAccessed[b] = True
        MST[a][b] = min   
        MST[b][a] = min
        edge+=1
    return MST

def expandMST(MST):
    MST_OR = copy.deepcopy(MST)
    for i in range(len(MST)):
        for j in range(len(MST)):
            if i != j and MST[i][j] == 0:
                MST_OR[i][j] = DFSMST(MST, i,j, [False for k in range(len(MST))], 0)
                MST_OR[j][i] = MST_OR[i][j]
    return MST_OR
                
def DFSMST(MST, start, goal,visited, value):
    visited[start] = True
    if MST[start][goal] != 0:
        print(value + MST[start][goal])
        return value + MST[start][goal]
    else:
        for i in range(len(MST)):
            if i!= start and MST[start][i]!=0 and not visited[i]:
                temp = DFSMST(MST, i, goal, visited, MST[start][i] + value)
                if temp!=None:
                    return temp  
        return None
                
        
def solve(matrix, start, finish, astar, astarMatrix = None):
    #I.S. start, finish string, exists in graph. Astar boolean.
    #F.S. return path from start to finish
    if astar:
        if astarMatrix == None:
            astarMatrix = getMinimumSpanningTree(matrix)
            astarMatrix = expandMST(astarMatrix)
            
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
                print(matrix[temp.GetNode()][i])
                queue.put(new)
    if(found):
        return temp.GetCost(),route
    else:
        return None, None

def createEuclidDistanceMatrix(arrayOfCoor):
    matrix = []
    for i in range(len(arrayOfCoor)):
        row = []
        for j in range(len(arrayOfCoor)):
            row.append(((arrayOfCoor[i][2]-arrayOfCoor[j][2])**2  + (arrayOfCoor[i][1]-arrayOfCoor[j][1])**2)**0.5)
        matrix.append(row)
    return matrix
            
        

def getNeighbour(matrix, node):
    array = []
    for i in range(len(matrix[node])):
        if matrix[node][i] != 0:
            array += [i]
    return array    


