INSERT INTO ingredients (name, quantity, unit, category, expiry_date, notes)
VALUES
('Eggs', 12, 'pcs', 'Protein', '2026-05-12', 'Use for breakfast or baking'),
('Milk', 2, 'L', 'Dairy', '2026-05-08', 'Opened carton'),
('Bread', 1, 'loaf', 'Bakery', '2026-05-06', 'Whole wheat'),
('Rice', 5, 'kg', 'Grain', NULL, 'Stored in pantry'),
('Chicken Breast', 4, 'pcs', 'Meat', '2026-05-10', 'Frozen');

INSERT INTO food (name, description, food_type, serving_size, category, expiry_date, notes)
VALUES
('Chocolate Bar', 'Sweet snack item', 'snack', '1 bar', 'Snack', '2026-06-01', 'Emergency snack'),
('Instant Noodles', 'Quick ready-to-eat meal', 'ready_to_eat', '1 pack', 'Meal', '2026-12-01', 'Good backup food'),
('Granola Bar', 'Small packaged snack', 'snack', '1 bar', 'Snack', '2026-08-15', 'For school');

INSERT INTO recipes (title, description, prep_time_minutes, cook_time_minutes, servings, tips)
VALUES
('Egg Fried Rice', 'Simple fried rice using pantry ingredients', 10, 15, 2, 'Use leftover rice for best texture'),
('Chicken Sandwich', 'Quick sandwich using chicken and bread', 10, 10, 1, 'Toast the bread first');

INSERT INTO recipe_ingredients (recipe_id, item, amount, unit, preparation)
VALUES
(1, 'Rice', '2', 'cups', 'cooked'),
(1, 'Eggs', '2', 'pcs', 'beaten'),
(2, 'Bread', '2', 'slices', 'toasted'),
(2, 'Chicken Breast', '1', 'pc', 'cooked and sliced');

INSERT INTO recipe_missing_ingredients (recipe_id, item, amount, unit, substitute)
VALUES
(1, 'Green Onion', '1', 'stalk', 'onion powder'),
(2, 'Lettuce', '2', 'leaves', 'spinach');

INSERT INTO recipe_instructions (recipe_id, step_number, instruction)
VALUES
(1, 1, 'Heat oil in a pan.'),
(1, 2, 'Add eggs and scramble.'),
(1, 3, 'Add rice and stir fry together.'),
(2, 1, 'Cook and slice the chicken.'),
(2, 2, 'Toast the bread.'),
(2, 3, 'Assemble the sandwich.');