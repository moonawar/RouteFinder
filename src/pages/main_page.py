from tkinter import Frame, Canvas, StringVar, IntVar, Label
from tkinter.ttk import Combobox
from utils.canvas_utils import *
from utils.file_reader import *
from utils.element_builder import DropdownBuilder, FilePickerBuilder
from utils.graph_drawer import GraphCanvas
from window.i_main_window import IMainWindow

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
            "message": StringVar(value="Load File First"),
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
        header = MainPage_FileInput_Header(self)
        header.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # body
        body = MainPage_FileInput_Body(self)
        body.grid(row=1, column=0, rowspan=2, sticky="nsew")

        # footer
        footer = MainPage_FileInput_Footer(self)
        footer.grid(row=2, column=1, sticky="nsew")

class MainPage_FileInput_Header(Canvas):
    def __init__(self, parent):
        super().__init__(parent, bg="#07111F")
        self.build()

    def build(self):
        self.create_text(40, 35, text="Route Finder", font=("Montserrat", 32, "bold"), fill="#E2BD45", anchor="nw")
        
        add_img(self, "main_page/header-logo.png")
        self.create_image(1000, 30, image=self.master.assets[-1], anchor="nw")

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

        self.start_dropdown.config(values=[str(x+1) for x in range(len(nodes))])
        self.start_dropdown.state(["!disabled"])
        self.parent.vars["start_node"].set("Select Node")

        self.dest_dropdown.config(values=[str(x+1) for x in range(len(nodes))])
        self.dest_dropdown.state(["!disabled"])
        self.parent.vars["dest_node"].set("Select Node")
    
    def create_graph(self, nodes) :
        self.parent.graph_canvas = GraphCanvas(self.parent, nodes)
        self.parent.graph_canvas.grid(row=1, column=1, sticky="nsew")

class MainPage_FileInput_Footer(Frame):
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
                              