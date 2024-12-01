drop table testing;

CREATE TABLE IF NOT EXISTS testing (
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

select * from testing where is_vegan = 0 or is_vegetarian = 0 or is_gluten_free = 0 or is_lactose_free = 0;

select * from ingredient where ingredient_id = 854 or ingredient_id = 1454;

select general_recipe_id, name, photo_url from general_recipe;

UPDATE general_recipe
SET base_recipe_id = recipe.recipe_id
FROM recipe
WHERE general_recipe.name = recipe.name;


select r.name, min(i.is_vegan) as vegan,  min(i.is_gluten_free) as gluten
from recipe r join contains c
on c.recipe_id = r.recipe_id
join ingredient i on i.ingredient_id = c.ingredient_id
group by r.name;

select * from general_recipe;


