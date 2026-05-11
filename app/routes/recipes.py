import threading
from datetime import date
from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required
from ..models.model import Recipe, RecipeIngredient, RecipeInstruction, RecipeMissingIngredient, Ingredient
from ..extensions.recipe import generate_recipes
from ..extensions.extensions import db

recipe_bp = Blueprint("recipes", __name__, url_prefix="/recipes")

_gen_status = {"state": "idle", "error": None}  # state: "idle" | "generating" | "done" | "error"


def save_recipe(r, user_id):
    recipe = Recipe.create(
        user_id=user_id,
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


def _generate_worker(ingredients, user_id):
    global _gen_status
    try:
        db.connect()
        raw = generate_recipes(ingredients)
        for r in raw:
            save_recipe(r, user_id)
        _gen_status = {"state": "done", "error": None}
    except Exception as e:
        _gen_status = {"state": "error", "error": str(e)}
    finally:
        if not db.is_closed():
            db.close()


def _relative_date(d):
    if isinstance(d, str):
        d = date.fromisoformat(d)
    elif hasattr(d, "date"):
        d = d.date()
    delta = (date.today() - d).days
    if delta == 0:
        return "today"
    if delta == 1:
        return "yesterday"
    return f"{delta} days ago"


def _render_section(user_id):
    recipes = [recipe_to_dict(r) for r in
               Recipe.select().where(Recipe.user_id == user_id).order_by(Recipe.id.desc())]
    for r in recipes:
        r["generated_label"] = _relative_date(r["created_at"])
    return render_template("_recipes_section.html", recipes=recipes, gen_status=_gen_status)


@recipe_bp.route("/status", methods=["GET"])
def generation_status():
    return jsonify(_gen_status)


@recipe_bp.route("/poll-status", methods=["GET"])
@login_required
def poll_status():
    return _render_section(int(current_user.id))


@recipe_bp.route("/rendered", methods=["GET"])
@login_required
def recipes_rendered():
    user_id = int(current_user.id)
    recipes = [recipe_to_dict(r) for r in Recipe.select().where(Recipe.user_id == user_id).order_by(Recipe.id.desc())]
    for r in recipes:
        r["generated_label"] = _relative_date(r["created_at"])
    return render_template("_recipes.html", recipes=recipes)


@recipe_bp.route("/", methods=["GET"])
def list_recipes():
    return jsonify([r.__data__ for r in Recipe.select()])


@recipe_bp.route("/<int:id>", methods=["GET"])
def get_recipe(id):
    recipe = Recipe.get_or_none(Recipe.id == id)
    if recipe is None:
        return jsonify({"error": f"Recipe {id} not found"}), 404
    return jsonify(recipe_to_dict(recipe))


@recipe_bp.route("/<int:id>", methods=["DELETE"])
def delete_recipe(id):
    recipe = Recipe.get_or_none(Recipe.id == id)
    if recipe is None:
        return jsonify({"error": f"Recipe {id} not found"}), 404
    RecipeIngredient.delete().where(RecipeIngredient.recipe == recipe).execute()
    RecipeMissingIngredient.delete().where(RecipeMissingIngredient.recipe == recipe).execute()
    RecipeInstruction.delete().where(RecipeInstruction.recipe == recipe).execute()
    recipe.delete_instance()
    return "", 204


@recipe_bp.route("/generate", methods=["POST"])
@login_required
def recipes_generate():
    global _gen_status
    user_id = int(current_user.id)
    if _gen_status["state"] != "generating":
        ingredients = [i.__data__ for i in Ingredient.select()]
        _gen_status = {"state": "generating", "error": None}
        threading.Thread(target=_generate_worker, args=(ingredients, user_id), daemon=True).start()

    if request.headers.get("HX-Request"):
        return _render_section(user_id)

    if _gen_status["state"] == "generating":
        return jsonify({"error": "Generation already in progress"}), 409
    return jsonify({"status": "started"}), 202
