import GetData
from Transformations.TransformGeneralRecipe import TransformGeneralRecipe
from Transformations.TransformIngredient import TransformIngredient
import Populator


def main():
    data_service = GetData.GetData("https://www.themealdb.com/api")
    populate_database = Populator.Populator()
    general_recipe = TransformGeneralRecipe()
    ingredients = TransformIngredient()
    MAX_ITERATOR = 317
    for iterator in range(MAX_ITERATOR):
        response = data_service.get_one(iterator)
        if response is not None:
            row = general_recipe.transform_data(response)
            print(row)

            populate_database.insert_row(general_recipe.table_name, row)



         # for i in range(20):
         #    populate_database = Populator.Populator()
         #    row = ingredients.transform_data(response)
         #    populate_database.insert_row(ingredients.table_name, row)


if __name__ == "__main__":
    main()
