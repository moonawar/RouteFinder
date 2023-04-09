from tkinter import Canvas, filedialog
from tkinter.ttk import Combobox
from utils.canvas_utils import *
import os

class DropdownBuilder():
    def __init__(self, parent):
        self.parent = parent

    def create(self, title, options, x, y, setvar = None) -> None:
        self.parent.create_text(x, y, text=title, font=("Montserrat", 18, "bold"), fill="white", anchor="nw")
        
        option_menu = Combobox(self.parent, textvariable=setvar,
                values=options, state="readonly", font=("Montserrat", 12, "normal"), width=20)
        option_menu.place(x=x, y=y+40)

        return option_menu

class FilePickerBuilder():
    def __init__(self, parent : Canvas):
        self.parent = parent
        self.file_chosen_label = None

    def create(self, x, y) -> None:
        self.parent.create_text(x, y, text="Select Your File", font=("Montserrat", 18, "bold"), fill="white", anchor="nw")

        img_btn = add_img(self.parent, "main_page/file-choose-button.png", 1)
        btn = self.parent.create_image(x, y+40, image=img_btn, anchor="nw")
        make_button(self.parent, btn, lambda e: self.open_file_dialog())

        self.file_chosen_label = self.parent.create_text(x+175, y+50, text="No file chosen", font=("Montserrat", 12, "normal"), fill="white", anchor="nw")

    def open_file_dialog(self):
        starting_path = os.getcwd() + "../test/"
        try:
            file_path = filedialog.askopenfilename(
                initialdir = starting_path, title = "Select file", filetypes = (("Text files", "*.txt"), ("all files", "*.*")))
        except:
            return
        
        if file_path == "":
            return
        self.parent.itemconfig(self.file_chosen_label, text=self.file_path_to_file_name(file_path))
        self.parent.on_file_picked(file_path)
        

    def file_path_to_file_name(self, file_path):
        return file_path.split("/")[-1]