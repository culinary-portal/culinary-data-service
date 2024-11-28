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