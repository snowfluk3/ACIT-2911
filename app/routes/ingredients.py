from datetime import date, timedelta
from flask import Blueprint, jsonify, redirect, request, render_template, url_for
from peewee import fn
from flask_login import current_user, login_required
from ..models.model import Ingredient

ingredients_bp = Blueprint("ingredients", __name__, url_prefix="/ingredients")

_OOB_CLEAR = '<div id="item-form-container" hx-swap-oob="innerHTML"></div>'


def _user_id():
    return int(current_user.id)


def _user_ingredients(user_id=None):
    owner_id = user_id if user_id is not None else _user_id()
    return Ingredient.select().where(Ingredient.user_id == owner_id) #type: ignore


def _get_user_ingredient(id):
    return Ingredient.get_or_none(
        (Ingredient.id == id) &
        (Ingredient.user_id == _user_id()) #type: ignore
    )


def _stats_context(user_id=None):
    ingredients = _user_ingredients(user_id)
    total = ingredients.count()
    top_categories = list(
        Ingredient.select(Ingredient.category, fn.COUNT(Ingredient.id).alias("n"))
        .where(Ingredient.user_id == (user_id if user_id is not None else _user_id())) # type: ignore
        .group_by(Ingredient.category)
        .order_by(fn.COUNT(Ingredient.id).desc())
        .limit(3)
        .tuples()
    )
    return dict(total=total, top_categories=top_categories)


def _stats_html():
    return render_template("_stats.html", **_stats_context())


def _stats_oob():
    return f'<div id="pantry-stats" hx-swap-oob="innerHTML">{_stats_html()}</div>'


def _items_html():
    today = date.today()
    # Passes 'today' and 'warning_days'. Can be checked by: 'if item.expiry_date <= warning_days'
    return render_template("_pantry_items.html", items=list(_user_ingredients().dicts()), today=today, warning_days=today + timedelta(days=3),)


@ingredients_bp.route("/new", methods=["GET"])
@login_required
def new_ingredient_form():
    return render_template("_ingredient_form.html", item=None)


@ingredients_bp.route("/<int:id>/edit", methods=["GET"])
@login_required
def edit_ingredient_form(id):
    ingredient = _get_user_ingredient(id)
    if ingredient is None:
        return "<p class='error-message'>Item not found</p>", 404
    return render_template("_ingredient_form.html", item=ingredient.__data__)


@ingredients_bp.route("/clear-form", methods=["GET"])
@login_required
def clear_ingredient_form():
    return ""


@ingredients_bp.route("", methods=["GET"])
@login_required
def list_ingredients():
    if request.accept_mimetypes.accept_html:
        return redirect(url_for("templates.dashboard"))

    ingredients = [i.__data__ for i in _user_ingredients()]
    return jsonify(ingredients)


@ingredients_bp.route("", methods=["POST"])
@login_required
def new_ingredient():
    if request.headers.get("HX-Request"):
        data = request.form
        Ingredient.create(
            user=current_user,
            name=data["name"],
            emoji=data.get("emoji") or "🥫",
            quantity=float(data["quantity"]),
            unit=data.get("unit", ""),
            category=data.get("category", ""),
            expiry_date=data.get("expiry_date") or None,
            notes=data.get("notes") or None,
        )
        return _items_html() + _OOB_CLEAR + _stats_oob()

    data = request.get_json()
    ingredient = Ingredient.create(
        user=current_user,
        name=data["name"],
        emoji=data.get("emoji") or "🥫",
        quantity=data["quantity"],
        unit=data["unit"],
        category=data["category"],
        expiry_date=data.get("expiry_date"),
        notes=data.get("notes"),
    )
    return jsonify(ingredient.__data__), 201


@ingredients_bp.route("/<int:id>", methods=["GET"])
@login_required
def get_ingredient(id):
    ingredient = _get_user_ingredient(id)
    if ingredient is None:
        return jsonify({"error": f"Ingredient {id} not found"}), 404
    return jsonify(ingredient.__data__)


@ingredients_bp.route("/<int:id>", methods=["PUT"])
@login_required
def update_ingredient(id):
    ingredient = _get_user_ingredient(id)
    if ingredient is None:
        if request.headers.get("HX-Request"):
            return "<p class='error-message'>Item not found</p>", 404
        return jsonify({"error": f"Ingredient {id} not found"}), 404

    if request.headers.get("HX-Request"):
        data = request.form
        for field in ("name", "emoji", "unit", "category"):
            if field in data:
                setattr(ingredient, field, data[field] or ("🥫" if field == "emoji" else ""))
        if "quantity" in data:
            ingredient.quantity = float(data["quantity"])
        if "expiry_date" in data:
            ingredient.expiry_date = data["expiry_date"] or None
        if "notes" in data:
            ingredient.notes = data["notes"] or None
        ingredient.save()
        return _items_html() + _OOB_CLEAR + _stats_oob()

    data = request.get_json()
    for field in ("name", "emoji", "quantity", "unit", "category", "expiry_date", "notes"):
        if field in data:
            setattr(ingredient, field, data[field] or ("🥫" if field == "emoji" else data[field]))
    ingredient.save()
    return jsonify(ingredient.__data__)


@ingredients_bp.route("/<int:id>", methods=["DELETE"])
@login_required
def delete_ingredient(id):
    ingredient = _get_user_ingredient(id)
    if ingredient is None:
        if request.headers.get("HX-Request"):
            return "<p class='error-message'>Item not found</p>", 404
        return jsonify({"error": f"Ingredient {id} not found"}), 404
    ingredient.delete_instance()
    if request.headers.get("HX-Request"):
        return _items_html() + _stats_oob(), 200
    return "", 204


# Filtering
@ingredients_bp.route("/filter", methods=["GET"])
def _filter_ingredients():
    today = date.today()
    user_id = int(current_user.id)
    search = request.args.get("search", "").strip().lower()
    category = request.args.get("category", "All")

    query = _user_ingredients(user_id)

    if search:
        query = query.where(
            fn.LOWER(Ingredient.name).contains(search)
        )

    if category != "All":
        query = query.where(Ingredient.category == category)

    return render_template("_pantry_items.html", items=list(query.dicts()), today=today, warning_days=today + timedelta(days=3),)
