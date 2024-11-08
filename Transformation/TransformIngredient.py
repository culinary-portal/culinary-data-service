import requests
import json


class TransformIngredient:
    def __init__(self):
        self.starting_id = 52767
        self.number_of_meals = 317
        self.table_name = "ingredient"
        self.row = ""

    def transform_data(self, response, iterator):
        ingredient = f"{response[f'strIngredient{iterator + 1}']}"
        print(ingredient)
        ingredient = ingredient.replace("'", "")
        fats, proteins, carbs, kcal = self.get_micro_elements(ingredient)
        self.row = f"DEFAULT, '{ingredient}',{fats}, {proteins}, {carbs}, {kcal},NULL,NULL"
        return self.row

    def get_micro_elements(self, ingredient):
        #for now dummy values, then we will get real data from API, keep in mind number of calls per day for the API
        headers = {
            'Content-Type': 'application/json',
            'x-app-id': '02cd2118',
            'x-app-key': 'x-app-key'
        }
        body = {
            "query": f"{ingredient}"
        }
        response = requests.post('https://trackapi.nutritionix.com/v2/natural/nutrients', headers=headers,
                                 data=json.dumps(body)).json()
        print(response)
        try:
            grams = response["foods"][0]["serving_weight_grams"]
            kcal = str(int(response["foods"][0]["nf_calories"]) * 100 / grams)
            proteins = str(int(response["foods"][0]["nf_protein"]) * 100 / grams)
            fats = str(int(response["foods"][0]["nf_total_fat"]) * 100 / grams)
            carbs = str(int(response["foods"][0]["nf_total_carbohydrate"]) * 100 / grams)

            return 5, 10, 15, 220
        except Exception as e:
            kcal, proteins, fats, carbs = "NULL", "NULL", "NULL", "NULL"
            return fats, proteins, carbs, kcal
