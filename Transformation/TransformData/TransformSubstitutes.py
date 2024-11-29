import psycopg2
import csv
import os
from dotenv import load_dotenv

load_dotenv()


class TransformSubstitutes(object):
    def __init__(self):
        self.table_name = "contains"
        self.params = {
            'dbname': os.getenv('GCP_DB_NAME'),
            'user': os.getenv('GCP_DB_USER'),
            'password': os.getenv('GCP_DB_PASSWORD'),
            'host': os.getenv('GCP_DB_HOST'),
            'port': os.getenv('GCP_DB_PORT')
        }
        print(self.params)
        self.substitutes_map = 'Transformation/ClearData/substitutes_map.txt'

    def transform_data(self):
        # fetch the ingredients ids
        with open(self.substitutes_map, mode='r', encoding='utf-8') as file:
            csvFile = csv.reader(file)
            ingredient_1 = ''
            ingredient_2 = ''
            with open("substitutes.txt", "w", encoding='utf-8') as substitutes_file:
                for lines in csvFile:
                    print(lines)
                    ingredient_1 = lines[0].lower().replace("'", "") \
                        .replace(",", "")
                    ingredient_2 = lines[1].lower().replace("'", "") \
                        .replace(",", "")
                    id_ingredient_1 = self.get_id("ingredient", "ingredient_id", ingredient_1.replace("'", ""))
                    id_ingredient_2 = self.get_id("ingredient", "ingredient_id", ingredient_2.replace("'", ""))

                    if id_ingredient_1 is None or id_ingredient_2 is None:
                        print(f"Missing ID for {id_ingredient_1} or {id_ingredient_2}")
                        return
                    else:
                        print(f"{ingredient_1} : {id_ingredient_1}")
                        print(f"{ingredient_2} : {id_ingredient_2}")
                        substitutes_file.write(f"DEFAULT, {id_ingredient_1}, {id_ingredient_2} \n")
                return

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
