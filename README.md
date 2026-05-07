# Snack Stash Storeroom

Snack Stash Storeroom is a Flask web application for tracking pantry items, monitoring quantities and expiry dates, and generating recipe ideas from the ingredients a user already has. The project combines a simple browser interface with JSON API routes backed by a SQLite database.

## Team Biscuit

- Luke Umali | Scrum Master
- Taran Sidhu | Product Owner
- Jack Simpson | Development Team
- Ken Yu | Development Team
- Rajveer Khurana | Development Team

## Features (Currently Working)

- Landing page with project branding, feature descriptions, shared layout, custom styling, and static image assets.
- Login popup with client-side form handling, error display, password show/hide toggle, and Flask-Login session support.
- Logout flow for authenticated users.
- Dashboard page for logged-in users.
- Pantry item interface that can list, add, edit, and delete pantry entries from the browser.
- Ingredient API with full CRUD support at `/ingredients`.
- Food API with full CRUD support at `/food`.
- Recipe API that can list, retrieve, delete, and generate recipes at `/recipes`.
- Recipe generation service that sends pantry ingredients to a local OpenAI-compatible chat completion endpoint and saves generated recipes to the database.
- SQLite database schema for ingredients, food, recipes, recipe ingredients, missing ingredients, and recipe instructions.
- Peewee ORM models for the current database tables.

## Current Login

The app currently uses a hardcoded demo user while authentication is still being developed:

- Username: `luke`
- Password: `self1234`

## Tech Stack

- Python 3.14+
- Flask
- Flask-Login
- Peewee ORM
- SQLite
- JavaScript, HTML, and CSS
- `uv` for dependency management

## Project Structure

```text
ACIT-2911/
├── app/
│   ├── __init__.py
│   ├── extensions/
│   │   ├── extensions.py
│   │   └── recipe.py
│   ├── models/
│   │   └── model.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── food.py
│   │   ├── ingredients.py
│   │   ├── recipes.py
│   │   └── templates.py
│   ├── static/
│   │   ├── images/
│   │   ├── pantry.js
│   │   ├── script.js
│   │   └── styles.css
│   └── templates/
│       ├── dashboard.html
│       ├── index.html
│       └── layout.html
├── database/
│   ├── database.db
│   ├── schema.sql
│   └── seed.sql
├── recipe_schema.json
├── run.py
├── system_prompt.txt
├── pyproject.toml
└── uv.lock
```

## Getting Started

Install dependencies:

```powershell
uv sync
```

Run the Flask app:

```powershell
uv run python run.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Recipe Generation Setup

Recipe generation expects a local OpenAI-compatible API server running at:

```text
http://localhost:1234/v1
```

The current configuration uses the model name:

```text
qwen/qwen3.5-9b
```

The recipe prompt is stored in `system_prompt.txt`, and the expected structured JSON response is defined in `recipe_schema.json`.

If the local model server is not running, the main pantry CRUD features can still work, but `POST /recipes/generate` will fail when it tries to contact the recipe generation API.

## API Routes

### Auth

- `POST /login` - authenticate the demo user and start a session.
- `POST /logout` - log out the current user.

### Pages

- `GET /` - render the landing page.
- `GET /dashboard` - render the pantry dashboard.

### Ingredients

- `GET /ingredients` - list pantry ingredients.
- `POST /ingredients` - create a pantry ingredient.
- `GET /ingredients/<id>` - get one pantry ingredient.
- `PUT /ingredients/<id>` - update one pantry ingredient.
- `DELETE /ingredients/<id>` - delete one pantry ingredient.

### Food

- `GET /food` - list food records.
- `POST /food` - create a food record.
- `GET /food/<id>` - get one food record.
- `PUT /food/<id>` - update one food record.
- `DELETE /food/<id>` - delete one food record.

### Recipes

- `GET /recipes` - list saved recipes.
- `GET /recipes/<id>` - get one saved recipe with ingredients, missing ingredients, and instructions.
- `DELETE /recipes/<id>` - delete one saved recipe and its related records.
- `POST /recipes/generate` - generate recipe suggestions from saved ingredients and store them in the database.

## Current Development Notes

- User authentication is functional for the demo user, but accounts are not stored in the database yet.
- The dashboard pantry UI currently uses the `/ingredients` API.
- The `/food` API exists for general food records, but it is not yet connected to a dedicated frontend view.
- Recipe generation is implemented on the backend and saves generated recipes, but the recipe frontend still needs to be connected.
- The SQLite database file is currently committed for development convenience. Longer term, the schema and seed files should become the source of truth instead of tracking local database state.
