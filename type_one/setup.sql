insert into ingredients_ingredient values (0, 'sugar', 8, 70, 0, 100, 0, 400);
insert into ingredients_ingredient values (1, 'milk', 0.5,30, 3, 4, 2, 60);
insert into ingredients_ingredient values (2, 'ray_bread', 4, 50, 1, 44, 4, 210);
insert into ingredients_ingredient values (3, 'wheat_bread', 5, 80, 1, 49, 1, 238);
insert into ingredients_ingredient values (4, 'potato_boiled', 1.5, 65, 0, 18, 2, 79);
insert into ingredients_ingredient values (5, 'potato_fried', 2.8, 95, 9, 24, 1, 192);
insert into ingredients_ingredient values (6, 'spaghetti', 2, 55, 1, 27, 6, 140);
insert into ingredients_ingredient values (7, 'buckwheat', 1.5, 40, 2, 17, 4, 100);
insert into ingredients_ingredient values (8, 'rice', 2, 80, 0, 25, 2, 113);
insert into ingredients_ingredient values (9, 'butter', 0.1, 51, 83, 1, 1, 748); //GI ?
insert into ingredients_ingredient values (10, 'cheese', 0, 15, 14, 3, 11, 183);
insert into ingredients_ingredient values (11, 'sausage', 0, 28, 28, 2, 10, 300);
insert into ingredients_ingredient values (12, 'burger', 0, 40, 20, 5, 16, 266);
insert into ingredients_ingredient values (13, 'pork_boiled', 0, 0, 30, 0, 23, 376);
insert into ingredients_ingredient values (14, 'pork_fried', 0, 0, 50, 0, 11, 489);
insert into ingredients_ingredient values (15, 'beef_boiled', 0, 0, 17, 0, 26, 252);
insert into ingredients_ingredient values (16, 'beef_fried', 0, 0, 28, 0, 33, 384);
insert into ingredients_ingredient values (17, 'chicken_boiled', 0, 0, 7, 0, 25, 170);
insert into ingredients_ingredient values (18, 'chicken_fried', 0, 0, 12, 0, 26, 210);
insert into ingredients_ingredient values (19, 'egg', 0.1, 0, 12, 1, 13, 160);
insert into ingredients_ingredient values (20, 'omelette', 0.2, 50, 20, 3, 14, 250);

insert into ingredients_weightunit values (0, 'gramm');
insert into ingredients_weightunit values (1, 'ml');
insert into ingredients_weightunit values (2, 'slice');
insert into ingredients_weightunit values (3, 'glass');
insert into ingredients_weightunit values (4, 'teaspoon');
insert into ingredients_weightunit values (5, 'spoon');
insert into ingredients_weightunit values (6, 'plate');
insert into ingredients_weightunit values (7, 'piece');

insert into ingredients_ingredientunit values (DEFAULT, 1, 0, 0);
insert into ingredients_ingredientunit values (DEFAULT, 1, 1, 0);
insert into ingredients_ingredientunit values (DEFAULT, 1, 2, 0);
insert into ingredients_ingredientunit values (DEFAULT, 1, 3, 0);
insert into ingredients_ingredientunit values (DEFAULT, 1, 4, 0);
insert into ingredients_ingredientunit values (DEFAULT, 1, 5, 0);
insert into ingredients_ingredientunit values (DEFAULT, 1, 6, 0);
insert into ingredients_ingredientunit values (DEFAULT, 1, 7, 0);
insert into ingredients_ingredientunit values (DEFAULT, 1, 8, 0);
insert into ingredients_ingredientunit values (DEFAULT, 1, 9, 0);
insert into ingredients_ingredientunit values (DEFAULT, 1, 10, 0);
insert into ingredients_ingredientunit values (DEFAULT, 1, 11, 0);
insert into ingredients_ingredientunit values (DEFAULT, 1, 12, 0);
insert into ingredients_ingredientunit values (DEFAULT, 1, 13, 0);
insert into ingredients_ingredientunit values (DEFAULT, 1, 14, 0);
insert into ingredients_ingredientunit values (DEFAULT, 1, 15, 0);
insert into ingredients_ingredientunit values (DEFAULT, 1, 16, 0);
insert into ingredients_ingredientunit values (DEFAULT, 1, 17, 0);
insert into ingredients_ingredientunit values (DEFAULT, 1, 18, 0);
insert into ingredients_ingredientunit values (DEFAULT, 1, 19, 0);
insert into ingredients_ingredientunit values (DEFAULT, 1, 20, 0);
insert into ingredients_ingredientunit values (DEFAULT, 1.04, 1, 1); -- 1.04 grams in 1 ml of milk
insert into ingredients_ingredientunit values (DEFAULT, 35, 2, 2);   -- slice of ray bread is 35g
insert into ingredients_ingredientunit values (DEFAULT, 25, 3, 2);   -- slice of wheat bread is 25g