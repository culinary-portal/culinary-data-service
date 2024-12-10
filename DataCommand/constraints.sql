alter table general_recipe
alter column name set not null;


alter table ingredient
alter column name set not null;
alter table ingredient
add constraint expected_macro check (fat >= 0  and carbohydrate >= 0 and protein >= 0 and kcal >= 0
and fat <= 100 and carbohydrate <= 100 and protein <= 100 and kcal <= 900);
alter table  ingredient
add constraint valid_flags check (is_keto in (0,1) and is_vegan in (0,1) and is_gluten_free in (0,1) and
is_vegetarian in (0,1) and is_lactose_free in (0,1));


alter table contains
add constraint valid_amount check ( amount > 0 and amount < 10000 );
alter table contains
add constraint valid_measure check ( cast(measure as float) > 0 and cast(measure as float) < 10000 );



