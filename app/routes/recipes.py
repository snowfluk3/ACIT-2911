from flask import Blueprint, jsonify, request
from ..models.model import Recipe, RecipeIngredient, RecipeInstruction, RecipeMissingIngredient, Ingredient
from ..extensions.recipe import generate_recipes

recipe_bp = Blueprint("recipes", __name__, url_prefix="/recipes")

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


@recipe_bp.route("/recipes", methods=["GET"])
def list_recipes():
    return jsonify([r.__data__ for r in Recipe.select()])


@recipe_bp.route("/recipes/<int:id>", methods=["GET"])
def get_recipe(id):
    recipe = Recipe.get_or_none(Recipe.id == id)
    if recipe is None:
        return jsonify({"error": f"Recipe {id} not found"}), 404
    return jsonify(recipe_to_dict(recipe))


@recipe_bp.route("/recipes/<int:id>", methods=["DELETE"])
def delete_recipe(id):
    recipe = Recipe.get_or_none(Recipe.id == id)
    if recipe is None:
        return jsonify({"error": f"Recipe {id} not found"}), 404
    RecipeIngredient.delete().where(RecipeIngredient.recipe == recipe).execute()
    RecipeMissingIngredient.delete().where(RecipeMissingIngredient.recipe == recipe).execute()
    RecipeInstruction.delete().where(RecipeInstruction.recipe == recipe).execute()
    recipe.delete_instance()
    return "", 204


@recipe_bp.route("/recipes/generate", methods=["POST"])
def recipes_generate():
    ingredients = [i.__data__ for i in Ingredient.select()]
    
    # Automatically saves all 3 generated recipes to the DB 
    # (Can be changed later when merged with the recipe generation frontend)
    raw_recipes = generate_recipes(ingredients)
    saved = [save_recipe(r) for r in raw_recipes]
    return jsonify([recipe_to_dict(r) for r in saved]), 201

