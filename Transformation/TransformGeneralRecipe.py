from psycopg2 import Error
import json


class TransformGeneralRecipe:
    def __init__(self):
        self.table_name = "general_recipe"

    def transform_data(self, response):
        if response['strMeal'] is not None:
            row = ""
            name = response['strMeal'].replace("'", "")
            description = response['strInstructions'].replace("'", "")
            pho_url = response['strMealThumb'].replace("'", "")
            row = f" DEFAULT, '{name}' ,'{pho_url}' ,NULL, NULL, NULL, NULL, '{description}'"
            return row
        else:
            return False
