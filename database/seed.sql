-- USERS
INSERT INTO users (username, email, password_hash)
VALUES
('kenyu', 'ken@example.com', 'hashed_password_123'),
('alice', 'alice@example.com', 'hashed_password_456'),
('bob', 'bob@example.com', 'hashed_password_789');

-- INGREDIENTS
INSERT INTO ingredients (
    user_id,
    name,
    emoji,
    quantity,
    unit,
    category,
    expiry_date,
    notes
)
VALUES
(1, 'Milk', '🥛', 2, 'L', 'Dairy', '2026-05-20', '2% milk'),
(1, 'Eggs', '🥚', 12, 'pcs', 'Protein', '2026-05-25', 'Free range'),
(1, 'Rice', '🍚', 5, 'kg', 'Grains', '2027-01-01', 'Jasmine rice'),
(2, 'Chicken Breast', '🍗', 1.5, 'kg', 'Meat', '2026-05-18', 'Boneless'),
(2, 'Broccoli', '🥦', 3, 'pcs', 'Vegetables', '2026-05-17', 'Fresh'),
(3, 'Cheddar Cheese', '🧀', 500, 'g', 'Dairy', '2026-06-01', 'Sharp cheddar');

-- FOOD
INSERT INTO food (
    user_id,
    name,
    emoji,
    food_type,
    description,
    serving_size,
    category,
    expiry_date,
    notes
)
VALUES
(1, 'Frozen Pizza', '🍕', 'ready_to_eat', 'Pepperoni frozen pizza', '1 pizza', 'Frozen Food', '2026-08-01', 'Keep frozen'),
(1, 'Caesar Salad', '🥗', 'prepared_meal', 'Fresh salad bowl', '1 bowl', 'Salad', '2026-05-16', 'Eat soon'),
(2, 'Chocolate Cake', '🍰', 'dessert', 'Birthday cake slice', '1 slice', 'Dessert', '2026-05-19', 'Contains nuts'),
(3, 'Sushi Pack', '🍣', 'ready_to_eat', 'Assorted sushi tray', '12 pcs', 'Japanese Food', '2026-05-16', 'Raw fish');

-- RECIPES
INSERT INTO recipes (
    user_id,
    title,
    description,
    prep_time_minutes,
    cook_time_minutes,
    servings,
    tips
)
VALUES
(
    1,
    'Chicken Fried Rice',
    'Simple homemade fried rice with chicken and vegetables',
    15,
    20,
    4,
    'Use cold rice for better texture'
),
(
    2,
    'Cheesy Broccoli Bake',
    'Oven baked broccoli with cheddar cheese',
    10,
    30,
    3,
    'Add breadcrumbs for crunch'
);

-- RECIPE INGREDIENTS
INSERT INTO recipe_ingredients (
    recipe_id,
    item,
    amount,
    unit,
    preparation
)
VALUES
(1, 'Rice', '3', 'cups', 'Cooked'),
(1, 'Chicken Breast', '300', 'g', 'Diced'),
(1, 'Eggs', '2', 'pcs', 'Beaten'),
(1, 'Soy Sauce', '2', 'tbsp', NULL),

(2, 'Broccoli', '2', 'pcs', 'Chopped'),
(2, 'Cheddar Cheese', '200', 'g', 'Shredded'),
(2, 'Milk', '1', 'cup', NULL);

-- RECIPE MISSING INGREDIENTS
INSERT INTO recipe_missing_ingredients (
    recipe_id,
    item,
    amount,
    unit,
    substitute
)
VALUES
(1, 'Green Onion', '2', 'stalks', 'Regular onion'),
(1, 'Sesame Oil', '1', 'tbsp', 'Olive oil'),
(2, 'Breadcrumbs', '1', 'cup', 'Crushed crackers');

-- RECIPE INSTRUCTIONS
INSERT INTO recipe_instructions (
    recipe_id,
    step_number,
    instruction
)
VALUES
(1, 1, 'Heat oil in a large pan over medium heat.'),
(1, 2, 'Cook diced chicken until fully cooked.'),
(1, 3, 'Add eggs and scramble lightly.'),
(1, 4, 'Add rice and soy sauce, then stir fry everything together.'),
(1, 5, 'Serve hot with green onions.'),

(2, 1, 'Preheat oven to 375F.'),
(2, 2, 'Steam broccoli until slightly tender.'),
(2, 3, 'Place broccoli in baking dish and add cheese.'),
(2, 4, 'Pour milk evenly over the dish.'),
(2, 5, 'Bake for 30 minutes until golden brown.');