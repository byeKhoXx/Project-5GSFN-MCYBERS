import sqlite3
import os.path

class db_connection:
    connection = None

    def __init__(self):
        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "../analytics_db.db")
        self.connection = sqlite3.connect(db_path)

    def save_changes(self):
        self.connection.commit()
    
    def get_cursor(self):
        cursor = self.connection.cursor()
        return cursor

    def close_connection(self):
        self.connection.close()
