-- Seed data for Snack Stash Storeroom
-- Passwords are hashed with Werkzeug's scrypt.
-- Both demo accounts use the password: password123
--
-- To apply:
--   sqlite3 database/database.db < database/schema.sql
--   sqlite3 database/database.db < database/seed.sql

PRAGMA foreign_keys = ON;

-- Users
-- password_hash value = generate_password_hash("password123")
INSERT INTO users (username, email, password_hash, created_at, updated_at) VALUES
    ('demo',  'demo@example.com',  'scrypt:32768:8:1$gzkSQP1SCuKqTR2q$55182a1cf75caa7e9d293c0481704354523be96dc41249c87461ed87e460451ffdc49ae9eff884bdee1b76461f1c2316e4f21f2953c0ba7be68a0f9c120c3f11', datetime('now'), datetime('now')),
    ('alice', 'alice@example.com', 'scrypt:32768:8:1$XhEy8OPFnpHu37Ri$d526bcf1df7c81b21498128652c16c97f60ccc19909c3a3e3d66a0dfda4adf1f65488e80d3140eaacb9c13e198c65081e119169ed891ff696e497be90a58a0cd', datetime('now'), datetime('now'));

-- Ingredients for demo (user_id = 1)
INSERT INTO ingredients (user_id, name, emoji, quantity, unit, category, expiry_date, notes, created_at, updated_at) VALUES
    (1, 'All-Purpose Flour',  '🌾', 2.0,  'kg',  'Dry Goods',   '2026-12-01', NULL,                        datetime('now'), datetime('now')),
    (1, 'Granulated Sugar',   '🍬', 1.0,  'kg',  'Dry Goods',   '2027-06-01', NULL,                        datetime('now'), datetime('now')),
    (1, 'Olive Oil',          '🫒', 750.0,'ml',  'Oils & Fats', '2026-08-15', 'Extra virgin',              datetime('now'), datetime('now')),
    (1, 'Chicken Breast',     '🍗', 600.0,'g',   'Meat',        '2026-05-17', 'Thaw before use',           datetime('now'), datetime('now')),
    (1, 'Garlic',             '🧄', 3.0,  'cloves','Produce',   '2026-05-25', NULL,                        datetime('now'), datetime('now')),
    (1, 'Roma Tomatoes',      '🍅', 4.0,  'units','Produce',    '2026-05-18', NULL,                        datetime('now'), datetime('now')),
    (1, 'Eggs',               '🥚', 6.0,  'units','Dairy',      '2026-05-22', NULL,                        datetime('now'), datetime('now')),
    (1, 'Whole Milk',         '🥛', 1.0,  'L',   'Dairy',       '2026-05-19', NULL,                        datetime('now'), datetime('now')),
    (1, 'Cheddar Cheese',     '🧀', 250.0,'g',   'Dairy',       '2026-06-10', NULL,                        datetime('now'), datetime('now')),
    (1, 'Soy Sauce',          '🍶', 300.0,'ml',  'Condiments',  NULL,         'Low sodium',                datetime('now'), datetime('now')),
    (1, 'Basmati Rice',       '🍚', 1.5,  'kg',  'Dry Goods',   '2027-01-01', NULL,                        datetime('now'), datetime('now')),
    (1, 'Onion',              '🧅', 3.0,  'units','Produce',    '2026-05-28', NULL,                        datetime('now'), datetime('now')),
    (1, 'Cumin',              '🫙', 50.0, 'g',   'Spices',      '2027-03-01', NULL,                        datetime('now'), datetime('now')),
    (1, 'Paprika',            '🌶️', 40.0, 'g',   'Spices',      '2027-03-01', 'Smoked variety',            datetime('now'), datetime('now')),
    (1, 'Canned Chickpeas',   '🥫', 2.0,  'cans','Canned Goods','2027-09-01', NULL,                        datetime('now'), datetime('now'));

-- Ingredients for alice (user_id = 2)
INSERT INTO ingredients (user_id, name, emoji, quantity, unit, category, expiry_date, notes, created_at, updated_at) VALUES
    (2, 'Pasta',              '🍝', 500.0,'g',   'Dry Goods',   '2027-04-01', 'Spaghetti',                 datetime('now'), datetime('now')),
    (2, 'Butter',             '🧈', 200.0,'g',   'Oils & Fats', '2026-06-01', NULL,                        datetime('now'), datetime('now')),
    (2, 'Lemon',              '🍋', 3.0,  'units','Produce',    '2026-05-20', NULL,                        datetime('now'), datetime('now')),
    (2, 'Parmesan',           '🧀', 100.0,'g',   'Dairy',       '2026-07-01', 'Grated',                    datetime('now'), datetime('now')),
    (2, 'Spinach',            '🥬', 150.0,'g',   'Produce',     '2026-05-16', 'Baby spinach',              datetime('now'), datetime('now')),
    (2, 'Canned Tomatoes',    '🥫', 2.0,  'cans','Canned Goods','2027-11-01', 'Crushed',                   datetime('now'), datetime('now')),
    (2, 'Black Pepper',       '🧂', 30.0, 'g',   'Spices',      '2027-05-01', 'Whole peppercorns',         datetime('now'), datetime('now')),
    (2, 'Salt',               '🧂', 500.0,'g',   'Spices',      NULL,         NULL,                        datetime('now'), datetime('now')),
    (2, 'Bacon',              '🥓', 200.0,'g',   'Meat',        '2026-05-18', NULL,                        datetime('now'), datetime('now'));

-- Food (ready-to-eat) for demo (user_id = 1)
INSERT INTO food (user_id, name, emoji, food_type, description, serving_size, category, expiry_date, notes, created_at, updated_at) VALUES
    (1, 'Greek Yogurt',       '🍦', 'ready_to_eat', 'Plain full-fat yogurt',           '200g',  'Dairy',      '2026-05-20', NULL,              datetime('now'), datetime('now')),
    (1, 'Instant Oatmeal',    '🥣', 'ready_to_eat', 'Quick-cook oats, plain',          '1 pack','Dry Goods',  '2026-11-01', 'Add boiling water',datetime('now'), datetime('now')),
    (1, 'Protein Bar',        '🍫', 'ready_to_eat', 'Chocolate chip, 20g protein',     '1 bar', 'Snacks',     '2026-09-15', NULL,              datetime('now'), datetime('now')),
    (1, 'Orange Juice',       '🧃', 'ready_to_eat', 'Not from concentrate',            '250ml', 'Beverages',  '2026-05-19', 'Refrigerate after opening', datetime('now'), datetime('now')),
    (1, 'Sourdough Bread',    '🍞', 'ready_to_eat', 'Sliced loaf from local bakery',   '2 slices','Bakery',   '2026-05-17', NULL,              datetime('now'), datetime('now'));

-- Food (ready-to-eat) for alice (user_id = 2)
INSERT INTO food (user_id, name, emoji, food_type, description, serving_size, category, expiry_date, notes, created_at, updated_at) VALUES
    (2, 'Hummus',             '🥙', 'ready_to_eat', 'Store-bought classic hummus',     '3 tbsp','Condiments',  '2026-05-21', NULL,              datetime('now'), datetime('now')),
    (2, 'Rice Cakes',         '🍘', 'ready_to_eat', 'Lightly salted',                  '3 cakes','Snacks',    '2026-10-01', NULL,              datetime('now'), datetime('now')),
    (2, 'Sparkling Water',    '💧', 'ready_to_eat', 'Unflavoured 330ml cans',          '330ml', 'Beverages',  '2027-01-01', NULL,              datetime('now'), datetime('now'));
