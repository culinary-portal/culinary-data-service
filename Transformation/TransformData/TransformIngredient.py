import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class TransformIngredient:
    def __init__(self):
        self.starting_id = 52767
        self.table_name = "ingredient"
        self.row = ""

    def transform_data(self, response):
        ingredient = response.replace("'", "")
        # get the macronutrient data
        fats, proteins, carbs, kcal = self.get_macro_elements(ingredient)

        self.row = f"DEFAULT, '{ingredient}', {fats}, {proteins}, {carbs}, {kcal}, NULL, NULL, NULL, NULL, NULL"
        return self.row

    def get_macro_elements(self, ingredient):
        headers = {
            'Content-Type': os.getenv('CONTENT_TYPE'),
            'x-app-id': os.getenv('X_APP_ID'),
            'x-app-key': os.getenv('X_APP_KEY')
        }
        body = {
            "query": ingredient
        }
        try:
            response = requests.post(
                'https://trackapi.nutritionix.com/v2/natural/nutrients',
                headers=headers,
                data=json.dumps(body)
            ).json()

            # debugging output for the response
            print(response)
            # placeholder when response not valid
            dummy_values = ("-1", "-1", "-1", "-1")
            # Parse the response
            food_data = response.get("foods", [{}])[0]
            grams = food_data.get("serving_weight_grams", 100)  # Assume 100g if missing
            kcal = str(round(food_data.get("nf_calories", 0) * 100 / grams, 2))
            proteins = str(round(food_data.get("nf_protein", 0) * 100 / grams, 2))
            fats = str(round(food_data.get("nf_total_fat", 0) * 100 / grams, 2))
            carbs = str(round(food_data.get("nf_total_carbohydrate", 0) * 100 / grams, 2))

            return fats, proteins, carbs, kcal
        except requests.exceptions.RequestException as e:
            print(f"Error while getting the data: {e}")
            return dummy_values


