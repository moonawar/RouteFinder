from window.i_main_window import IMainWindow
from pages.starting_page import StartingPage
from pages.main_page import MainPage_FileInput, MainPage_MapPick

class MainWindow(IMainWindow):
    def __init__(self):
        super().__init__()
        
        # window layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        # init pages
        self.pages = {
            "StartingPage": StartingPage(self),
            "MainPage_FileInput": MainPage_FileInput(self),
            "MainPage_MapPick": MainPage_MapPick(self)
        }

        self.opened_page = self.pages["MainPage_MapPick"]
        self.opened_page.grid(row=0, column=0, sticky="nsew")

    def open_page(self, page_name):
        # change opened page
        self.opened_page.grid_forget()
        self.opened_page = self.pages[page_name]
        self.opened_page.grid(row=0, column=0, sticky="nsew")

    def refresh_page(self):
        new_page = self.opened_page.__class__(self)
        self.pages[self.opened_page.__class__.__name__] = new_page
        self.open_page(self.opened_page.__class__.__name__)