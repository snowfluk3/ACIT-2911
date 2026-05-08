INSERT INTO users (id, username, email, password_hash)
VALUES (1, 'luke', 'luke@example.com', 'self1234');

INSERT INTO ingredients (user_id, name, quantity, unit, category, expiry_date, notes)
VALUES
(1, 'Eggs', 12, 'pcs', 'Protein', '2026-05-12', 'Use for breakfast or baking'),
(1, 'Milk', 2, 'L', 'Dairy', '2026-05-08', 'Opened carton'),
(1, 'Bread', 1, 'loaf', 'Bakery', '2026-05-06', 'Whole wheat'),
(1, 'Rice', 5, 'kg', 'Grain', NULL, 'Stored in pantry'),
(1, 'Chicken Breast', 4, 'pcs', 'Meat', '2026-05-10', 'Frozen'),
(1, 'Garlic', 8, 'cloves', 'Produce', '2026-05-28', NULL),
(1, 'Cheddar Cheese', 0.5, 'kg', 'Dairy', '2026-05-20', 'Block, unopened'),
(1, 'Fettuccine', 500, 'g', 'Grain', NULL, 'Stored in pantry');
