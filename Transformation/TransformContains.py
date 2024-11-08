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
            'port': '5432'
        }

    def transform_data(self, response, iterator):
        # Fetch recipe and ingredient names
        recipe_name = response.get('strMeal', '').replace("'", "")
        ingredient_name = response.get(f'strIngredient{iterator + 1}', '').replace("'", "")

        # Fetch the IDs for recipe and ingredient
        recipe_id = self.get_id("recipe", "recipe_id", recipe_name)
        ingredient_id = self.get_id("ingredient", "ingredient_id", ingredient_name)

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

    def extract_quantity_and_unit(self, how_much):
        # Regular expressions for quantity (including fractions) and units
        quantity_pattern = re.compile(r"(?P<quantity>\d+[\d./¼¾½]*[-\d½]*)")
        unit_pattern = re.compile(r"(?P<unit>[a-zA-Z]+)")

        # Match patterns for quantity and unit
        quantity_match = quantity_pattern.match(how_much)
        unit_match = unit_pattern.search(how_much)

        # Parse the quantity and unit
        quantity = quantity_match.group('quantity').strip() if quantity_match else -1
        unit = unit_match.group('unit').strip() if unit_match else "N/A"

        return quantity, unit
