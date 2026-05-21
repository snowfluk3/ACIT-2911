from datetime import date, timedelta
from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from peewee import fn
from ..models.model import Food
from ..extensions.extensions import category_names, _categories_oob

food_bp = Blueprint("food", __name__, url_prefix="/food")

_OOB_CLEAR = '<div id="food-form-container" hx-swap-oob="innerHTML"></div>'


def _user_id():
    return int(current_user.id)


def _user_food(user_id=None):
    owner_id = user_id if user_id is not None else _user_id()
    return Food.select().where(Food.user_id == owner_id) #type: ignore


def _get_user_food(id):
    return Food.get_or_none(
        (Food.id == id) &
        (Food.user_id == _user_id()) #type: ignore
    )


def _items_html():
    today = date.today()
    return render_template(
        "_food_items.html",
        items=list(_user_food().dicts()),
        today=today,
        warning_days=today + timedelta(days=3),
    )


@food_bp.route("/page")
@login_required
def food_page():
    today = date.today()
    items = list(_user_food().dicts())

    food_categories = category_names(Food, current_user.id)
    return render_template(
        "food.html",
        categories=food_categories,
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
    item = _get_user_food(id)
    if item is None:
        return "<p class='error-message'>Item not found</p>", 404
    return render_template("_food_form.html", item=item.__data__)


@food_bp.route("/clear-form", methods=["GET"])
@login_required
def clear_food_form():
    return ""


@food_bp.route("", methods=["GET"])
@login_required
def list_food():
    if request.accept_mimetypes.accept_html:
        return redirect(url_for("food.food_page"))

    items = [f.__data__ for f in _user_food()]
    return jsonify(items)


@food_bp.route("", methods=["POST"])
@login_required
def new_food():
    if request.headers.get("HX-Request"):
        data = request.form
        Food.create(
            user=current_user,
            name=data["name"],
            emoji=data.get("emoji") or "🍽️",
            food_type="ready_to_eat",
            category=data["category"],
            description=data.get("description") or None,
            serving_size=data.get("serving_size") or None,
            expiry_date=data.get("expiry_date") or None,
            notes=data.get("notes") or None,
        )

        food_categories = category_names(Food, _user_id())
        return _items_html() + _OOB_CLEAR + _categories_oob(
            "_food_categories_oob.html",
            food_categories
        )

    data = request.get_json()
    item = Food.create(
        user=current_user,
        name=data["name"],
        emoji=data.get("emoji") or "🍽️",
        food_type=data.get("food_type", "ready_to_eat"),
        category=data["category"],
        description=data.get("description"),
        serving_size=data.get("serving_size"),
        expiry_date=data.get("expiry_date"),
        notes=data.get("notes"),
    )
    return jsonify(item.__data__), 201


@food_bp.route("/<int:id>", methods=["GET"])
@login_required
def get_food(id):
    item = _get_user_food(id)
    if item is None:
        return jsonify({"error": f"Food {id} not found"}), 404
    return jsonify(item.__data__)


@food_bp.route("/<int:id>", methods=["PUT"])
@login_required
def update_food(id):
    item = _get_user_food(id)
    if item is None:
        if request.headers.get("HX-Request"):
            return "<p class='error-message'>Item not found</p>", 404
        return jsonify({"error": f"Food {id} not found"}), 404

    if request.headers.get("HX-Request"):
        data = request.form
        for field in ("name", "emoji", "category", "description", "serving_size"):
            if field in data:
                setattr(item, field, data[field] or ("🍽️" if field == "emoji" else None))
        if "expiry_date" in data:
            item.expiry_date = data["expiry_date"] or None
        if "notes" in data:
            item.notes = data["notes"] or None
        item.save()
        food_categories = category_names(Food, _user_id())
        return _items_html() + _OOB_CLEAR + _categories_oob(
            "_food_categories_oob.html",
            food_categories
        )

    data = request.get_json()
    for field in ("name", "emoji", "food_type", "category", "description", "serving_size", "expiry_date", "notes"):
        if field in data:
            setattr(item, field, data[field] or ("🍽️" if field == "emoji" else data[field]))
    item.save()
    return jsonify(item.__data__)


@food_bp.route("/<int:id>", methods=["DELETE"])
@login_required
def delete_food(id):
    item = _get_user_food(id)
    if item is None:
        if request.headers.get("HX-Request"):
            return "<p class='error-message'>Item not found</p>", 404
        return jsonify({"error": f"Food {id} not found"}), 404
    item.delete_instance()
    food_categories = category_names(Food, _user_id())
    if request.headers.get("HX-Request"):
        return _items_html() + _categories_oob("_food_categories_oob.html", food_categories), 200
    return "", 204


# Filtering
@food_bp.route("/filter", methods=["GET"])
@login_required
def _filter_foods():
    today = date.today()
    user_id = _user_id()
    search = request.args.get("search", "").strip().lower()
    category = request.args.get("category", "All")

    query = _user_food(user_id)

    if search:
        query = query.where(
            fn.LOWER(Food.name).contains(search)
        )

    if category != "All":
        query = query.where(Food.category == category)

    return render_template("_food_items.html", items=list(query.dicts()), today=today, warning_days=today + timedelta(days=3),)
