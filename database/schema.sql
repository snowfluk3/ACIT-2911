PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS recipe_instructions;
DROP TABLE IF EXISTS recipe_missing_ingredients;
DROP TABLE IF EXISTS recipe_ingredients;
DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS food;
DROP TABLE IF EXISTS ingredients;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    quantity REAL NOT NULL,
    unit TEXT NOT NULL,
    category TEXT NOT NULL,
    expiry_date TEXT,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE food (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    food_type TEXT NOT NULL CHECK (food_type IN ('snack', 'ready_to_eat')),
    serving_size TEXT,
    category TEXT NOT NULL,
    expiry_date TEXT,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    prep_time_minutes INTEGER NOT NULL,
    cook_time_minutes INTEGER NOT NULL,
    servings INTEGER NOT NULL,
    tips TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE recipe_ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    item TEXT NOT NULL,
    amount TEXT NOT NULL,
    unit TEXT,
    preparation TEXT,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

CREATE TABLE recipe_missing_ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    item TEXT NOT NULL,
    amount TEXT NOT NULL,
    unit TEXT,
    substitute TEXT,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

CREATE TABLE recipe_instructions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    step_number INTEGER NOT NULL,
    instruction TEXT NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);