from tkinter import Canvas
import networkx as nx
import matplotlib.pyplot as plt
from PIL import ImageTk, Image

class GraphCanvas(Canvas):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.data = data
        self.graph = None
        self.graph_image = None
        self.output_file_path = ""
        self.build()

    def build(self):
        self.draw_graph()
        self.graph_image = ImageTk.PhotoImage(Image.open(self.output_file_path))
        self.create_image(100, 0, image=self.graph_image, anchor="nw")

    def draw_graph(self):
        data = self.data
        if isSymmetric(data, len(data)):
            self.graph = nx.Graph()
        else:
            self.graph = nx.DiGraph()

        self.graph.add_nodes_from([i for i in range(len(data))])
        self.graph.add_weighted_edges_from(
            [
             (i, j, data[i][j]) 
             for i in range(len(data)) 
             for j in range(len(data)) 
             if data[i][j] != 0
            ])

        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True)
        self.output_file_path = "../test/result/graph.png"
        plt.savefig(self.output_file_path)

# To check if a matrix is symmetric (the graph is undirected) or not (which means the graph is directed)
def isSymmetric(mat, N):
    for i in range(N):
        for j in range(N):
            if (mat[i][j] != mat[j][i]):
                return False
    return True