--changing the naming to contain only lowercase letter
update ingredient set name = lower(name);
--updating column general_recipe.recipe_id with the id from base recipe
UPDATE general_recipe
SET base_recipe_id = recipe.recipe_id
FROM recipe
WHERE general_recipe.name = recipe.name;
-- flagging the recipe based on the flags of ingredients
-- first, we create temp view to then create cases and populate column
create temp view joined as
select r.recipe_id, min(i.is_vegan) as vegan,  min(i.is_gluten_free) as gluten_free,
min(i.is_lactose_free) as lactose_free, min(i.is_vegetarian)  as vegetarian
from recipe r join contains c
on c.recipe_id = r.recipe_id
join ingredient i on i.ingredient_id = c.ingredient_id
group by r.recipe_id;
--
UPDATE recipe
SET diet_type_id = subquery.diet_type_id
FROM (
    SELECT r.recipe_id, dt.diet_type_id
    FROM recipe r
    INNER JOIN joined j ON r.recipe_id = j.recipe_id
    INNER JOIN diet_type dt ON dt.diet_type = 'VEGETARIAN'
    WHERE j.vegetarian = 1
) AS subquery
WHERE recipe.recipe_id = subquery.recipe_id;
--
UPDATE recipe
SET diet_type_id = subquery.diet_type_id
FROM (
    SELECT r.recipe_id, dt.diet_type_id
    FROM recipe r
    INNER JOIN joined j ON r.recipe_id = j.recipe_id
    INNER JOIN diet_type dt ON dt.diet_type = 'VEGAN'
    WHERE j.vegan = 1
) AS subquery
WHERE recipe.recipe_id = subquery.recipe_id;
--
UPDATE recipe
SET diet_type_id = subquery.diet_type_id
FROM (
    SELECT r.recipe_id, dt.diet_type_id
    FROM recipe r
    INNER JOIN joined j ON r.recipe_id = j.recipe_id
    INNER JOIN diet_type dt ON dt.diet_type = 'GLUTEN_FREE'
    WHERE j.gluten_free = 1
) AS subquery
WHERE recipe.recipe_id = subquery.recipe_id;
--
UPDATE recipe
SET diet_type_id = subquery.diet_type_id
FROM (
    SELECT r.recipe_id, dt.diet_type_id
    FROM recipe r
    INNER JOIN joined j ON r.recipe_id = j.recipe_id
    INNER JOIN diet_type dt ON dt.diet_type = 'LACTOSE_FREE'
    WHERE j.lactose_free = 1
) AS subquery
WHERE recipe.recipe_id = subquery.recipe_id;
-- check for duplicates inside the ingredients table (especially in after adding the substitues )
WITH cte_duplicates AS (
    SELECT
        MIN(ingredient_id) AS min_id,  -- keep the lowest id for contains table for mapping
        name, fat, protein, carbohydrate, is_vegetarian, is_lactose_free, is_gluten_free, is_vegan, is_keto
    FROM ingredient
    GROUP BY name, fat, protein, carbohydrate, kcal,is_vegetarian, is_lactose_free, is_gluten_free, is_vegan, is_keto
)
DELETE FROM ingredient
WHERE ingredient_id NOT IN (
    SELECT min_id FROM cte_duplicates
);
-- update NULL columns to "unknown" for smooth handling null values
update general_recipe
set description = 'NA'
where true;
--
update recipe
set description = 'NA'
where true;
-- if regular expression did not find any match, replace the value with "average" value
update contains
set amount = 1
where amount in (0,-1,-2);
--
update contains
set measure = 10
where measure = 'n/a';
-- add column to enable future proportion
alter table contains add proportion_i1_i2 float;
-- populate 1 to make backend work without changes
update contains
set proportion_i1_i2 = 1
where 1 = 1;
