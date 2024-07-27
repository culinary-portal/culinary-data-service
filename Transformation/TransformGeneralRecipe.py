from psycopg2 import Error
import json


class TransformGeneralRecipe:
    def __init__(self):
        self.table_name = "generalrecipe"

    def transform_data(self, response):
        row = ""
        if response['strMeal'] is not None:
            name = response['strMeal']
            row += name.replace("'", "")
            row = "DEFAULT," "'" + row + ",NULL,NULL,NULL" "'"
            return row
        else:
            return False
