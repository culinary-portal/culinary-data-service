from psycopg2 import Error
from ConnectionToDatabase import Database


class Populator():
    def __init__(self):
        self.database = Database("postgres", "postgres", "postgres", "localhost", 5432)
        self.connection = self.database.connect()
        self.cursor = self.connection.cursor()

    def populate(self, table_name, row):
        try:
            query = f"INSERT INTO {table_name}(name) VALUES ({row});"
            print(query)
            self.cursor.execute(query)
            self.connection.commit()
        except Error as e:
            print(f"Error while inserting {e}")
            self.cursor.close()
            self.connection.close()
        self.cursor.close()
        self.connection.close()
