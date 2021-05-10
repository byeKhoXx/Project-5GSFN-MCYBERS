import sqlite3

class db_connection:
    connection = None

    def __init__(self):
        self.connection = sqlite3.connect('analytics_db.db')

    def save_changes(self):
        self.connection.commit()
    
    def get_cursor(self):
        cursor = self.connection.cursor()
        return cursor

    def close_connection(self):
        self.connection.close()
