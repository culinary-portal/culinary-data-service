from connection_to_db import Database
from psycopg2 import Error
from get_data import CulinaryDataService


class PopulateGeneralRecipe:
    def __init__(self):
        self.database = Database("postgres", "postgres", "postgres", "localhost", 5432)
        self.connection = self.database.connect()
        self.cursor = self.connection.cursor()
        self.starting_id = 52767
        self.number_of_meals = 317
        self.table_name = None
        self.row = ""

    def transform_data(self, iterator):
        data_service = CulinaryDataService("https://www.themealdb.com/api")
        json_response = data_service.get_method(f"json/v1/1/lookup.php?i={self.starting_id + iterator}")
        print(json_response)
        if json_response['meals'] is None:
            print("No data")
            return None
        else:
            name = f"{json_response['meals'][0]['strMeal']}".replace("","")
            self.row += name.replace("'","")
            self.row = "'" + self.row + "'"
            return True

    def populate(self, table_name):
        for i in range(self.number_of_meals):
            if self.transform_data(i) is not None:
                self.table_name = table_name
                try:
                    query = f"INSERT INTO {self.table_name}(name) VALUES ({self.row});"
                    print(query)
                    self.cursor.execute(query)
                    self.connection.commit()
                except Error as e:
                    print("Error while inserting")
                    self.cursor.close()
                    self.connection.close()
            else:
                print(f"missing data for  id{self.starting_id + i}")
            self.row = ""
        self.cursor.close()
        self.connection.close()