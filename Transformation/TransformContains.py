import psycopg2
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
        # Get recipe and ingredient IDs
        recipe_id = self.get_id_recipe(response['strMeal'].replace("'", ""))
        ingredient_id = self.get_id_ingredient(response[f'strIngredient{iterator + 1}'].replace("'", ""))
        if recipe_id is None or ingredient_id is None:
            print("Recipe or ingredient ID not found.")
            return None

        # Extract quantity and unit from 'how_much' string
        how_much = response[f'strMeasure{iterator + 1}']
        quantity_pattern = re.compile(r"(?P<quantity>\d+[\d./¼¾½]*[-\d½]*)")
        unit_pattern = re.compile(r"(?P<unit>[a-zA-Z]+)")

        quantity_match = quantity_pattern.match(how_much)
        unit_match = unit_pattern.search(how_much)

        # Assign the extracted quantity and unit, or set defaults if not found
        quantity = quantity_match.group('quantity').strip() if quantity_match else -1
        unit = unit_match.group('unit').strip() if unit_match else "N/A"

        return f"DEFAULT, {quantity}, '{unit}',{recipe_id[0]}, {ingredient_id[0]}"

    def get_id_recipe(self, recipe_name):
        try:
            connection = psycopg2.connect(**self.params)
            cursor = connection.cursor()
            cursor.execute("SELECT general_recipe_id FROM general_recipe WHERE name = %s", (recipe_name,))
            row = cursor.fetchone()
            cursor.close()
            connection.close()
            return row
        except Exception as e:
            print(f"Error fetching recipe ID for '{recipe_name}': {e}")
            return None

    def get_id_ingredient(self, ingredient_name):
        try:
            connection = psycopg2.connect(**self.params)
            cursor = connection.cursor()
            cursor.execute("SELECT ingredient_id FROM ingredient WHERE name = %s", (ingredient_name,))
            row = cursor.fetchone()
            cursor.close()
            connection.close()
            return row
        except Exception as e:
            print(f"Error fetching ingredient ID for '{ingredient_name}': {e}")
            return None
