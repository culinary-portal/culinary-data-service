import psycopg2
from psycopg2 import Error

class TransformRecipe:
    def __init__(self):
        self.table_name = "recipe"
        self.params = {
            'dbname': 'postgres',
            'user': 'postgres',
            'password': 'postgres',
            'host': 'localhost',
            'port': '5432'
        }

    def transform_data(self, response):
        if response.get('strMeal') is not None:
            name = response['strMeal'].replace("'", "")
            id_general_recipe = self.get_id_recipe(name)
            if id_general_recipe is not None:
                row = f"DEFAULT, '{id_general_recipe}', '{name}', 'NULL', NULL"
                return row
        return False

    def get_id_recipe(self, recipe_name):
        query = "SELECT general_recipe_id FROM general_recipe WHERE name = %s"
        result = self._fetch_single_result(query, (recipe_name,))
        return result[0] if result else None

    def get_id_diet_type(self, diet_type):
        query = "SELECT general_recipe_id FROM general_recipe WHERE name = %s"
        result = self._fetch_single_result(query, (diet_type,))
        return result[0] if result else None

    def _fetch_single_result(self, query, params):
        try:
            with psycopg2.connect(**self.params) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    return cursor.fetchone()
        except Error as e:
            print(f"Database error occurred: {e}")
            return None
