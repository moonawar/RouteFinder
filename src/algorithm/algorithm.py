import networkx as nx
from queue import PriorityQueue
from QELMT import Elmt
from route import Route
import shlex
import os
import matplotlib.pyplot as plt
def solve(graph, start, finish, astar, astarMatrix):
    print("Finish: " + finish)
    #I.S. start, finish string, exists in graph. Astar boolean.
    #F.S. return path from start to finish
    queue = PriorityQueue()
    queue.put(Elmt(Route(), start, 0))
    found = False
    while not queue.empty() and not found:
        #get elmt
        temp = queue.get()
        if(temp.GetNode() in temp.GetRoute().GetBuffer()):
            continue
        
        print("Simpul E: " +temp.GetNode()+", "+ str(temp.GetCost()))
        
        newRoute = Route(temp.GetRoute())
        newRoute.addNode(temp.GetNode())
        if(temp.GetNode() == finish):
            found = True
            route = newRoute
        else:
            for i in graph.neighbors(temp.GetNode()):
                new = Elmt(newRoute, i,int(graph[temp.GetNode()][i]['weight']) + temp.GetCost())
                queue.put(new)
    return temp.GetCost(),route



def TxtReader(file):
    #Return graph
    f = open(file, "r")
    nodes = []
    graph = nx.Graph()
    for i, line in enumerate(f.readlines()):
        if(i==0):
            for j,node in enumerate(shlex.split(line)):
                if j!=0:
                    graph.add_node(node)
                    nodes += node
        else:
            enumartion = line.split()
            for j in range(i+1, len(enumartion)):    
                if enumartion[j] != '#':
                    graph.add_edge(nodes[j-1], enumartion[0])
                    graph[nodes[j-1]][enumartion[0]]["weight"] = enumartion[j]
    f.close()
    return graph


test = TxtReader("src/algorithm/test.txt")
pos = nx.spring_layout(test)
labels = nx.get_edge_attributes(test,'weight')
nx.draw(test,pos, with_labels = True)
nx.draw_networkx_edge_labels(test,pos,edge_labels=labels)

#plt.show()

cost,solution = solve(test, "A", "B", False, False)
print("Hasilnya "+solution.__str__()+" dengan cost "+str(cost))



