class Route:
    def __init__(self, other = None):
        if other == None:
            self.buffer = []
        else:
            self.buffer = other.GetBuffer().copy()
    def __str__(self):
        output = ""
        for i in self.buffer:
            output+=i
        return output
    def addNode(self,node):
        self.buffer += [node]
        
    def isExists(self,node):
        for i in self.buffer:
            if(i == node):
                return True 
        return False
    def GetBuffer(self):
        return self.buffer
    