import logging

import gui
import database
import login
import tasks

class App:

    def __init__(self):
        self.logger = logging.basicConfig(level='DEBUG')
        self.database_master = database.DatabaseMaster()
        self.login_master = login.LoginMaster(self)
        self.task_master = tasks.TaskMaster(self)
        self.gui = gui.GUI(self)

    def run(self):
        self.gui.run()

    def quit(self):
        pass