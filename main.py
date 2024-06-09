import populate_general_recipe
import populate_ingredient
def main():
    #p = populate_general_recipe.PopulateGeneralRecipe()
    #p.populate()

    p = populate_ingredient.PopulateIngredient()
    p.populate()


if __name__ == "__main__":
    main()