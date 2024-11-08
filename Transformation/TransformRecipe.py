from psycopg2 import Error
import json
import psycopg2


class TransformRecipe:
    def __init__(self):
        self.table_name = "recipe"
        self.params = {
            'dbname': 'postgres',
            'user': 'postgres',
            'password': 'postgres',
            'host': 'localhost',
            'port': '5432'}

    def transform_data(self, response):
        if response['strMeal'] is not None:
            name = response['strMeal'].replace("'", "")
            id_general_recipe = self.get_id_recipe(name)[0]
            row = f"DEFAULT, '{id_general_recipe}' ,'{name}' , 'NULL' , NULL"
            return row
        else:
            return False

    def get_id_recipe(self, recipe_name):
        try:
            connection = psycopg2.connect(**self.params)
            cursor = connection.cursor()
            try:
                cursor.execute(f"SELECT general_recipe_id from general_recipe WHERE name = '{recipe_name}'")
                row = cursor.fetchone()
                return row
            except:
                cursor.close()
                connection.close()
        except:
            print("Error while fetching the data")

    def get_id_diet_type(self, diet_type):
        try:
            connection = psycopg2.connect(**self.params)
            cursor = connection.cursor()
            try:
                cursor.execute(f"SELECT general_recipe_id from general_recipe WHERE name = '{diet_type}'")
                row = cursor.fetchone()
                return row
            except:
                cursor.close()
                connection.close()
        except:
            print("Error while fetching the data")
