import GeneralUtilities.GetData as GetData
from Transformation.TransformGeneralRecipe import TransformGeneralRecipe
from Transformation.TransformIngredient import TransformIngredient
from Transformation.TransformContains import TransformContains
from Transformation.TransformRecipe import TransformRecipe
import GeneralUtilities.Populator as Populator
from Transformation import SavingTableTxt

# Flags to control execution of specific parts
ENABLE_GENERAL_RECIPE_INSERT = True
ENABLE_INGREDIENTS_INSERT = True
ENABLE_CONTAINS_INSERT = True
ENABLE_RECIPE_INSERT = True


def main():
    data_service = GetData.GetData("https://www.themealdb.com/api")
    populate_database = Populator.Populator()
    general_recipe = TransformGeneralRecipe()
    ingredients = TransformIngredient()
    recipe = TransformRecipe()
    contains = TransformContains()
    MAX_ITERATOR = 317
    MAX_INGREDIENTS = 20

    for iterator in range(MAX_ITERATOR):
        response = data_service.get_one(iterator)
        if response is not None:

            if ENABLE_GENERAL_RECIPE_INSERT:
                row = general_recipe.transform_data(response)
                #populate_database.insert_row(general_recipe.table_name, row)
                print("Inserted general recipe row:", row)

            max_ingredients_for_recipe = int(data_service.get_number_of_max_ingredients(response)) - 1
            for i in range(MAX_INGREDIENTS):
                if ENABLE_INGREDIENTS_INSERT:
                    row = ingredients.transform_data(response, i)
                    #populate_database.insert_row(ingredients.table_name, row)
                    print("Inserted ingredient row:", row)

                if ENABLE_CONTAINS_INSERT:
                    row = contains.transform_data(response, i)
                    #populate_database.insert_row(contains.table_name, row)
                    print("Inserted contains row:", row)

                # Break if we've reached the max ingredients for this recipe
                if i == max_ingredients_for_recipe:
                    break

            if ENABLE_RECIPE_INSERT:
                recipe_row = recipe.transform_data(response)
                #populate_database.insert_row(recipe.table_name, recipe_row)
                print("Inserted recipe row:", recipe_row)


if __name__ == "__main__":
    main()
