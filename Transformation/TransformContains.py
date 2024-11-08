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
        # Attempt to fetch recipe_id and ingredient_id
        recipe_name = response.get('strMeal', '').replace("'", "")
        ingredient_name = response.get(f'strIngredient{iterator + 1}', '').replace("'", "")

        # Debugging: Print the names being processed
        print(f"Processing Recipe: {recipe_name}, Ingredient: {ingredient_name}")

        recipe_id = self.get_id_recipe(recipe_name)
        ingredient_id = self.get_id_ingredient(ingredient_name)

        # Check if IDs are valid
        if recipe_id is None or ingredient_id is None:
            print(f"Missing ID - Recipe ID: {recipe_id}, Ingredient ID: {ingredient_id}")
            return None

        # Get measurement and extract quantity and unit
        how_much = response.get(f'strMeasure{iterator + 1}', "")
        print(f"Measurement for ingredient {ingredient_name}: {how_much}")

        quantity_pattern = re.compile(r"(?P<quantity>\d+[\d./¼¾½]*[-\d½]*)")
        unit_pattern = re.compile(r"(?P<unit>[a-zA-Z]+)")

        quantity_match = quantity_pattern.match(how_much)
        unit_match = unit_pattern.search(how_much)

        # Assign the extracted quantity and unit, or set defaults if not found
        quantity = quantity_match.group('quantity').strip() if quantity_match else -1
        unit = unit_match.group('unit').strip() if unit_match else "N/A"

        print(
            f"Transformed Data - Quantity: {quantity}, Unit: {unit}, Recipe ID: {recipe_id[0]}, Ingredient ID: {ingredient_id[0]}")
        return f"DEFAULT, {quantity}, '{unit}',{recipe_id[0]}, {ingredient_id[0]}"

    def get_id_recipe(self, recipe_name):
        try:
            connection = psycopg2.connect(**self.params)
            cursor = connection.cursor()
            cursor.execute("SELECT recipe_id FROM recipe WHERE name = %s", (recipe_name,))
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
