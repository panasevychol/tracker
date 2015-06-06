import sqlite3
import logging

class DatabaseFramework:

    def __init__(self, database_name):
        self.logger = logging.getLogger('app')
        self.connect_to_database(database_name)

    def connect_to_database(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def create_table(self, table_name, **kwargs):
        columns = 'id integer'
        for key,value in kwargs.iteritems():
            columns += ', ' + key + ' ' + value
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
        self.logger.debug('Executing SQL: ' + sql)
        self.cursor.execute(sql)
        self.connection.commit()

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


class DatabaseMaster(DatabaseFramework):

    DATABASE_NAME = 'tracker.db'
    USERS_TABLE_NAME = 'users'

    def __init__(self):
        DatabaseFramework.__init__(self, self.DATABASE_NAME)
        self.setup_database()

    def test(self):
        self.find_record('petro', self.USERS_TABLE_NAME, 'login')

    def setup_database(self):
        self.create_users_table()

    def login_user(self, login, password):
        user_record = self.find_record(login, self.USERS_TABLE_NAME, 'login')
        if user_record:
            if password == user_record[-1]:
                return
            else:
                return 'Incorrect password'
        else:
            return 'User not found'

    def add_user(self, login, password, admin_rights=False):
        if not self.find_record(login, self.USERS_TABLE_NAME, 'login'):
            self.insert_record(self.USERS_TABLE_NAME, login, password, admin_rights)
        else:
            return 'User already exists'

    def create_users_table(self):
        columns = {'login': 'string', 'password': 'string', 'admin': 'integer'}
        self.create_table(self.USERS_TABLE_NAME, **columns)