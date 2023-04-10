from route import Route
class Elmt:
    def __init__(self,  route, node, cost):
        self.route = route
        self.node = node
        self.cost = cost
    def __lt__(self, other):
        return self.cost<other.cost
    def __eq__(self, other):
        return self.cost == other.cost
    def GetNode(self):
        return self.node
    def GetRoute(self):
        return self.route
    def GetCost(self):
        return self.cost