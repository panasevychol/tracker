import logging

import gui
import database

class App:

    def __init__(self):
        self.logger = logging.basicConfig(level='DEBUG')
        self.gui = gui.GUI(self)
        self.database_master = database.DatabaseMaster()

    def run(self):
        self.gui.run()

    def quit(self):
        pass