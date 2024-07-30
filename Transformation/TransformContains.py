import psycopg2
import json
import re

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
        ingredient_id = self.get_id_ingredient(response[f'strIngredient{iterator + 1}'].replace("'", ""))
        how_much = response[f'strMeasure{iterator + 1}']

        # regular expression for extracting quantity/ unit
        quantity_pattern = re.compile(r"(?P<quantity>\d+[\d./¼¾½]*[-\d½]*)")
        unit_pattern = re.compile(r"(?P<unit>[a-zA-Z]+)")
        #checking
        quantity_match = quantity_pattern.match(how_much)
        unit_match = unit_pattern.search(how_much)
        # assigning the result
        quantity = quantity_match.group('quantity').strip() if quantity_match else "N/A"
        unit = unit_match.group('unit').strip() if unit_match else "N/A"

        print(quantity, unit)
        print(recipe_id)
        print(ingredient_id)
        return f"DEFAULT, {quantity}, '{unit}',{recipe_id[0]}, {ingredient_id[0]}"

    def get_id_recipe(self, recipe_name):
        print(recipe_name)
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

    def get_id_ingredient(self, ingredient_name):
        print(ingredient_name)
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
