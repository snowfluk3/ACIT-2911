from datetime import date, timedelta
from flask import Blueprint, render_template
from flask_login import current_user, login_required
from ..models.model import Recipe, Ingredient
from ..extensions.extensions import category_names
from . import recipes as recipes_mod
from .ingredients import _stats_context, _user_ingredients

template_bp = Blueprint("templates", __name__)

@template_bp.route("/")
def index():
    return render_template("index.html")


@template_bp.route("/dashboard")
@login_required
def dashboard():
    user_id = int(current_user.id)
    items = list(_user_ingredients(user_id).dicts())
    recipes = [recipes_mod.recipe_to_dict(r) for r in
                Recipe.select().where(Recipe.user_id == user_id).order_by(Recipe.id.desc())] #type:ignore
    for r in recipes:
        r["generated_label"] = recipes_mod._relative_date(r["created_at"])
    today = date.today()
    stats = _stats_context(user_id)

    # Dynamically generate categories
    ingredient_categories = category_names(Ingredient, user_id)

    return render_template(
        "dashboard.html",
        items=items,
        recipes=recipes,
        categories=ingredient_categories,
        gen_status=recipes_mod._gen_status,
        today=today,
        warning_days=today + timedelta(days=3),
        **stats,
    )

@template_bp.route("/about")
def about():
    return render_template("about.html")


@template_bp.route("/contact")
def contact():
    return render_template("contact.html")
