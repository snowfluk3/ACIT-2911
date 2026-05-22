from flask_login import login_user, logout_user, login_required
from ..extensions.extensions import login_manager
from flask import Blueprint, jsonify, make_response, render_template_string, request, url_for, redirect

from ..models.model import User
from werkzeug.security import check_password_hash

auth_bp = Blueprint("auth", __name__)

_ERROR_FRAGMENT = '<p class="quicksand-regular" style="color:red"><strong>{{msg}}</strong></p>'


def authenticate(identity, password):
    user = User.get_or_none((User.username == identity) | (User.email == identity))

    if not user:
        print(f"Could not find {identity} in database")
        return None

    if user and user.check_password(password):
        return user
    return None


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.form

    if User.get_or_none((User.username == data.get("username")) | (User.email == data.get("email"))):
        if request.headers.get("HX-Request"):
            return render_template_string(_ERROR_FRAGMENT, msg="Username or email already taken"), 200
        return jsonify({"success": False, "error": "Username or email already taken"}), 400

    new_user = User(username=data.get("username"), email=data.get("email"))
    new_user.set_password(password=data.get("password"))
    new_user.save()
    login_user(new_user)

    if request.headers.get("HX-Request"):
        resp = make_response("", 200)
        resp.headers["HX-Redirect"] = url_for("templates.dashboard")
        return resp
    return jsonify({"success": True, "redirect": url_for("templates.dashboard")}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    login_input = request.form.get("login_input")
    password = request.form.get("password")

    user = authenticate(login_input, password)

    if request.headers.get("HX-Request"):
        if user:
            login_user(user, remember=True)
            resp = make_response("", 200)
            resp.headers["HX-Redirect"] = url_for("templates.dashboard")
            return resp
        return render_template_string(_ERROR_FRAGMENT, msg="Invalid user credentials"), 200

    if user:
        login_user(user, remember=True)
        return jsonify({"success": True, "redirect": url_for("templates.dashboard")})
    return jsonify({"success": False, "error": "Invalid user credentials"}), 401


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("templates.index"))