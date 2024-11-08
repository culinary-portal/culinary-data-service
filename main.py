import GeneralUtilities.GetData as GetData
from Transformation.TransformGeneralRecipe import TransformGeneralRecipe
from Transformation.TransformIngredient import TransformIngredient
from Transformation.TransformContains import TransformContains
from Transformation.TransformRecipe import TransformRecipe


def main():
    data_service = GetData.GetData("https://www.themealdb.com/api")
    general_recipe = TransformGeneralRecipe()
    ingredients = TransformIngredient()
    recipe = TransformRecipe()
    contains = TransformContains()

    MAX_ITERATOR = 317
    MAX_INGREDIENTS = 20

    # Open files for each table
    with open("general_recipe_data.txt", "w", encoding='utf-8') as general_recipe_file, \
         open("recipe_data.txt", "w", encoding='utf-8') as recipe_file, \
         open("ingredient_data.txt", "w", encoding='utf-8') as ingredient_file, \
         open("contains_data.txt", "w", encoding='utf-8') as contains_file:

        for iterator in range(MAX_ITERATOR):
            response = data_service.get_one(iterator)
            if response is not None:
                # Transform and save the general recipe row
                row = general_recipe.transform_data(response)
                print(f"Writing General Recipe Row for Iterator {iterator}: {row}")
                general_recipe_file.write(f"{row}\n")

                # # Transform and save the recipe row
                # recipe_row = recipe.transform_data(response)
                # print(f"Writing Recipe Row for Iterator {iterator}: {recipe_row}")
                # recipe_file.write(f"{recipe_row}\n")
                #
                # max_ingredients_for_recipe = int(data_service.get_number_of_max_ingredients(response)) - 1
                #
                # for i in range(MAX_INGREDIENTS):
                #     # Transform and save ingredient row
                #     ingredient_row = ingredients.transform_data(response, i)
                #     print(f"Writing Ingredient Row (Iterator {iterator}, Ingredient {i}): {ingredient_row}")
                #     ingredient_file.write(f"{ingredient_row}\n")

                    # # Transform and save "contains" row
                    # contains_row = contains.transform_data(response, i)
                    # if contains_row:
                    #     print(f"Writing Contains Row (Iterator {iterator}, Ingredient {i}): {contains_row}")
                    #     contains_file.write(f"{contains_row}\n")
                    # else:
                    #     print(f"No valid 'Contains' data for Ingredient {i} in Iterator {iterator}")
                    #
                    # # Break if max ingredients reached for the current recipe
                    # if i == max_ingredients_for_recipe:
                    #     break


if __name__ == "__main__":
    main()
