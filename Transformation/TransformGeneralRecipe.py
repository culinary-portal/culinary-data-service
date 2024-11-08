class TransformGeneralRecipe:
    def __init__(self):
        self.table_name = "general_recipe"

    def transform_data(self, response):
        # Check for required fields
        if not all(key in response for key in ['strMeal', 'strInstructions', 'strMealThumb']):
            return False

        # Validate 'strMeal' existence and value
        name = response.get('strMeal')
        if not name:
            return False

        # Extract and clean fields
        name = name.replace("'", "")
        instructions = response.get('strInstructions', "").replace("'", "")
        pho_url = response.get('strMealThumb', "").replace("'", "")

        # Construct row with formatted string for better readability
        row = f"DEFAULT, '{name}', '{pho_url}', NULL, NULL, '{instructions}', NULL"

        return row
