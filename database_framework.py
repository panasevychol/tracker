import sqlite3
import logging

class DatabaseFramework:

    def __init__(self, database_name):
        self.logger = logging.getLogger('app')
        self.connect_to_database(database_name)

    def connect_to_database(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def create_table(self, table_name, relationship_options, columns_string):
        columns_string = 'id integer, ' + columns_string
        if relationship_options:
            columns_string += ', ' + relationship_options
        sql = 'create table if not exists ' + table_name + '(' + columns_string + ')'
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
        string, table, column = str(string), str(table), str(column)
        self.logger.debug('Searching for "' + string + '" in table "' + table + '", column "' + column + '".')
        sql = 'select * from ' + table + ' where ' +  column + ' like "%' + string + '%"'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def quit(self):
        self.cursor.close()
        self.connection.close()

    def get_relationship_command(self, daughter_table_column, mother_table, mother_table_column):
        return 'FOREIGN KEY('+ daughter_table_column + ') REFERENCES '+ mother_table + '(' + mother_table_column + ')'