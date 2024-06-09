import requests

class CulinaryDataService:
    def __init__(self, base_url) :
        self.base_url = base_url

    def combine_url(self, endpoint) :
        return f"{self.base_url}/{endpoint}"

    def get_method(self, endpoint):
        url = self.combine_url(endpoint)
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code)
            print("Error while getting the response")



