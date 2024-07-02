import populate_general_recipe
import populate_ingredient
import get_data
def main():
    #p = populate_general_recipe.PopulateGeneralRecipe()
    #p.populate()

    p = populate_ingredient.PopulateIngredient()
    p.populate()


if __name__ == "__main__":
    filesave = get_data.CulinaryDataService("https://www.themealdb.com/api")
    filesave.save_to_file()
    #main()