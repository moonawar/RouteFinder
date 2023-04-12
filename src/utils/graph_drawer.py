from tkinter import Canvas
import networkx as nx
import matplotlib.pyplot as plt
from PIL import ImageTk, Image

NODE_COLOR = "#07111F"
SOLUTION_EDGE_COLOR = "#E2BD45"
NODE_NAME_COLOR = "#0D356A"

class GraphCanvas(Canvas):
    def __init__(self, parent, data, node_names = None):
        super().__init__(parent)
        self.data = data
        self.graph = None
        self.graph_image = None
        self.output_file_path = ""
        self.canvas_img = None
        self.node_names = node_names

        self.build()

    def build(self):
        self.draw_graph()
        self.graph_image = ImageTk.PhotoImage(Image.open(self.output_file_path))
        self.canvas_img = self.create_image(100, 0, image=self.graph_image, anchor="nw")

    def draw_graph(self):
        plt.clf()
        data = self.data
        labelpos = 0.4
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
        self.pos = pos

        nx.draw(self.graph, pos, node_color=NODE_COLOR, node_size=500, alpha=0.85,
                arrows=True, width=2, with_labels=False)
                
        edge_labels = nx.get_edge_attributes(self.graph, "weight")
        nx.draw_networkx_edge_labels(self.graph, pos, font_size=8, label_pos=labelpos, font_color="black",
                edge_labels=edge_labels, alpha=0.9)
        
        labels_pos = { i : (pos[i][0], pos[i][1] + 0.1) for i in pos.keys()}
        label_names = { i : self.node_names[i] for i in range(len(self.node_names))}
        nx.draw_networkx_labels(self.graph, labels_pos, font_size=8, font_color=NODE_NAME_COLOR,
                labels = label_names, alpha=0.9, font_weight="bold")

        self.output_file_path = "../test/result/graph.png"
        plt.savefig(self.output_file_path)

    def draw_solution_route(self, list_of_nodes):
        

        tuples_of_edge = [(list_of_nodes[i], list_of_nodes[i+1]) for i in range(len(list_of_nodes) - 1)]

        nx.draw_networkx_edges(self.graph, self.pos, edgelist=tuples_of_edge, 
                width=2, alpha=1, edge_color=SOLUTION_EDGE_COLOR, arrows=True)
        plt.savefig(self.output_file_path)
        self.graph_image = ImageTk.PhotoImage(Image.open(self.output_file_path))
        self.canvas_img = self.create_image(100, 0, image=self.graph_image, anchor="nw")

# To check if a matrix is symmetric (the graph is undirected) or not (which means the graph is directed)
def isSymmetric(mat, N):
    for i in range(N):
        for j in range(N):
            if (mat[i][j] != mat[j][i]):
                return False
    return True