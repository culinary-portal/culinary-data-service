

CREATE TABLE IF NOT EXISTS testing (
ingredient_id SERIAL PRIMARY KEY,
name VARCHAR,
fat FLOAT,
protein FLOAT,
carbohydrate FLOAT,
kcal FLOAT,
is_vegan BOOLEAN,
is_vegetarian BOOLEAN,
is_gluten_free BOOLEAN,
is_lactose_free BOOLEAN
);