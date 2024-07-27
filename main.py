import GeneralUtilities.GetData as GetData
from Transformation.TransformGeneralRecipe import TransformGeneralRecipe
from Transformation.TransformIngredient import TransformIngredient
import GeneralUtilities.Populator as Populator


def main():
    data_service = GetData.GetData("https://www.themealdb.com/api")
    populate_database = Populator.Populator()
    general_recipe = TransformGeneralRecipe()
    ingredients = TransformIngredient()
    MAX_ITERATOR = 317
    MAX_INGREDIENTS = 20
    for iterator in range(1):
        response = data_service.get_one(iterator)
        if response is not None:
            # row = general_recipe.transform_data(response)
            # print(row)
            # populate_database.insert_row(general_recipe.table_name, row)
            # max_ingredients_for_recipe = int(data_service.get_number_of_max_ingredients(response)) - 1
            # for i in range(MAX_INGREDIENTS):
            #     row = ingredients.transform_data(response, i)
            #     print(row)
            #     if i == max_ingredients_for_recipe:
            #         break
            #     populate_database.insert_row(ingredients.table_name, row)
            pass

if __name__ == "__main__":
    main()
