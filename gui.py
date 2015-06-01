from Tkinter import *

class GUI:

    def __init__(self, app):
        self.app = app
        self.base = Tk()
        self.setup_main_window()

    def setup_main_window(self):
        self.base.resizable(width=FALSE, height=FALSE)

    def run(self):
        self.base.mainloop()
        self.app.quit()