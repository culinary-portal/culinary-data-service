import psycopg2
import json


class TransformContains:
    def __init__(self):
        self.table_name = "contains"
        self.params = {
            'dbname': 'postgres',
            'user': 'postgres',
            'password': 'postgres',
            'host': 'localhost',
            'port': '5432'}

    def transform_data(self, response, iterator):
        recipe_id = self.get_id_recipe(response['strMeal'].replace("'", ""))
        ingredient_id = self.get_id_ingredient(response[f'strIngredient{iterator + 1}'])
        how_much = response[f'strMeasure{iterator + 1}'].split(" ")
        print(how_much)
        if len(how_much) > 1:
            measure = how_much[0]
            quantity = how_much[1]
        else:
            measure = how_much[0]
        #return f"{recipe_id[0]}, {ingredient_id[0]}"

    def get_id_recipe(self, recipe_name):
        try:
            connection = psycopg2.connect(**self.params)
            cursor = connection.cursor()
            try:
                cursor.execute(f"SELECT general_recipe_id from generalrecipe WHERE name = '{recipe_name}'")
                row = cursor.fetchone()
                return row
            except:
                cursor.close()
                connection.close()
        except:
            print("Error while fetching the data")

    def get_id_ingredient(self, ingredient_name):
        try:
            connection = psycopg2.connect(**self.params)
            cursor = connection.cursor()
            try:
                cursor.execute(f"SELECT ingredient_id from ingredient WHERE name = '{ingredient_name}'")
                row = cursor.fetchone()
                return row
            except:
                print("error 1 ")
        except:
            print("error 2")
