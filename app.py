import logging

import gui
import database
import login

class App:

    def __init__(self):
        self.logger = logging.basicConfig(level='DEBUG')
        self.gui = gui.GUI(self)
        self.database_master = database.DatabaseMaster()
        self.login_master = login.LoginMaster(self)

    def run(self):
        self.gui.run()

    def quit(self):
        pass