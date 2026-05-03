-- INGREDIENTS TABLE
CREATE TABLE ingredients (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  quantity REAL NOT NULL,
  unit TEXT NOT NULL,
  category TEXT NOT NULL,
  expiry_date TEXT,
  notes TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- FOOD TABLE
CREATE TABLE food (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  description TEXT,
  food_type TEXT NOT NULL,
  serving_size TEXT,
  category TEXT NOT NULL,
  expiry_date TEXT,
  notes TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- RECIPES TABLE
CREATE TABLE recipes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT,
  prep_time_minutes INTEGER NOT NULL,
  cook_time_minutes INTEGER NOT NULL,
  servings INTEGER NOT NULL,
  tips TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- RECIPE INGREDIENTS TABLE
CREATE TABLE recipe_ingredients (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  recipe_id INTEGER NOT NULL,
  item TEXT NOT NULL,
  amount TEXT NOT NULL,
  unit TEXT,
  preparation TEXT,
  FOREIGN KEY (recipe_id) REFERENCES recipes(id)
);

-- MISSING INGREDIENTS TABLE
CREATE TABLE recipe_missing_ingredients (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  recipe_id INTEGER NOT NULL,
  item TEXT NOT NULL,
  amount TEXT NOT NULL,
  unit TEXT,
  substitute TEXT,
  FOREIGN KEY (recipe_id) REFERENCES recipes(id)
);

-- RECIPE INSTRUCTIONS TABLE
CREATE TABLE recipe_instructions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  recipe_id INTEGER NOT NULL,
  step_number INTEGER NOT NULL,
  instruction TEXT NOT NULL,
  FOREIGN KEY (recipe_id) REFERENCES recipes(id)
);