from flask import Blueprint, jsonify, request
from ..models.model import Food

food_bp = Blueprint("food", __name__, url_prefix="/food")

@food_bp.route("/food", methods=["GET"])
def list_food():
    items = [f.__data__ for f in Food.select()]
    return jsonify(items)


@food_bp.route("/food", methods=["POST"])
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


@food_bp.route("/food/<int:id>", methods=["GET"])
def get_food(id):
    item = Food.get_or_none(Food.id == id)
    if item is None:
        return jsonify({"error": f"Food {id} not found"}), 404
    return jsonify(item.__data__)


@food_bp.route("/food/<int:id>", methods=["PUT"])
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


@food_bp.route("/food/<int:id>", methods=["DELETE"])
def delete_food(id):
    item = Food.get_or_none(Food.id == id)
    if item is None:
        return jsonify({"error": f"Food {id} not found"}), 404
    item.delete_instance()
    return "", 204