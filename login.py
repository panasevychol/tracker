import logging

class LoginMaster:

    def __init__(self, app):
        self.logger = logging.getLogger('app')
        self.app = app
        self.db_master = self.app.database_master

    def login_user(self, login, password):
        error = self.db_master.login_user(login, password)
        if error:
            self.logger.info('Login failed. ' + error)
        else:
            return login

    def add_user(self, login, password):
        error = self.db_master.add_user(login, password)
        if not error:
            self.login_user(login, password)
        else:
            return error
