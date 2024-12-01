import csv
import os


class TransformGeneralRecipe:
    def __init__(self):
        self.table_name = "general_recipe"

    def transform_data(self, response):
        # Check for required fields
        if not all(key in response for key in ['strMeal', 'strInstructions', 'strMealThumb']):
            return False

        # Validate 'strMeal' existence and value
        name = response.get('strMeal')
        if not name:
            return False

        # Extract and clean fields
        name = name.replace("'", "")
        instructions = response.get('strInstructions', "").replace("'", "").replace("\n", " ").replace('\r', " ")
        pho_url = response.get('strMealThumb', "").replace("'", "")

        # Construct row with formatted string for better readability
        row = f"DEFAULT, '{name}', '{pho_url}', 'BREAKFAST', NULL, '{instructions}', NULL"
        return row

    def post_processing(self):
        # file paths
        main_file = 'Transformation/ClearData/general_recipe_table.txt'
        mapping_file = 'Transformation/mapping/meal_type_map.txt'
        output_file = 'Transformation/ClearData/general_recipe_table_meal_typed.txt'

        key_value_map = {}
        with open(mapping_file, mode='r', newline='\n', encoding='utf-8') as map_file:
            reader = csv.reader(map_file)
            for row in reader:
                name = row[0].strip('"')
                new_meal_type = row[1]
                key_value_map[name] = new_meal_type

        # update the mealtype column according to mapping
        updated_rows = []
        print(f"File exists: {os.path.exists(main_file)}")
        with open(main_file, mode='r', newline='', encoding='utf-8') as main_csv:
            reader_main = csv.reader(main_csv, quotechar='"', delimiter=',')
            for row in reader_main:
                if len(row) > 3:
                    name = row[1].strip("'")
                    if name in key_value_map:
                        row[3] = f"'{key_value_map[name]}'"
                # add ' signs to properly load to db
                row[1] = "'" + row[1] + "'"
                row[2] = "'" + row[2] + "'"
                # populate description field with nulls
                row[4] = 'NULL'
                print(row)
                updated_rows.append(row)
        # now save the new file with updated column
        with open(output_file, mode='w', newline='', encoding='utf-8') as output_csv:
            writer = csv.writer(output_csv)
            writer.writerows(updated_rows)
