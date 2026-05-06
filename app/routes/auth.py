from flask_login import UserMixin, login_user, logout_user, login_required
from ..extensions.extensions import login_manager
from flask import Blueprint, jsonify, request, url_for, redirect
# from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, id: str, username: str, password: str):
        self.id = id
        self.username = username
        self.password = password

users = {
    "1": User("1", "luke", "self1234")
}

# Find user in database
def find_user_by_username(username):
    for user in users.values():
        if user.username == username:
            return user
    return None

# Find user by id
def find_user_by_id(user_id):
    for user in users.values():
        if user.id == user_id:
            return user
    return None

# Authenticate user
def authenticate(username, password):
    user = find_user_by_username(username)

    if not user:
        return None
    
    if password == user.password:
        return user
    
    return None



# Auth Routes
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    user = authenticate(username, password)

    if user:
        login_user(user, remember=True)
        return jsonify({"success": True, "redirect": url_for("templates.index")})

    return jsonify({"success": False, "error": "Invalid user credentials"}), 401

@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("templates.index"))