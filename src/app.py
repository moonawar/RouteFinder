from window.main_window import MainWindow
import sys


app : MainWindow = None

def on_app_close():
    app.quit()
    sys.exit()

if __name__ == "__main__":
    app = MainWindow()
    app.protocol("WM_DELETE_WINDOW", on_app_close)
    app.mainloop()