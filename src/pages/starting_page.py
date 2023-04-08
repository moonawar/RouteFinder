from tkinter import Frame, Canvas
from utils.canvas_utils import *
from window.i_main_window import IMainWindow

class StartingPage(Frame):
    def __init__(self, window : IMainWindow):
        super().__init__(window)
        self.window = window
        self.assets = []
        self.build()
    
    def build(self):
        page_canvas = Canvas(self)
        page_canvas.place(x=-10, y=-10, relwidth=1.1, relheight=1.1)
        change_background(page_canvas, "starting_page/bg.png")
        
        # title
        page_canvas.create_text(120, 165, text="Route Finder", font=("Montserrat", 32, "bold"), fill="#E2BD45", anchor="nw")

        # title description
        page_canvas.create_text(120, 230, font=("Montserrat", 16, "bold"), fill="white", anchor="nw", width=480,
            text="Route finder application with uniform cost search algorithm and A* algorithm")
        
        # button
        page_canvas.create_text(120, 350, font=("Montserrat", 16, "bold"), fill="white", anchor="nw",
            text="Choose your mode:")

        # button 1 : file input
        add_img(page_canvas, "starting_page/file-input-btn.png")
        btn1 = page_canvas.create_image(120, 400, image=self.assets[-1], anchor="nw")
        page_canvas.tag_bind(btn1, "<Button-1>", lambda e: self.window.open_page("MainPage_FileInput"))

        # btn1 desc
        page_canvas.create_text(120, 465, font=("Montserrat", 12, "normal"), fill="white", anchor="nw", width = 200,
            text="Insert your map from an adjacency matrix in .txt file")

        # button 2 : map pick
        add_img(page_canvas, "starting_page/map-pick-btn.png")
        btn2 = page_canvas.create_image(375, 400, image=self.assets[-1], anchor="nw")
        page_canvas.tag_bind(btn2, "<Button-1>", lambda e: self.window.open_page("MainPage_MapPick"))

        # btn2 desc
        page_canvas.create_text(375, 465, font=("Montserrat", 12, "normal"), fill="white", anchor="nw", width = 200,
            text="Pick points from map with google map API")
        
        # footer
        page_canvas.create_text(120, 600, font=("Montserrat", 12, "normal"), fill="white", anchor="nw",
            text="Athif Nirwasito - 13521053")
        page_canvas.create_text(120, 625, font=("Montserrat", 12, "normal"), fill="white", anchor="nw",
            text="Addin Munawwar Yusuf - 13521085")
        
        # logo big
        add_img(page_canvas, "starting_page/logo-big.png", 0.9)
        page_canvas.create_image(650, 100, image=self.assets[-1], anchor="nw")
