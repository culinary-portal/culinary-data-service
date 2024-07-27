import psycopg2
import json


class TransformGeneralRecipe:
    def __init__(self):
        self.table_name = "contains"
        self.params = {
            'dbname': 'postgres',
            'user': 'postgres',
            'password': 'postgres',
            'host': 'localhost',
            'port': '5432'}

    def transform_data(self, response, iterator):
        recipe_name = response['strMeal']
        recipe_name = recipe_name.replace("'", "")
        ingredient_name = response[f'strIngredient{iterator+1}']

    def get_id_recipe(self, recipe_name):
        try:
            connection = psycopg2.connect(**self.params)
            cursor = connection.cursor()
            try:
                cursor.execute(f"SELECT general_recipe_id from general_recipes WHERE recipe_name = '{recipe_name}'")

    def get_id_ingredient(self, recipe_name):
        try:
            connection = psycopg2.connect(**self.params)
            cursor = connection.cursor()
            try:
                cursor.execute(f"SELECT general_recipe_id from general_recipes WHERE recipe_name = '{recipe_name}'")