from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required

from model import db, init_db, Ingredient, Food, Recipe, RecipeIngredient, RecipeMissingIngredient, RecipeInstruction
from recipe import generate_recipes
from auth import authenticate, users

import os
from dotenv import load_dotenv

app = Flask(__name__)

def run():
    app.run(debug=True)

login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key = "secret"

@app.before_request
def open_db():
    db.connect(reuse_if_open=True)


@app.teardown_request
def close_db(exc):
    if not db.is_closed():
        db.close()


init_db()

"""Render HTML Pages"""
@app.route("/")
def index():
    return render_template("index.html")

"""CRUD Operations"""
@app.route("/ingredients", methods=["GET"])
def list_ingredients():
    ingredients = [i.__data__ for i in Ingredient.select()]
    return jsonify(ingredients)


@app.route("/ingredients", methods=["POST"])
def new_ingredient():
    data = request.get_json()
    ingredient = Ingredient.create(
        name=data["name"],
        quantity=data["quantity"],
        unit=data["unit"],
        category=data["category"],
        expiry_date=data.get("expiry_date"),
        notes=data.get("notes"),
    )
    return jsonify(ingredient.__data__), 201


@app.route("/ingredients/<int:id>", methods=["GET"])
def get_ingredient(id):
    ingredient = Ingredient.get_or_none(Ingredient.id == id)
    if ingredient is None:
        return jsonify({"error": f"Ingredient {id} not found"}), 404
    return jsonify(ingredient.__data__)


@app.route("/ingredients/<int:id>", methods=["PUT"])
def update_ingredient(id):
    ingredient = Ingredient.get_or_none(Ingredient.id == id)
    if ingredient is None:
        return jsonify({"error": f"Ingredient {id} not found"}), 404
    data = request.get_json()
    for field in ("name", "quantity", "unit", "category", "expiry_date", "notes"):
        if field in data:
            setattr(ingredient, field, data[field])
    ingredient.save()
    return jsonify(ingredient.__data__)


@app.route("/ingredients/<int:id>", methods=["DELETE"])
def delete_ingredient(id):
    ingredient = Ingredient.get_or_none(Ingredient.id == id)
    if ingredient is None:
        return jsonify({"error": f"Ingredient {id} not found"}), 404
    ingredient.delete_instance()
    return "", 204


@app.route("/food", methods=["GET"])
def list_food():
    items = [f.__data__ for f in Food.select()]
    return jsonify(items)


@app.route("/food", methods=["POST"])
def new_food():
    data = request.get_json()
    item = Food.create(
        name=data["name"],
        food_type=data["food_type"],
        category=data["category"],
        description=data.get("description"),
        serving_size=data.get("serving_size"),
        expiry_date=data.get("expiry_date"),
        notes=data.get("notes"),
    )
    return jsonify(item.__data__), 201


@app.route("/food/<int:id>", methods=["GET"])
def get_food(id):
    item = Food.get_or_none(Food.id == id)
    if item is None:
        return jsonify({"error": f"Food {id} not found"}), 404
    return jsonify(item.__data__)


@app.route("/food/<int:id>", methods=["PUT"])
def update_food(id):
    item = Food.get_or_none(Food.id == id)
    if item is None:
        return jsonify({"error": f"Food {id} not found"}), 404
    data = request.get_json()
    for field in ("name", "food_type", "category", "description", "serving_size", "expiry_date", "notes"):
        if field in data:
            setattr(item, field, data[field])
    item.save()
    return jsonify(item.__data__)


@app.route("/food/<int:id>", methods=["DELETE"])
def delete_food(id):
    item = Food.get_or_none(Food.id == id)
    if item is None:
        return jsonify({"error": f"Food {id} not found"}), 404
    item.delete_instance()
    return "", 204


def save_recipe(r):
    recipe = Recipe.create(
        title=r["title"],
        description=r.get("description"),
        prep_time_minutes=r["prep_time_minutes"],
        cook_time_minutes=r["cook_time_minutes"],
        servings=r["servings"],
        tips=r.get("tips"),
    )
    RecipeIngredient.insert_many(
        [{"recipe": recipe, "item": i["item"], "amount": i["amount"],
          "unit": i.get("unit"), "preparation": i.get("preparation")}
         for i in r["ingredients_used"]]
    ).execute()
    RecipeMissingIngredient.insert_many(
        [{"recipe": recipe, "item": i["item"], "amount": i["amount"],
          "unit": i.get("unit"), "substitute": i.get("substitute")}
         for i in r["missing_ingredients"]]
    ).execute()
    RecipeInstruction.insert_many(
        [{"recipe": recipe, "step_number": idx + 1, "instruction": step}
         for idx, step in enumerate(r["instructions"])]
    ).execute()
    return recipe


def recipe_to_dict(recipe):
    return {
        **recipe.__data__,
        "ingredients_used": [i.__data__ for i in recipe.ingredients],
        "missing_ingredients": [m.__data__ for m in recipe.missing_ingredients],
        "instructions": [
            i.__data__ for i in recipe.instructions.order_by(RecipeInstruction.step_number)
        ],
    }


@app.route("/recipes", methods=["GET"])
def list_recipes():
    return jsonify([r.__data__ for r in Recipe.select()])


@app.route("/recipes/<int:id>", methods=["GET"])
def get_recipe(id):
    recipe = Recipe.get_or_none(Recipe.id == id)
    if recipe is None:
        return jsonify({"error": f"Recipe {id} not found"}), 404
    return jsonify(recipe_to_dict(recipe))


@app.route("/recipes/<int:id>", methods=["DELETE"])
def delete_recipe(id):
    recipe = Recipe.get_or_none(Recipe.id == id)
    if recipe is None:
        return jsonify({"error": f"Recipe {id} not found"}), 404
    RecipeIngredient.delete().where(RecipeIngredient.recipe == recipe).execute()
    RecipeMissingIngredient.delete().where(RecipeMissingIngredient.recipe == recipe).execute()
    RecipeInstruction.delete().where(RecipeInstruction.recipe == recipe).execute()
    recipe.delete_instance()
    return "", 204


@app.route("/recipes/generate", methods=["POST"])
def recipes_generate():
    ingredients = [i.__data__ for i in Ingredient.select()]
    
    # Automatically saves all 3 generated recipes to the DB 
    # (Can be changed later when merged with the recipe generation frontend)
    raw_recipes = generate_recipes(ingredients)
    saved = [save_recipe(r) for r in raw_recipes]
    return jsonify([recipe_to_dict(r) for r in saved]), 201

"""Login Authentication"""

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    user = authenticate(username, password)

    if user:
        login_user(user, remember=True)
        return jsonify({"success": True, "redirect": url_for("index")})

    return jsonify({"success": False, "error": "Invalid user credentials"}), 401

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

# Run the file
if __name__ == "__main__":
    run()
