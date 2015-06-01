import sqlite3
import logging

class DatabaseMaster:

    DATABASE_NAME = 'tracker.db'

    def __init__(self):
        self.logger = logging.getLogger('app')
        self.connection = sqlite3.connect(self.DATABASE_NAME)
        self.cursor = self.connection.cursor()
        self.test()
        self.close()

    def test(self):
        self.create_table('users', **{'login': 'string', 'password': 'string'})
        self.insert_record('users', 2, 'Petro', 'ololo')


    def create_table(self, table_name, **kwargs):
        columns = 'id integer'
        for key,value in kwargs.iteritems():
            columns += ', ' + key + ' ' + value
        sql = 'create table if not exists ' + table_name + '(' + columns + ')'
        self.execute_sql(sql)

    def insert_record(self, table, *args):
        values = ''
        for index, value in enumerate(args):
            if isinstance(value, str):
                values += '"' + value + '"'
            else:
                values += str(value)
            if index < len(args)-1:
                values += ', '
        sql = 'INSERT INTO ' + table + ' VALUES(' + values + ')'
        self.execute_sql(sql)

    def execute_sql(self,sql):
        self.logger.info('Executing SQL: ' + sql)
        self.cursor.execute(sql)
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()