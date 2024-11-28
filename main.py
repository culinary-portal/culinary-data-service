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
    ENABLE_INGREDIENTS = True
    ENABLE_CONTAINS = False
    ENABLE_SUBSTITUTES = True
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

    # Open files for each table
    with open("general_recipe_data.txt", "w", encoding='utf-8') as general_recipe_file, \
            open("recipe_data.txt", "w", encoding='utf-8') as recipe_file, \
            open("ingredient_data.txt", "a", encoding='utf-8') as ingredient_file, \
            open("contains_data.txt", "w", encoding='utf-8') as contains_file:

        # Transform and save ingredient row
        if Config.ENABLE_INGREDIENTS:
            for one_ingredient in get_ingredient_name_list('Transformation/ClearData/grouped_ingredients.csv'):
                ingredient_row = ingredients.transform_data(one_ingredient, 0)
                if ingredient_row:
                    print(f"Writing Ingredient Row  {ingredient_row}")
                    ingredient_file.write(f"{ingredient_row}\n")

        for iterator in range(Config.MAX_ITERATOR):
            response = data_service.get_one(iterator)
            if response is None:
                print(f"No data returned for iterator {iterator}. Skipping...")
                continue

            # Transform and save the general recipe row
            if Config.ENABLE_GENERAL_RECIPE:
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

            max_ingredients_for_recipe = int(data_service.get_number_of_max_ingredients(response)) - 1

            for i in range(max_ingredients_for_recipe):
                # Transform and save "contains" row
                if Config.ENABLE_CONTAINS:
                    contains_row = contains.transform_data(response, i)
                    if contains_row:
                        print(f"Writing Contains Row (Iterator {iterator}, Ingredient {i}): {contains_row}")
                        contains_file.write(f"{contains_row}\n")
                    else:
                        print(f"No valid 'Contains' data for Ingredient {i} in Iterator {iterator}")
        if Config.ENABLE_CONTAINS: # creates a new file with all combinations of ids from the substitutes_map
            substitutes.transform_data()


if __name__ == "__main__":
    main()
