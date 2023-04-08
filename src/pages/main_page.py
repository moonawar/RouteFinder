from tkinter import Frame, Canvas, OptionMenu, StringVar
from utils.canvas_utils import *
from window.i_main_window import IMainWindow

class MainPage_FileInput(Frame):
    def __init__(self, window : IMainWindow):
        super().__init__(window)
        self.window = window
        self.assets = []

        # dropdown options
        self.start_node = StringVar()
        self.start_node.set("Not Selected")
        self.dest_node = StringVar()
        self.dest_node.set("Not Selected")
        self.algorithm = StringVar()
        self.algorithm.set("Not Selected")

        self.build()
    
    def build(self):
        # layout
        self.rowconfigure(0, weight=2, uniform="a")
        self.rowconfigure(1, weight=9, uniform="a")
        self.rowconfigure(2, weight=1, uniform="a")
        self.columnconfigure(0, weight=3, uniform="a")
        self.columnconfigure(1, weight=7, uniform="a")

        # header
        header = MainPage_FileInput_Header(self)
        header.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # body
        body = MainPage_FileInput_Body(self)
        body.grid(row=1, column=0, rowspan=2, sticky="nsew")

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
        self.build()

    def build(self):
        builder = DropdownBuilder(self)

        builder.create("Starting Node", ["A", "B", "C"], 40, 40, self.parent.start_node)
        builder.create("Destination Node", ["A", "B", "C"], 40, 140, self.parent.dest_node)
        builder.create("Algorithm", ["A", "B", "C"], 40, 240, self.parent.algorithm)


        # Start button
        self.create_text(40, 400, text="Start Finding", font=("Montserrat", 16, "bold"), fill="white", anchor="nw")   
        add_img(self, "main_page/start-button.png", 1)
        self.create_image(200, 400, image=self.master.assets[-1], anchor="nw")

        # Clear button
        self.create_text(40, 450, text="Clear", font=("Montserrat", 16, "bold"), fill="white", anchor="nw")
        add_img(self, "main_page/clear-button.png", 1)
        self.create_image(200, 450, image=self.master.assets[-1], anchor="nw")


class DropdownBuilder():
    def __init__(self, parent):
        self.parent = parent

    def create(self, title, options, x, y, setvar) -> None:
        self.parent.create_text(x, y, text=title, font=("Montserrat", 18, "bold"), fill="white", anchor="nw")
        option_menu = OptionMenu(self.parent, setvar, *options)
        option_menu.config(bg="white", fg="#07111F", font=("Montserrat", 12, "normal"), 
            highlightthickness=0, borderwidth=0, width=16)
        option_menu.place(x=x, y=y+40)
