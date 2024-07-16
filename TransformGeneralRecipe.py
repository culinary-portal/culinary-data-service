from psycopg2 import Error
import json

class TransformGeneralRecipe:
    def __init__(self):
        self.iterator = 0
        self.table_name = "generalrecipe"
        self.row = ""


    def transform_data(self, response):
        name = response['strMeal']
        self.row += name.replace("'","")
        self.row = "DEFAULT," "'" + self.row + "'"
        return self.row
