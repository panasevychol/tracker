import sqlite3
import logging
import time

class DatabaseFramework:

    def __init__(self, database_name):
        self.logger = logging.getLogger('app')
        self.connect_to_database(database_name)

    def connect_to_database(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def create_table(self, table_name, relationship_options, **kwargs):
        columns = 'id integer'
        for key,value in kwargs.iteritems():
            columns += ', ' + key + ' ' + value
        if relationship_options:
            columns += ', ' + relationship_options
        sql = 'create table if not exists ' + table_name + '(' + columns + ')'
        self.commit_sql(sql)

    def insert_record(self, table, *args):
        values = ''
        for index, value in enumerate(args):
            if isinstance(value, str):
                values += '"' + value + '"'
            else:
                values += str(value)
            if index < len(args)-1:
                values += ', '
        if values:
            values = str(self.get_next_value_id(table)) + ', ' + values
            sql = 'INSERT INTO ' + table + ' VALUES(' + values + ')'
            self.commit_sql(sql)

    def commit_sql(self,sql):
        self.logger.debug('Commiting SQL: ' + sql)
        self.cursor.execute(sql)
        self.connection.commit()

    def execute_sql(self, sql):
        self.logger.debug('Executing SQL: ' + sql)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_next_value_id(self, table):
        sql = 'SELECT Count(*) FROM ' + table
        self.cursor.execute(sql)
        result = self.cursor.fetchone()[0]
        return int(result) + 1

    def find_record(self, string, table, column):
        sql = 'select * from ' + table + ' where ' + column + ' like "%' + string + '%"'
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result

    def close(self):
        self.cursor.close()
        self.connection.close()

    def get_relationship_command(self, daughter_table_column, mother_table, mother_table_column):
        return 'FOREIGN KEY('+ daughter_table_column + ') REFERENCES '+ mother_table + '(' + mother_table_column + ')'


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
        user_record = self.find_record(login, self.USERS_TABLE_NAME, 'login')
        if user_record:
            if password == str(user_record[-2]):
                return
            else:
                return 'Incorrect password'
        else:
            return 'User not found'

    def add_user(self, login, password, admin_rights=0):
        if not self.find_record(login, self.USERS_TABLE_NAME, 'login'):
            self.insert_record(self.USERS_TABLE_NAME, login, password, admin_rights)
        else:
            return 'User already exists'

    def get_all_logins(self):
        sql = 'SELECT login FROM ' + self.USERS_TABLE_NAME
        logins = self.execute_sql(sql)
        print(logins)
        return tuple(logins)

    def create_all_tables(self):
        self.create_users_table()
        self.create_tasks_table()

    def create_users_table(self):
        columns = {'login': 'string', 'password': 'string', 'admin_rights': 'integer'}
        self.create_table(self.USERS_TABLE_NAME, None, **columns)

    def create_tasks_table(self):
        columns = {'name': 'string', 'text': 'string', 'owner_id': 'integer', 'state': 'integer', 'timestamp' : 'string'}
        relationship_options = self.get_relationship_command('owner_id', self.USERS_TABLE_NAME, 'id')
        self.create_table(self.TASKS_TABLE_NAME, relationship_options, **columns)

    def create_task(self, name, text, owner, state):
        owner_id = self.find_record(owner,self.USERS_TABLE_NAME, 'login')[0]
        self.insert_record(self.TASKS_TABLE_NAME, name, text, owner_id, state, time.ctime())