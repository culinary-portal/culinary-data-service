import psycopg2
import re
from dotenv import load_dotenv
import os

load_dotenv()


class TransformContains:
    def __init__(self):
        self.table_name = "contains"
        self.params = {
            'dbname': os.getenv('GCP_DB_NAME'),
            'user': os.getenv('GCP_DB_USER'),
            'password': os.getenv('GCP_DB_PASSWORD'),
            'host': os.getenv('GCP_DB_HOST'),
            'port': os.getenv('GCP_DB_PORT')
        }

    def transform_data(self, response, iterator):
        # Fetch recipe and ingredient names
        recipe_name = response.get('strMeal', '').replace("'", "")
        ingredient_name = response.get(f'strIngredient{iterator + 1}', '').replace("'", "").replace(",", "").lower()

        # Fetch the IDs for recipe and ingredient
        recipe_id = self.get_id("recipe", "recipe_id", recipe_name)
        ingredient_id = self.get_id("ingredient", "ingredient_id", ingredient_name)

        if recipe_id is None:
            print(f"Missing Recipe ID: {recipe_id} , {recipe_name}")
            return False
        elif ingredient_id is None:
            print(f"Missing Ingredient ID: {ingredient_id}, {ingredient_name}")
            return False

        # Extract quantity and unit from the measure
        how_much = response.get(f'strMeasure{iterator + 1}', "")
        quantity, unit = self.extract_quantity_and_unit(how_much)

        # Prepare and return the transformed row
        print(
            f"Transformed Data - Quantity: {quantity}, Unit: {unit}, Recipe ID: {recipe_id}, "
            f"Ingredient ID: {ingredient_id}, recipe: {recipe_name}, ingredient_name: {ingredient_name}")
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

        unit_to_grams = {
            "g": 1,
            "grams": 1,
            "tsp": 5,
            "teaspoon": 5,
            "tblsp": 15,
            "tbsp": 15,
            "tbs": 15,
            "tablespoon": 15,
            "cup": 240,
            "cups": 240,
            "ml": 1,
            "mL": 1,
            "pinch": 0.36,
            "dash": 0.6,
            "kg": 1000,
            "lb": 454,
            "pounds": 454,
            "oz": 28.35,
            "ounces": 28.35,
            "l": 1000,
            "litre": 1000,
            "liter": 1000,
            "can": 400,
            "clove": 4,
            "cloves": 4,
            "large": 150,
            "medium": 100,
            "small": 50,
            "sprigs": 5,
            "bunch": 100,
            "packet": 200,
            "bag": 200,
            "scoop": 30,
            "handful": 30,
            "stick": 113,
            "knob": 10,
            "slice": 20,
            "head": 500,
            "pod": 0.5,
            "stalk": 30,
            "rashers": 15,
            "drops": 0.05,
            "quarts": 946,
            "qt": 946,
            "yolk": 17,
            "yolkes": 17,
            "n/a": "n/a"
        }
        print(quantity_match, unit_match)
        # Parse the quantity and unit
        quantity = quantity_match.group('quantity').strip() if quantity_match is not None else None
        unit = unit_match.group('unit').strip() if unit_match is not None else None
        print(quantity, unit)
        if quantity is None:
            quantity = -1
        if unit is None:
            unit = "n/a"

        # map unit to grams
        unit_to_grams = unit_to_grams.get(unit.lower(), "n/a")
        return quantity, unit_to_grams
