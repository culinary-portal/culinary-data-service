from psycopg2 import Error
import requests
import json

class TransformIngredient:
    def __init__(self):
        self.starting_id = 52767
        self.number_of_meals = 317
        self.table_name = "ingredient"
        self.row = ""
        self.ingredients_size = 20
        self.last_ingredient_id = 0
        self.ninja_api_key = '0vZpAVmpN3ZDYCbMyvsPDQ==86dLn8e6GhCQXOIJ'

    def transform_data(self, response):
        ingredient = f"{response[f'strIngredient{self.last_ingredient_id + 1}']}"
        print(ingredient)
        ingredient = ingredient.replace("'", "")
        fats, proteins, carbs, kcal = self.get_micro_elements(ingredient)
        self.row = "DEFAULT," + "'" + ingredient + "'" + "," + fats + "," + proteins + "," + carbs + "," + kcal
        self.last_ingredient_id += 1
        return self.row

    def get_micro_elements(self, ingredient):
        headers = {
            'Content-Type': 'application/json',
            'x-app-id': '02cd2118',
            'x-app-key': 'e6d09e67fb32c4dde191663580baa2b1'
        }
        body = {
            "query": f"{ingredient}"
        }
        response = requests.post('https://trackapi.nutritionix.com/v2/natural/nutrients', headers=headers,data=json.dumps(body)).json()
        print(response)
        grams = response["foods"][0]["serving_weight_grams"]
        kcal = str(int(response["foods"][0]["nf_calories"]) / grams * 100)
        proteins = str(int(response["foods"][0]["nf_protein"]) / grams * 100)
        fats = str(int(response["foods"][0]["nf_total_fat"]) / grams * 100)
        carbs = str(int(response["foods"][0]["nf_total_carbohydrate"]) / grams * 100)
        print(grams)
        return kcal, proteins, fats, carbs



















