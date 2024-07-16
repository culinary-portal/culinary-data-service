from ConnectionToDatabase import Database
from psycopg2 import Error
import requests


class PopulateIngredient:
    def __init__(self):
        self.database = Database("postgres", "postgres", "postgres", "localhost", 5432)
        self.connection = self.database.connect()
        self.cursor = self.connection.cursor()
        self.starting_id = 52767
        self.number_of_meals = 317
        self.table_name = "ingredient"
        self.row = []
        self.ingredients_size = 20
        self.ninja_api_key = '0vZpAVmpN3ZDYCbMyvsPDQ==86dLn8e6GhCQXOIJ'

    def transform_data(self, iterator):
        data_service = CulinaryDataService("https://www.themealdb.com/api")
        json_response = data_service.get_method(f"json/v1/1/lookup.php?i={self.starting_id + iterator}")

        if json_response['meals'] is None:
            print("No data")
            return None
        else:
            for i in range(self.ingredients_size):
                ingredient = f"{json_response['meals'][0][f'strIngredient{i + 1}']}"
                print(ingredient)
                ingredient = ingredient.replace("'", "")
                self.row.append(ingredient)
            return True

    def get_micro_elements(self, ingredient):
        url = f"https://api.api-ninjas.com/v1/nutrition?query={ingredient}"
        response = requests.get(url, headers={'X-Api-Key': self.ninja_api_key}).json()
        print(response)
        fat = response[0]['fat_total_g']
        protein = response[0]['protein_g']
        carbohydrate = response[0]['carbohydrates_total_g']
        kcal = response[0]['calories']
        return fat, protein, carbohydrate, kcal

    def populate(self):
        for i in range(self.number_of_meals):
            if self.transform_data(i) is not None:
                for ingredient in self.row:
                    try:
                        fat, protein, carbohydrate, kcal = self.get_micro_elements(ingredient)
                        ingredient = "'" + ingredient + "'"
                        query = f'INSERT INTO {self.table_name} VALUES (DEFAULT,{ingredient},{fat},{protein},{carbohydrate},{kcal});'
                        print(query)
                        self.cursor.execute(query)
                        self.connection.commit()
                    except Error as e:
                        print("Error while inserting")
                        self.cursor.close()
                        self.connection.close()
            else:
                print(f"missing data for  id{self.starting_id + i}")
            self.row = []
        self.cursor.close()
        self.connection.close()
