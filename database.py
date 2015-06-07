import time
from database_framework import DatabaseFramework

class DatabaseMaster(DatabaseFramework):

    DATABASE_NAME = 'tracker.db'
    USERS_TABLE_NAME = 'users'
    TASKS_TABLE_NAME = 'tasks'

    def __init__(self):
        DatabaseFramework.__init__(self, self.DATABASE_NAME)
        self.setup_database()

    def test(self):
        self.find_record('petro', self.USERS_TABLE_NAME, 'login')

    def setup_database(self):
        self.create_all_tables()

    def login_user(self, login, password):
        self.logger.debug('Searching for user record: ' + login)
        login, password = str(login), str(password)
        user_record = self.find_record(login, self.USERS_TABLE_NAME, 'login')
        if user_record:
            if password == str(user_record[0][-2]):
                return
            else:
                return 'Incorrect password'
        else:
            return 'User not found'

    def add_user(self, login, password, admin_rights=0):
        if self.find_record(login, self.USERS_TABLE_NAME, 'login'):
            return 'User already exists'
        self.insert_record(self.USERS_TABLE_NAME, login, password, admin_rights)

    def get_all_logins(self):
        sql = 'SELECT login FROM ' + self.USERS_TABLE_NAME
        logins = self.execute_sql(sql)
        return tuple(logins)

    def create_all_tables(self):
        self.create_users_table()
        self.create_tasks_table()

    def create_users_table(self):
        columns_string = 'login string, password string, admin_rights integer'
        self.create_table(self.USERS_TABLE_NAME, None, columns_string)

    def create_tasks_table(self):
        columns_string = 'name string, text string, owner_id integer, state integer, timestamp string'
        relationship_options = self.get_relationship_command('owner_id', self.USERS_TABLE_NAME, 'id')
        self.create_table(self.TASKS_TABLE_NAME, relationship_options, columns_string)

    def create_task(self, name, text, owner, state):
        name, text = str(name), str(text)
        search_result = self.find_record(name, self.TASKS_TABLE_NAME, 'name')
        print(search_result)
        if search_result:
            return 'Task "' + name + '" already exists'
        owner_id = self.find_record(owner,self.USERS_TABLE_NAME, 'login')[0][0]
        self.insert_record(self.TASKS_TABLE_NAME, name, text, owner_id, state, time.ctime())

    def get_user_tasks(self, login):
        owner_id = self.find_record(login, self.USERS_TABLE_NAME, 'login')[0][0]
        result = self.find_record(owner_id, self.TASKS_TABLE_NAME, 'owner_id')
        return result

    def get_task_record(self, task_name):
        result = self.find_record(task_name, self.TASKS_TABLE_NAME, 'name')
        if result:
            return result[0]
        self.logger.debug('Task "' + task_name + '" not found.')