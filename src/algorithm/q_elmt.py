from algorithm.route import Route
class Elmt:
    def __init__(self,  route, node, cost, priority = None):
        self.route = route
        self.node = node
        self.cost = cost
        self.priority = priority
    def __lt__(self, other):
        return self.priority<other.priority
    def __eq__(self, other):
        return self.priority == other.priority
    def GetNode(self):
        return self.node
    def GetRoute(self):
        return self.route
    def GetCost(self):
        return self.cost