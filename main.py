import GeneralUtilities.GetData as GetData
from Transformation.TransformData.TransformGeneralRecipe import TransformGeneralRecipe
from Transformation.TransformData.TransformIngredient import TransformIngredient
from Transformation.TransformData.TransformContains import TransformContains
from Transformation.TransformData.TransformRecipe import TransformRecipe
from Transformation.TransformData.TransformSubstitutes import TransformSubstitutes
import csv


class Config:
    # Configuration flags for enabling/disabling specific parts of the code
    ENABLE_GENERAL_RECIPE = False
    ENABLE_RECIPE = False
    # fetching the ingredients result in having all the data apart from the flags
    ENABLE_INGREDIENTS = False
    ENABLE_CONTAINS = False
    ENABLE_SUBSTITUTES = False
    MAX_ITERATOR = 300
    MAX_INGREDIENTS = 20


def get_ingredient_name_list(file_path):
    ingredient_names = []
    with open(file_path, mode="r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if len(row) > 1:
                ingredient_names.append(row[1])  # Second column
    return ingredient_names


def main():
    data_service = GetData.GetData("https://www.themealdb.com/api")
    general_recipe = TransformGeneralRecipe()
    ingredients = TransformIngredient()
    recipe = TransformRecipe()
    contains = TransformContains()
    substitutes = TransformSubstitutes()

    g = general_recipe.post_processing()

    if Config.ENABLE_SUBSTITUTES:  # creates a new file with all combinations of ids from the substitutes_map
        substitutes = substitutes.transform_data()
    # Open files for each table
    with open("Transformation/ClearData/general_recipe_table.txt", "w", encoding='utf-8') as general_recipe_file, \
            open("Transformation/ClearData/recipe_table.txt", "w", encoding='utf-8') as recipe_file, \
            open("ingredient_data.txt", "a", encoding='utf-8') as ingredient_file, \
            open("Transformation/ClearData/contains_data.txt", "w", encoding='utf-8') as contains_file:

        # Transform and save ingredient row
        if Config.ENABLE_INGREDIENTS:
            for one_ingredient in get_ingredient_name_list('Transformation/working_data/grouped_ingredients.txt'):
                ingredient_row = ingredients.transform_data(one_ingredient)
                if ingredient_row:
                    print(f"Writing Ingredient Row  {ingredient_row}")
                    ingredient_file.write(f"{ingredient_row}\n")
        if Config.ENABLE_GENERAL_RECIPE:
            for iterator in range(Config.MAX_ITERATOR):
                response = data_service.get_one(iterator)
                if response is not None:

                    # Transform and save the general recipe row
                    row = general_recipe.transform_data(response)
                    if row:
                        print(f"Writing General Recipe Row for Iterator {iterator}: {row}")
                        general_recipe_file.write(f"{row}\n")
                # Transform and save the recipe row
                if Config.ENABLE_RECIPE:
                    recipe_row = recipe.transform_data(response)
                    if recipe_row:
                        print(f"Writing Recipe Row for Iterator {iterator}: {recipe_row}")
                        recipe_file.write(f"{recipe_row}\n")

                if Config.ENABLE_CONTAINS:
                    max_ingredients_for_recipe = int(data_service.get_number_of_max_ingredients(response)) - 1
                    for i in range(max_ingredients_for_recipe):
                        # Transform and save "contains" row
                        contains_row = contains.transform_data(response, i)
                        if contains_row:
                            print(f"Writing Contains Row (Iterator {iterator}, Ingredient {i}): {contains_row}")
                            contains_file.write(f"{contains_row}\n")
                        else:
                            print(f"No valid 'Contains' data for Ingredient {i} in Iterator {iterator}")
            else:
                print("Response is none")


if __name__ == "__main__":
    main()
