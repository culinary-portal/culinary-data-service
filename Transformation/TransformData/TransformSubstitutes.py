import psycopg2
import re
import csv

class TransformSubstitutes(object):
    def __init__(self):
        self.table_name = "contains"
        self.params = {
            'dbname': 'postgres',
            'user': 'postgres',
            'password': 'postgres',
            'host': 'localhost',
            'port': '5432'
        }
        self.substitutes_map = 'Transformation/ClearData/substitutes_map.txt.txt'

    def transform_data(self, response, iterator):
        # fetch the ingredients ids
        with open(self.substitutes_map, mode='r') as file:
            csvFile = csv.reader(file)
            for lines in csvFile:


        ingredient_1 = self.get_id("ingredient", "ingredient_id", recipe_name)
        ingredient_2 = self.get_id("ingredient", "ingredient_id", ingredient_name)

        if recipe_id is None or ingredient_id is None:
            print(f"Missing ID - Recipe ID: {recipe_id}, Ingredient ID: {ingredient_id}")
            return None

        # Extract quantity and unit from the measure
        how_much = response.get(f'strMeasure{iterator + 1}', "")
        quantity, unit = self.extract_quantity_and_unit(how_much)

        # Prepare and return the transformed row
        print(
            f"Transformed Data - Quantity: {quantity}, Unit: {unit}, Recipe ID: {recipe_id}, Ingredient ID: {ingredient_id}")
        return f"DEFAULT, {quantity}, '{unit}', {recipe_id}, {ingredient_id}"

    def get_id(self, table_name, id_column, name):
        query = f"SELECT {id_column} FROM {table_name} WHERE name = %s"
        try:
            with psycopg2.connect(**self.params) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (name,))
                    result = cursor.fetchone()
                    return result[0] if result else None
        except psycopg2.Error as e:
            print(f"Error fetching {id_column} for '{name}' in table '{table_name}': {e}")
            return None
