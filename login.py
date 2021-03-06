import logging

class LoginMaster:

    def __init__(self, app):
        self.logger = logging.getLogger('app')
        self.user = None
        self.app = app
        self.db_master = self.app.database_master

    def login_user(self, login, password):
        error = self.db_master.login_user(login, password)
        if error:
            self.logger.info('Login failed. ' + error)
            return error
        else:
            self.user = login
            self.logger.info('Successfully login from ' + login)

    def register_user(self, login, password):
        error = self.db_master.add_user(login, password)
        if not error:
            self.login_user(login, password)
        else:
            return error

    def logout_user(self):
        self.user = None

    def get_users_list(self):
        users = self.db_master.get_all_logins()
        return users
