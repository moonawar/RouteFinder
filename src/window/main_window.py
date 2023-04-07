from window.i_main_window import IMainWindow
from pages.starting_page import StartingPage

class MainWindow(IMainWindow):
    def __init__(self):
        super().__init__()
        
        # window layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        # init pages
        self.pages = {
            "StartingPage": StartingPage(self),
            # "MainPage_FileInput": MainPage_FileInput(self),
            # "MainPage_MapPick": MainPage_GoogleMap(self)
        }

        self.opened_page = self.pages["StartingPage"]
        self.opened_page.grid(row=0, column=0, sticky="nsew")

    def open_page(self, page_name):
        # change opened page
        self.opened_page.grid_forget()
        self.opened_page = self.pages[page_name]
        self.opened_page.grid(row=0, column=0, sticky="nsew")