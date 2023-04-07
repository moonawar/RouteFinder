from abc import ABC, abstractmethod
from tkinter import Tk
import ctypes

class IMainWindow(Tk, ABC):
    def __init__(self, *args, **kwargs):
        # init window
        super().__init__(*args, **kwargs)
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

        # window config
        super().title("USC and A* Route Finder")
        super().geometry("1200x720")
        super().resizable(False, False)

    @abstractmethod
    def open_page(self, page_name):
        pass