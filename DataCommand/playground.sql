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

select  * from testing;


WITH cte_duplicates AS (
    SELECT
        MIN(ingredient_id) AS min_id,  -- Keep the row with the smallest ID
        name, fat, protein, carbohydrate, is_vegetarian, is_lactose_free, is_gluten_free, is_vegan, is_keto
    FROM testing
    GROUP BY name, fat, protein, carbohydrate, kcal,is_vegetarian, is_lactose_free, is_gluten_free, is_vegan, is_keto
)
DELETE FROM testing
WHERE ingredient_id NOT IN (
    SELECT min_id FROM cte_duplicates
);




-- finding constaints on tables
SELECT
    conname AS constraint_name,
    contype AS constraint_type,
    conrelid::regclass AS table_name
FROM
    pg_constraint
WHERE
    conrelid = 'TABLEname'::regclass;