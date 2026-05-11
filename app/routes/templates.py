from flask import Blueprint, render_template
from flask_login import current_user, login_required
from ..models.model import Ingredient, Recipe
from . import recipes as recipes_mod

template_bp = Blueprint("templates", __name__)


@template_bp.route("/")
def index():
    return render_template("index.html")


@template_bp.route("/dashboard")
@login_required
def dashboard():
    user_id = int(current_user.id)
    items = list(Ingredient.select().dicts())
    recipes = [recipes_mod.recipe_to_dict(r) for r in
               Recipe.select().where(Recipe.user_id == user_id).order_by(Recipe.id.desc())]
    for r in recipes:
        r["generated_label"] = recipes_mod._relative_date(r["created_at"])
    return render_template(
        "dashboard.html",
        items=items,
        recipes=recipes,
        gen_status=recipes_mod._gen_status,
    )
