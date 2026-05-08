from flask import Blueprint, render_template

template_bp = Blueprint("templates", __name__)

@template_bp.route("/")
def index():
    return render_template("index.html")

@template_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")