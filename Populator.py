from psycopg2 import Error
import ConnectionToDatabase


class Populator():
    def __init__(self):
        self.database = ConnectionToDatabase.ConnectionToDatabase("postgres", "postgres", "postgres", "localhost", 5432)
        self.connection = self.database.connect()
        self.cursor = self.connection.cursor()

    def insert_row(self, table_name, row):
        try:
            query = f"INSERT INTO {table_name} VALUES ({row});"
            print(query)
            self.cursor.execute(query)
            self.connection.commit()
        except Error as e:
            print(f"Error while inserting {e}")
            self.cursor.close()
            self.connection.close()
        self.cursor.close()
        self.connection.close()
