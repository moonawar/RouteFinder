from tkinter import Canvas
from PIL import ImageTk, Image

# notice : image_path is relative to asset folder
def change_background(canvas : Canvas, image_path : str):
    canvas.master.assets.append(ImageTk.PhotoImage(Image.open("../asset/" + image_path)))
    canvas.create_image(0, 0, image=canvas.master.assets[-1], anchor="nw")

def add_img (canvas : Canvas, image_path : str, size_factor = 1):
    img = Image.open("../asset/" + image_path)
    img = img.resize((int(img.width * size_factor), int(img.height * size_factor)), Image.ANTIALIAS)
    canvas.master.assets.append(ImageTk.PhotoImage(img))
    return canvas.master.assets[-1]

def make_button(canvas : Canvas, tag : str, callback, change_cursor = True):
    canvas.tag_bind(tag, "<Button-1>", callback)
    if change_cursor:
        canvas.tag_bind(tag, "<Enter>", lambda e: canvas.config(cursor="hand2"))
        canvas.tag_bind(tag, "<Leave>", lambda e: canvas.config(cursor=""))