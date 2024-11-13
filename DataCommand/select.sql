select * from ingredient;


insert into ingredient(name, fat, protein, carbohydrate, kcal)
select name, max(fat), max(protein), max(carbohydrate), max(kcal) from ingredient_empty
group by name;

select count(*) from ingredient;


select * from contains;

select  count(*), measure from contains group by    measure;

select * from recipe;