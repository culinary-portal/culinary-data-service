import requests

class GetData:
    def __init__(self, base_url):
        self.base_url = "https://www.themealdb.com/api"
        self.max_ingredients = 20
        self.number_of_meals = 317
        self.starting_id = 52767
        self.file_name = 'mealdb_data'

    def combine_url(self, endpoint):
        return f"{self.base_url}/{endpoint}"

    def get_method(self, endpoint):
        url = self.combine_url(endpoint)
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code)
            print("Error while getting the response")

    def save_to_file(self):
        f = open(self.file_name, 'w')
        for i in range(self.number_of_meals):
            response = requests.get(f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={self.starting_id + i}')
            f.write(response.text)
        f.close()

    def get_one(self, iterator):
        current_response = self.get_method(f"json/v1/1/lookup.php?i={self.starting_id + iterator}")
        print(current_response)
        if current_response['meals'] is None:
            print("No data")
            return None
        else:
            return current_response['meals'][0]

    def get_number_of_max_ingredients(self, response):
        for i in range(1,self.max_ingredients):
            if response[f'strIngredient{i}'] is None or response[f'strIngredient{i}'] == '':
                print(i)
                return i

