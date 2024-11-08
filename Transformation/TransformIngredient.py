import requests
import json


class TransformIngredient:
    def __init__(self):
        self.starting_id = 52767
        self.number_of_meals = 317
        self.table_name = "ingredient"
        self.row = ""

    def transform_data(self, response, iterator):
        ingredient = response.get(f'strIngredient{iterator + 1}', "").replace("'", "")

        if not ingredient:
            return None  # Skip if no ingredient is found

        # Fetch nutritional values
        fats, proteins, carbs, kcal = self.get_micro_elements(ingredient)

        # Create the SQL row format
        self.row = f"DEFAULT, '{ingredient}', {fats}, {proteins}, {carbs}, {kcal}, NULL, NULL"
        return self.row

    def get_micro_elements(self, ingredient):
        """
        Retrieves the macronutrient information for an ingredient.
        Currently returns dummy values to reduce API calls during testing.
        """
        headers = {
            'Content-Type': 'application/json',
            'x-app-id': '02cd2118',
            'x-app-key': 'your-app-key'
        }

        body = {
            "query": ingredient
        }

        # Placeholder values for testing without API calls
        dummy_values = ("5", "10", "15", "220")

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

