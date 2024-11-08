import GeneralUtilities.GetData as GetData
from Transformation.TransformGeneralRecipe import TransformGeneralRecipe
from Transformation.TransformIngredient import TransformIngredient
from Transformation.TransformContains import TransformContains
from Transformation.TransformRecipe import TransformRecipe
import GeneralUtilities.Populator as Populator


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
            # Insert the general recipe row
            row = general_recipe.transform_data(response)
            print(f"Inserting General Recipe Row for Iterator {iterator}: {row}")
            populate_database.insert_row(general_recipe.table_name, row)

            # Insert into the recipe table and ensure success
            recipe_row = recipe.transform_data(response)
            recipe_insert_success = populate_database.insert_row(recipe.table_name, recipe_row)
            print(f"Inserting Recipe Row for Iterator {iterator}: {recipe_row}")

            if not recipe_insert_success:
                print(f"Failed to insert recipe for {response['strMeal']}; skipping 'contains' insertions.")
                continue  # Skip to the next iterator if the recipe insertion fails

            max_ingredients_for_recipe = int(data_service.get_number_of_max_ingredients(response)) - 1

            for i in range(MAX_INGREDIENTS):
                # Insert ingredients row
                ingredient_row = ingredients.transform_data(response, i)
                print(f"Inserting Ingredient Row (Iterator {iterator}, Ingredient {i}): {ingredient_row}")
                populate_database.insert_row(ingredients.table_name, ingredient_row)

                # Insert "contains" relationship
                contains_row = contains.transform_data(response, i)
                if contains_row:
                    print(f"Inserting Contains Row (Iterator {iterator}, Ingredient {i}): {contains_row}")
                    insert_success = populate_database.insert_row(contains.table_name, contains_row)

                    # Check if insertion failed due to foreign key constraint
                    if not insert_success:
                        print(
                            f"Failed to insert 'contains' row for recipe ID {contains_row.split(', ')[3]} and ingredient {i}")
                else:
                    print(f"No valid 'Contains' data for Ingredient {i} in Iterator {iterator}")

                # Break if max ingredients reached for the current recipe
                if i == max_ingredients_for_recipe:
                    break


if __name__ == "__main__":
    main()
