import ConnectionToDatabase
import GetData
import TransformGeneralRecipe
import TransformIngredient
import Populator


def main():
    data_service = GetData.GetData("https://www.themealdb.com/api")
    populate_database = Populator.Populator()
    general_recipe = TransformGeneralRecipe.TransformGeneralRecipe()
    ingredients = TransformIngredient.TransformIngredient()
    MAX_ITERATOR = 317
    # for iterator in range(MAX_ITERATOR):
    for iterator in range(0, 1):
        response = data_service.get_one(iterator)

        row = general_recipe.transform_data(response)
        populate_database.insert_row(general_recipe.table_name, row)


        for i in range(20):
            populate_database = Populator.Populator()
            row = ingredients.transform_data(response)
            populate_database.insert_row(ingredients.table_name, row)


if __name__ == "__main__":
    main()
