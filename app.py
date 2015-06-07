import logging
import sys

import gui
import database
import login
import tasks

class App:

    @staticmethod
    def get_logger(name):
        logger = logging.getLogger(name)
        std_handler = logging.StreamHandler()
        logger.addHandler(std_handler)
        return logger

    def __init__(self, debug=False):
        self.logger = self.get_logger('app')
        if debug:
            self.logger.setLevel('DEBUG')
        else:
            self.logger.setLevel('INFO')
        self.logger.info('Tracker is started!')
        self.database_master = database.DatabaseMaster()
        self.login_master = login.LoginMaster(self)
        self.task_master = tasks.TaskMaster(self)
        self.gui = gui.GUI(self)

    def run(self):
        self.gui.run()

    def quit(self):
        self.database_master.quit()
        self.logger.info('Goodbye!')
