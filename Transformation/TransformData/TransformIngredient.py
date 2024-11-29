import requests
import json
import time


class TransformIngredient:
    def __init__(self):
        self.starting_id = 52767
        self.table_name = "ingredient"
        self.row = ""

    def transform_data(self, response):
        ingredient = response.replace("'", "")
        # Get the macronutrient data
        fats, proteins, carbs, kcal = self.get_macro_elements(ingredient)

        self.row = f"DEFAULT, '{ingredient}', {fats}, {proteins}, {carbs}, {kcal}, NULL, NULL, NULL, NULL, NULL"
        return self.row

    def get_macro_elements(self, ingredient):
        # headers = {
        #     'Content-Type': 'application/json',
        #     'x-app-id': 'df854fb1   ',
        #     'x-app-key': '372bc7c57fb7fa88021e943b8a3e3ad2'
        # }
        headers = {
            'Content-Type': 'application/json',
            'x-app-id': '02cd2118',
            'x-app-key': '72b52f538fcc03c90ef4d9fa90ffd1b8'
        }

        body = {
            "query": ingredient
        }

        # placeholder when response not valid
        dummy_values = ("-1", "-1", "-1", "-1")

        try:
            response = requests.post(
                'https://trackapi.nutritionix.com/v2/natural/nutrients',
                headers=headers,
                data=json.dumps(body)
            ).json()

            # Debugging output for the response
            print(response)

            # Parse the response
            food_data = response.get("foods", [{}])[0]
            grams = food_data.get("serving_weight_grams", 100)  # Assume 100g if missing
            kcal = str(round(food_data.get("nf_calories", 0) * 100 / grams, 2))
            proteins = str(round(food_data.get("nf_protein", 0) * 100 / grams, 2))
            fats = str(round(food_data.get("nf_total_fat", 0) * 100 / grams, 2))
            carbs = str(round(food_data.get("nf_total_carbohydrate", 0) * 100 / grams, 2))

            return fats, proteins, carbs, kcal

        except Exception as e:
            print(f"Error fetching nutrient data for {ingredient}: {e}")
            return dummy_values  # Use placeholder values on error
