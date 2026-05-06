from flask import Blueprint, jsonify, request
from ..models.model import Ingredient

ingredients_bp = Blueprint("ingredients", __name__, url_prefix="/ingredients")

@ingredients_bp.route("", methods=["GET"])
def list_ingredients():
    ingredients = [i.__data__ for i in Ingredient.select()]
    return jsonify(ingredients)

@ingredients_bp.route("", methods=["POST"])
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

@ingredients_bp.route("/ingredients/<int:id>", methods=["GET"])
def get_ingredient(id):
    ingredient = Ingredient.get_or_none(Ingredient.id == id)
    if ingredient is None:
        return jsonify({"error": f"Ingredient {id} not found"}), 404
    return jsonify(ingredient.__data__)


@ingredients_bp.route("/ingredients/<int:id>", methods=["PUT"])
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


@ingredients_bp.route("/ingredients/<int:id>", methods=["DELETE"])
def delete_ingredient(id):
    ingredient = Ingredient.get_or_none(Ingredient.id == id)
    if ingredient is None:
        return jsonify({"error": f"Ingredient {id} not found"}), 404
    ingredient.delete_instance()
    return "", 204