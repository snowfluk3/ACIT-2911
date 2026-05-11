from flask_login import login_user, logout_user, login_required
from ..extensions.extensions import login_manager
from flask import Blueprint, jsonify, request, url_for, redirect

from ..models.model import User
from werkzeug.security import check_password_hash

auth_bp = Blueprint("auth", __name__)

# Authenticate user
def authenticate(identity, password):
    user = User.get_or_none((User.username == identity) | (User.email == identity))
    
    if not user:
        print(f"Could not find {identity} in database")
        return None

    if user and user.check_password(password):
        return user
    return None

# Auth Routes
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.form

    # Check to see if user exists
    if User.get_or_none((User.username == data.get("username")) | (User.email == data.get("email"))):
        return jsonify({"success": False, "error": "Username or email already taken"}), 400
    
    # IF successful, create user
    new_user = User(username=data.get("username"), email=data.get("email"))
    new_user.set_password(password=data.get("password"))

    new_user.save()
    login_user(new_user)

    return jsonify({"success": True, "redirect": url_for("templates.dashboard")}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    login_input = request.form.get("login_input")
    password = request.form.get("password")

    user = authenticate(login_input, password)

    if user:
        login_user(user, remember=True)
        return jsonify({"success": True, "redirect": url_for("templates.dashboard")})

    return jsonify({"success": False, "error": "Invalid user credentials"}), 401

@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("templates.index"))