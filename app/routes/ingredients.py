from flask import Blueprint, jsonify, request, render_template
from ..models.model import Ingredient

ingredients_bp = Blueprint("ingredients", __name__, url_prefix="/ingredients")

_OOB_CLEAR = '<div id="item-form-container" hx-swap-oob="innerHTML"></div>'


def _items_html():
    today = date.today()
    # Passes 'today' and 'warning_days'. Can be checked by: 'if item.expiry_date <= warning_days'
    return render_template("_pantry_items.html", items=list(Ingredient.select().dicts()), today=today.isoformat(), warning_days=(today + timedelta(days=3)).isoformat(),)


@ingredients_bp.route("/new", methods=["GET"])
def new_ingredient_form():
    return render_template("_ingredient_form.html", item=None)


@ingredients_bp.route("/<int:id>/edit", methods=["GET"])
def edit_ingredient_form(id):
    ingredient = Ingredient.get_or_none(Ingredient.id == id)
    if ingredient is None:
        return "<p class='error-message'>Item not found</p>", 404
    return render_template("_ingredient_form.html", item=ingredient.__data__)


@ingredients_bp.route("/clear-form", methods=["GET"])
def clear_ingredient_form():
    return ""


@ingredients_bp.route("", methods=["GET"])
def list_ingredients():
    ingredients = [i.__data__ for i in Ingredient.select()]
    return jsonify(ingredients)


@ingredients_bp.route("", methods=["POST"])
def new_ingredient():
    if request.headers.get("HX-Request"):
        data = request.form
        Ingredient.create(
            name=data["name"],
            quantity=float(data["quantity"]),
            unit=data.get("unit", ""),
            category=data.get("category", ""),
            expiry_date=data.get("expiry_date") or None,
            notes=data.get("notes") or None,
        )
        return _items_html() + _OOB_CLEAR

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


@ingredients_bp.route("/<int:id>", methods=["GET"])
def get_ingredient(id):
    ingredient = Ingredient.get_or_none(Ingredient.id == id)
    if ingredient is None:
        return jsonify({"error": f"Ingredient {id} not found"}), 404
    return jsonify(ingredient.__data__)


@ingredients_bp.route("/<int:id>", methods=["PUT"])
def update_ingredient(id):
    ingredient = Ingredient.get_or_none(Ingredient.id == id)
    if ingredient is None:
        if request.headers.get("HX-Request"):
            return "<p class='error-message'>Item not found</p>", 404
        return jsonify({"error": f"Ingredient {id} not found"}), 404

    if request.headers.get("HX-Request"):
        data = request.form
        for field in ("name", "unit", "category"):
            if field in data:
                setattr(ingredient, field, data[field])
        if "quantity" in data:
            ingredient.quantity = float(data["quantity"])
        if "expiry_date" in data:
            ingredient.expiry_date = data["expiry_date"] or None
        if "notes" in data:
            ingredient.notes = data["notes"] or None
        ingredient.save()
        return _items_html() + _OOB_CLEAR

    data = request.get_json()
    for field in ("name", "quantity", "unit", "category", "expiry_date", "notes"):
        if field in data:
            setattr(ingredient, field, data[field])
    ingredient.save()
    return jsonify(ingredient.__data__)


@ingredients_bp.route("/<int:id>", methods=["DELETE"])
def delete_ingredient(id):
    ingredient = Ingredient.get_or_none(Ingredient.id == id)
    if ingredient is None:
        if request.headers.get("HX-Request"):
            return "<p class='error-message'>Item not found</p>", 404
        return jsonify({"error": f"Ingredient {id} not found"}), 404
    ingredient.delete_instance()
    if request.headers.get("HX-Request"):
        return _items_html(), 200
    return "", 204
