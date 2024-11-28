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
            ingredient_1 = ''
            ingredient_2 = ''
            for lines in csvFile:
                ingredient_1 = lines[0]
                ingredient_2 = lines[1]

                id_ingredient_1 = self.get_id("ingredient", "ingredient_id", ingredient_1)
                id_ingredient_2 = self.get_id("ingredient", "ingredient_id", ingredient_2)

                if id_ingredient_1 is None or id_ingredient_2 is None:
                    print(f"Missing ID for {id_ingredient_1} or {id_ingredient_2}")
                    return
                else:
                    print(f"{ingredient_1} : {id_ingredient_1}")
                    print(f"{ingredient_2} : {id_ingredient_2}")
                    return f"DEFAULT,{id_ingredient_1},{id_ingredient_1}"

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
