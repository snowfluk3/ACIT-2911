from datetime import date, timedelta
from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required
from ..models.model import Food

food_bp = Blueprint("food", __name__, url_prefix="/food")

_OOB_CLEAR = '<div id="food-form-container" hx-swap-oob="innerHTML"></div>'


def _items_html():
    today = date.today()
    return render_template(
        "_food_items.html",
        items=list(Food.select().where(Food.user == current_user).dicts()),
        today=today,
        warning_days=today + timedelta(days=3),
    )


@food_bp.route("/page")
@login_required
def food_page():
    today = date.today()
    items = list(Food.select().where(Food.user == current_user).dicts())
    return render_template(
        "food.html",
        items=items,
        today=today,
        warning_days=today + timedelta(days=3),
    )


@food_bp.route("/new", methods=["GET"])
@login_required
def new_food_form():
    return render_template("_food_form.html", item=None)


@food_bp.route("/<int:id>/edit", methods=["GET"])
@login_required
def edit_food_form(id):
    item = Food.get_or_none(Food.id == id)
    if item is None:
        return "<p class='error-message'>Item not found</p>", 404
    return render_template("_food_form.html", item=item.__data__)


@food_bp.route("/clear-form", methods=["GET"])
def clear_food_form():
    return ""


@food_bp.route("", methods=["GET"])
def list_food():
    items = [f.__data__ for f in Food.select()]
    return jsonify(items)


@food_bp.route("", methods=["POST"])
@login_required
def new_food():
    if request.headers.get("HX-Request"):
        data = request.form
        Food.create(
            user=current_user,
            name=data["name"],
            food_type="ready_to_eat",
            category=data["category"],
            description=data.get("description") or None,
            serving_size=data.get("serving_size") or None,
            expiry_date=data.get("expiry_date") or None,
            notes=data.get("notes") or None,
        )
        return _items_html() + _OOB_CLEAR

    data = request.get_json()
    item = Food.create(
        user=current_user,
        name=data["name"],
        food_type=data.get("food_type", "ready_to_eat"),
        category=data["category"],
        description=data.get("description"),
        serving_size=data.get("serving_size"),
        expiry_date=data.get("expiry_date"),
        notes=data.get("notes"),
    )
    return jsonify(item.__data__), 201


@food_bp.route("/<int:id>", methods=["GET"])
def get_food(id):
    item = Food.get_or_none(Food.id == id)
    if item is None:
        return jsonify({"error": f"Food {id} not found"}), 404
    return jsonify(item.__data__)


@food_bp.route("/<int:id>", methods=["PUT"])
@login_required
def update_food(id):
    item = Food.get_or_none(Food.id == id)
    if item is None:
        if request.headers.get("HX-Request"):
            return "<p class='error-message'>Item not found</p>", 404
        return jsonify({"error": f"Food {id} not found"}), 404

    if request.headers.get("HX-Request"):
        data = request.form
        for field in ("name", "category", "description", "serving_size"):
            if field in data:
                setattr(item, field, data[field] or None)
        if "expiry_date" in data:
            item.expiry_date = data["expiry_date"] or None
        if "notes" in data:
            item.notes = data["notes"] or None
        item.save()
        return _items_html() + _OOB_CLEAR

    data = request.get_json()
    for field in ("name", "food_type", "category", "description", "serving_size", "expiry_date", "notes"):
        if field in data:
            setattr(item, field, data[field])
    item.save()
    return jsonify(item.__data__)


@food_bp.route("/<int:id>", methods=["DELETE"])
@login_required
def delete_food(id):
    item = Food.get_or_none(Food.id == id)
    if item is None:
        if request.headers.get("HX-Request"):
            return "<p class='error-message'>Item not found</p>", 404
        return jsonify({"error": f"Food {id} not found"}), 404
    item.delete_instance()
    if request.headers.get("HX-Request"):
        return _items_html(), 200
    return "", 204
