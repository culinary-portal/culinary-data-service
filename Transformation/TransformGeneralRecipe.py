
class TransformGeneralRecipe:
    def __init__(self):
        self.table_name = "general_recipe"

    def transform_data(self, response):
        if response['strMeal'] is not None:
            name = response['strMeal'].replace("'", "")
            instructions = response['strInstructions'].replace("'", "")
            pho_url = response['strMealThumb'].replace("'", "")
            row = f" DEFAULT, '{name}' ,'{pho_url}' ,NULL, NULL, '{instructions}', NULL"
            return row
        else:
            return False
