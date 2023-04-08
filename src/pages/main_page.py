from tkinter import Frame, Canvas, StringVar, IntVar, Label, messagebox
from tkinter.ttk import Combobox
from utils.canvas_utils import *
from utils.file_reader import *
from utils.element_builder import DropdownBuilder, FilePickerBuilder
from utils.graph_drawer import GraphCanvas
from utils.map_provider import MapView
from window.i_main_window import IMainWindow

""" Main Page for File Input Mode"""
class MainPage_FileInput(Frame):
    def __init__(self, window : IMainWindow):
        super().__init__(window)
        self.window = window
        self.assets = []
        self.graph_canvas = None

        # dropdown options
        self.vars = {
            "start_node": StringVar(value="Load File First"),
            "dest_node": StringVar(value="Load File First"),
            "algorithm": StringVar(value="Not Selected"),
            "file_path": StringVar(value="None"),
            "num_of_nodes": IntVar(value=0),
            "message": StringVar(value="Please load a file first before running the algorithm"),
        }

        self.build()
    
    def build(self):
        # layout
        self.rowconfigure(0, weight=2, uniform="a")
        self.rowconfigure(1, weight=8, uniform="a")
        self.rowconfigure(2, weight=2, uniform="a")
        self.columnconfigure(0, weight=3, uniform="a")
        self.columnconfigure(1, weight=7, uniform="a")

        # header
        header = MainPage_Header(self)
        header.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # body
        body = MainPage_FileInput_Body(self)
        body.grid(row=1, column=0, rowspan=2, sticky="nsew")

        # footer
        footer = MainPage_Footer(self)
        footer.grid(row=2, column=1, sticky="nsew")

    def run_algorithm(self):
        if self.vars["file_path"].get() == "None":
            self.vars["message"].set("Please load a file first before running the algorithm")
            messagebox.showerror("Error", "Please load a file first before running the algorithm")
            return
        elif self.vars["start_node"].get() == "Select Node" or self.vars["dest_node"].get() == "Select Node":
            self.vars["message"].set("Please select a start and destination node")
            messagebox.showerror("Error", "Please select a start and destination node")
            return
        elif self.vars["algorithm"].get() == "Not Selected":
            self.vars["message"].set("Please select the search algorithm")
            messagebox.showerror("Error", "Please select the search algorithm")
            return
        else:
            self.vars["message"].set("Running Algorithm...")
            if self.vars["algorithm"].get() == "Uniform-Cost Search":
                print("Uniform-Cost Search")
            elif self.vars["algorithm"].get() == "A* Search":
                print("A* Search")


"""Header Component for Main Page"""
class MainPage_Header(Canvas):
    def __init__(self, parent):
        super().__init__(parent, bg="#07111F")
        self.build()

    def build(self):
        self.create_text(40, 35, text="Route Finder", font=("Montserrat", 32, "bold"), fill="#E2BD45", anchor="nw")
        
        add_img(self, "main_page/header-logo.png")
        self.create_image(1000, 30, image=self.master.assets[-1], anchor="nw")

"""Body Component for Main Page (File Input Mode)"""
class MainPage_FileInput_Body(Canvas):
    def __init__(self, parent):
        super().__init__(parent)
        change_background(self, "main_page/body-bg.png")
        self.parent = parent

        self.start_dropdown : Combobox = None
        self.dest_dropdown : Combobox = None

        self.build()

    def build(self):
        builder_dropdown = DropdownBuilder(self)
        builder_file_picker = FilePickerBuilder(self)

        # Create file picker
        builder_file_picker.create(40, 40)

        # Create dropdowns
        self.start_dropdown = builder_dropdown.create("Starting Node", [], 40, 140, self.parent.vars["start_node"])
        self.start_dropdown.state(["disabled"])

        self.dest_dropdown = builder_dropdown.create("Destination Node", [], 40, 240, self.parent.vars["dest_node"])
        self.dest_dropdown.state(["disabled"])
        
        builder_dropdown.create("Algorithm", ["Uniform-Cost Search", "A* Search"], 40, 340, self.parent.vars["algorithm"])

        # Start button
        self.create_text(40, 455, text="Start Finding", font=("Montserrat", 16, "bold"), fill="white", anchor="nw")   
        img_start_btn = add_img(self, "main_page/start-button.png", 1)
        start_btn = self.create_image(200, 450, image=img_start_btn, anchor="nw")
        self.tag_bind(start_btn, "<Button-1>", lambda e: self.parent.run_algorithm())

        # Clear button
        self.create_text(40, 505, text="Clear", font=("Montserrat", 16, "bold"), fill="white", anchor="nw")
        img_clear_btn = add_img(self, "main_page/clear-button.png", 1)
        clear_btn = self.create_image(200, 500, image=img_clear_btn, anchor="nw")
        self.tag_bind(clear_btn, "<Button-1>", lambda e: self.parent.window.refresh_page())

    # File picker callback
    def on_file_picked(self, file_path : str):
        self.parent.vars["file_path"].set(file_path)

        nodes = file_to_matrix(file_path)
        self.create_graph(nodes)

        self.parent.vars["num_of_nodes"].set(len(nodes))
        self.parent.vars["message"].set("File " + file_path.split("/")[-1] + " loaded successfully")

        self.start_dropdown.config(values=[str(x+1) for x in range(len(nodes))])
        self.start_dropdown.state(["!disabled"])
        self.parent.vars["start_node"].set("Select Node")

        self.dest_dropdown.config(values=[str(x+1) for x in range(len(nodes))])
        self.dest_dropdown.state(["!disabled"])
        self.parent.vars["dest_node"].set("Select Node")
    
    def create_graph(self, nodes) :
        self.parent.graph_canvas = GraphCanvas(self.parent, nodes)
        self.parent.graph_canvas.grid(row=1, column=1, sticky="nsew")

"""Footer Component for Main Page"""
class MainPage_Footer(Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#07111F")
        self.parent = parent
        self.build()

    def build(self):
        # layout
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(1, weight=1, uniform="a")
        self.rowconfigure(2, weight=1, uniform="a")
        self.rowconfigure(3, weight=1, uniform="a")
        
        self.columnconfigure(0, weight=5, uniform="a")
        self.columnconfigure(1, weight=10, uniform="a")
        self.columnconfigure(2, weight=2, uniform="a")
        self.columnconfigure(3, weight=80, uniform="a")

        # create footer
        total_nodes_label = Label(self, text="Total Nodes : ", 
            font=("Montserrat", 12, "normal"), bg="#07111F", fg="white", anchor="w")
        total_nodes_label.grid(row=1, column=1, sticky="nsew", columnspan=2)

        total_nodes_value = Label(self, textvariable=self.parent.vars["num_of_nodes"],
            font=("Montserrat", 12, "normal"), bg="#07111F", fg="#E2BD45", anchor="w")
        total_nodes_value.grid(row=1, column=3, sticky="nsew")

        message_label = Label(self, text="Message : ",
            font=("Montserrat", 12, "normal"), bg="#07111F", fg="white", anchor="w")
        message_label.grid(row=2, column=1, sticky="nsew")

        message_value = Label(self, textvariable=self.parent.vars["message"],
            font=("Montserrat", 12, "normal"), bg="#07111F", fg="white", anchor="w")
        message_value.grid(row=2, column=2, sticky="nsew", columnspan=2)
                            
""" Main Page for File Input Mode"""
class MainPage_MapPick(Frame):
    def __init__(self, window : IMainWindow):
        super().__init__(window)
        self.window = window
        self.assets = []
        self.markers = []

        # dropdown options
        self.vars = {
            "start_node": StringVar(value="Select 5 Nodes or More"),
            "dest_node": StringVar(value="Select 5 Nodes or More"),
            "algorithm": StringVar(value="Not Selected"),
            "num_of_nodes": IntVar(value=0),
            "message": StringVar(value="Select at least 5 nodes before running the algorithm"),
        }

        self.start_dropdown : Combobox = None
        self.dest_dropdown : Combobox = None

        self.build()
    
    def build(self):
        # layout
        self.rowconfigure(0, weight=2, uniform="a")
        self.rowconfigure(1, weight=8, uniform="a")
        self.rowconfigure(2, weight=2, uniform="a")
        self.columnconfigure(0, weight=3, uniform="a")
        self.columnconfigure(1, weight=7, uniform="a")

        # header
        header = MainPage_Header(self)
        header.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # body
        body = MainPage_MapPick_Body(self)
        body.grid(row=1, column=0, rowspan=2, sticky="nsew")
        self.start_dropdown = body.start_dropdown
        self.dest_dropdown = body.dest_dropdown

        # map view
        map_view = MapView(self)
        map_view.grid(row=1, column=1, sticky="nsew")

        # footer
        footer = MainPage_Footer(self)
        footer.grid(row=2, column=1, sticky="nsew")

    def run_algorithm(self):
        if self.vars["start_node"].get() == "Select Node" or self.vars["dest_node"].get() == "Select Node":
            self.vars["message"].set("Please select a start and destination node")
            messagebox.showerror("Error", "Please select a start and destination node")
            return
        elif self.vars["algorithm"].get() == "Not Selected":
            self.vars["message"].set("Please select the search algorithm")
            messagebox.showerror("Error", "Please select the search algorithm")
            return
        else:
            self.vars["message"].set("Running Algorithm...")
            if self.vars["algorithm"].get() == "Uniform-Cost Search":
                print("Uniform-Cost Search")
            elif self.vars["algorithm"].get() == "A* Search":
                print("A* Search")

    def on_marker_added(self):
        self.vars["num_of_nodes"].set(len(self.markers))
        if len(self.markers) >= 5:
            self.start_dropdown.config(values=[str(x+1) for x in range(len(self.markers))])
            self.start_dropdown.state(["!disabled"])
            self.vars["start_node"].set("Select Node")

            self.dest_dropdown.config(values=[str(x+1) for x in range(len(self.markers))])
            self.dest_dropdown.state(["!disabled"])
            self.vars["dest_node"].set("Select Node")

            self.vars["message"].set("Keep adding nodes or run the algorithm")

"""Body Component for Main Page (Map Pick Mode)"""
class MainPage_MapPick_Body(Canvas):
    def __init__(self, parent):
        super().__init__(parent)
        change_background(self, "main_page/body-bg.png")
        self.parent = parent

        self.start_dropdown : Combobox = None
        self.dest_dropdown : Combobox = None

        self.build()

    def build(self):
        builder_dropdown = DropdownBuilder(self)

        # Create dropdowns
        self.start_dropdown = builder_dropdown.create("Starting Node", [], 40, 40, self.parent.vars["start_node"])
        self.start_dropdown.state(["disabled"])

        self.dest_dropdown = builder_dropdown.create("Destination Node", [], 40, 140, self.parent.vars["dest_node"])
        self.dest_dropdown.state(["disabled"])
        
        builder_dropdown.create("Algorithm", ["Uniform-Cost Search", "A* Search"], 40, 240, self.parent.vars["algorithm"])

        # Start button
        self.create_text(40, 355, text="Start Finding", font=("Montserrat", 16, "bold"), fill="white", anchor="nw")   
        img_start_btn = add_img(self, "main_page/start-button.png", 1)
        start_btn = self.create_image(200, 350, image=img_start_btn, anchor="nw")
        self.tag_bind(start_btn, "<Button-1>", lambda e: self.parent.run_algorithm())

        # Clear button
        self.create_text(40, 405, text="Clear", font=("Montserrat", 16, "bold"), fill="white", anchor="nw")
        img_clear_btn = add_img(self, "main_page/clear-button.png", 1)
        clear_btn = self.create_image(200, 400, image=img_clear_btn, anchor="nw")
        self.tag_bind(clear_btn, "<Button-1>", lambda e: self.parent.window.refresh_page())
