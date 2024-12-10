import psycopg2
from psycopg2 import Error
import os
from dotenv import load_dotenv

load_dotenv()


class TransformRecipe:
    def __init__(self):
        self.table_name = "recipe"
        self.params = {
            'dbname': os.getenv('GCP_DB_NAME'),
            'user': os.getenv('GCP_DB_USER'),
            'password': os.getenv('GCP_DB_PASSWORD'),
            'host': os.getenv('GCP_DB_HOST'),
            'port': os.getenv('GCP_DB_PORT')
        }

    def transform_data(self, response):
        # map the fields
        if response is not None:
            print(response.get('strMeal'))
            name = response['strMeal'].replace("'", "")
            id_general_recipe = self.get_id_recipe(name.replace("'", ""))
            if id_general_recipe is not None:
                row = f"DEFAULT, '{id_general_recipe}', '{name}', NULL, NULL"
                return row
        return False

    def get_id_recipe(self, recipe_name):
        query = "SELECT general_recipe_id FROM general_recipe WHERE name = %s"
        result = self.fetch_single_result(query, recipe_name)
        return result[0] if result else None

    def fetch_single_result(self, query, params):
        try:
            with psycopg2.connect(**self.params) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    return cursor.fetchone()
        except Error as e:
            print(f"Database error occurred: {e}")
            return None


