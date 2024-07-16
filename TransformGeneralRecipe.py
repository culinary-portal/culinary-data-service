from psycopg2 import Error


class PopulateGeneralRecipe:
    def __init__(self):
        self.iterator = 0
        self.table_name = "generalrecipe"
        self.current_response = ""
        self.row = ""

    def transform_data(self, iterator):
        name = f"{self.current_response['meals'][0]['strMeal']}"
        self.row += name.replace("'","")
        self.row = "'" + self.row + "'"
        print(self.row)
        return self.row
