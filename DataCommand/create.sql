CREATE TABLE IF NOT EXISTS diet_type (
diet_type_id SERIAL PRIMARY KEY,
diet_type VARCHAR
);

CREATE TABLE IF NOT EXISTS general_recipe (
general_recipe_id SERIAL PRIMARY KEY,
name VARCHAR(100) NOT NULL,
photo_url TEXT,
meal_type VARCHAR(10) NOT NULL CHECK (meal_type IN ('BREAKFAST', 'LUNCH', 'DINNER', 'SUPPER', 'DESSERT')),
description TEXT,
steps TEXT,
base_recipe_id INTEGER
);

CREATE TABLE IF NOT EXISTS users (
user_id SERIAL PRIMARY KEY,
user_name VARCHAR,
email VARCHAR,
password VARCHAR,
birthdate TIMESTAMP,
create_date TIMESTAMP,
photo_url TEXT,
pref_is_vegan BOOLEAN,
pref_is_gluten_free BOOLEAN,
account_enabled BOOLEAN,
account_expired BOOLEAN,
account_locked BOOLEAN,
credentials_expired BOOLEAN
);

CREATE TABLE IF NOT EXISTS user_diet_type (
user_id INT,
diet_type_id INT,
PRIMARY KEY (user_id, diet_type_id),
FOREIGN KEY (user_id) REFERENCES users (user_id),
FOREIGN KEY (diet_type_id) REFERENCES diet_type (diet_type_id)
);

CREATE TABLE IF NOT EXISTS roles (
role_id SERIAL PRIMARY KEY,
user_id INTEGER NOT NULL,
role VARCHAR(255) CHECK (role IN ('ADMIN', 'ANONYMOUS', 'USER')),
CONSTRAINT fk_user_roles FOREIGN KEY (user_id) REFERENCES users (user_id)
);

CREATE TABLE IF NOT EXISTS ingredient (
ingredient_id SERIAL PRIMARY KEY,
name VARCHAR,
fat FLOAT,
protein FLOAT,
carbohydrate FLOAT,
kcal FLOAT,
is_vegan INT,
is_vegetarian INT,
is_gluten_free INT,
    is_lactose_free INT,
    is_keto INT
);

CREATE TABLE IF NOT EXISTS recipe (
recipe_id SERIAL PRIMARY KEY,
general_recipe_id INTEGER,
name VARCHAR,
description TEXT,
diet_type_id INTEGER,
CONSTRAINT fk_general_recipe FOREIGN KEY (general_recipe_id) REFERENCES general_recipe (general_recipe_id),
CONSTRAINT fk_diet_type FOREIGN KEY (diet_type_id) REFERENCES diet_type (diet_type_id)
);

CREATE TABLE IF NOT EXISTS contains (
contains_id SERIAL PRIMARY KEY,
amount FLOAT,
measure VARCHAR,
recipe_id INTEGER,
ingredient_id INTEGER,
CONSTRAINT fk_recipe_contains FOREIGN KEY (recipe_id) REFERENCES recipe (recipe_id),
CONSTRAINT fk_contains_ingredient FOREIGN KEY (ingredient_id) REFERENCES ingredient (ingredient_id)
);

CREATE TABLE IF NOT EXISTS substitute (
substitute_id SERIAL PRIMARY KEY,
ingredient1_id INTEGER,
ingredient2_id INTEGER,
CONSTRAINT fk_ingredient1 FOREIGN KEY (ingredient1_id) REFERENCES ingredient (ingredient_id),
CONSTRAINT fk_ingredient2 FOREIGN KEY (ingredient2_id) REFERENCES ingredient (ingredient_id)
);

CREATE TABLE IF NOT EXISTS review (
review_id SERIAL PRIMARY KEY,
user_id INTEGER,
general_recipe_id INTEGER,
rating INTEGER,
opinion VARCHAR,
CONSTRAINT fk_review_user FOREIGN KEY (user_id) REFERENCES users (user_id),
CONSTRAINT fk_review_general_recipe FOREIGN KEY (general_recipe_id) REFERENCES general_recipe (general_recipe_id)
);

CREATE TABLE IF NOT EXISTS favorite (
favorites_id SERIAL PRIMARY KEY,
user_id INTEGER,
general_recipe_id INTEGER,
CONSTRAINT fk_favorites_user FOREIGN KEY (user_id) REFERENCES users (user_id),
CONSTRAINT fk_favorites_recipe FOREIGN KEY (general_recipe_id) REFERENCES general_recipe (general_recipe_id)
);

CREATE TABLE IF NOT EXISTS modified_recipe (
modified_recipe_id SERIAL PRIMARY KEY,
user_id INTEGER,
recipe_id INTEGER,
CONSTRAINT fk_modified_user FOREIGN KEY (user_id) REFERENCES users (user_id),
CONSTRAINT fk_modified_recipe FOREIGN KEY (recipe_id) REFERENCES recipe (recipe_id)
);

CREATE TABLE IF NOT EXISTS specific (
specific_id SERIAL PRIMARY KEY,
user_id INTEGER,
id_ingredient INTEGER,
likes BOOLEAN,
CONSTRAINT fk_specific_user FOREIGN KEY (user_id) REFERENCES users (user_id),
CONSTRAINT fk_specific_ingredient FOREIGN KEY (id_ingredient) REFERENCES ingredient (ingredient_id)
);
