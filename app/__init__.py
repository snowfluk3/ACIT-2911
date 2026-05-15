from pathlib import Path

from flask import Flask
from .extensions.extensions import login_manager, db

def create_app():
    app = Flask(__name__)
    app.secret_key = "secret"

    db.init("database/database.db")
    from .models.model import init_db
    init_db()
    login_manager.init_app(app)

    @app.context_processor
    def inject_asset_version():
        styles_path = Path(app.static_folder) / "styles.css"
        return {"asset_version": int(styles_path.stat().st_mtime)}

    # Load User
    from .models.model import User
    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.get_or_none(User.id == int(user_id))
        except (ValueError, TypeError):
            return None

    # Database Initialization
    @app.before_request
    def open_db():
        db.connect(reuse_if_open=True)

    @app.teardown_request
    def close_db(exec):
        if not db.is_closed():
            db.close()

    # Blueprints
    from .routes.ingredients import ingredients_bp
    from .routes.food import food_bp
    from .routes.recipes import recipe_bp
    from .routes.templates import template_bp
    from .routes.auth import auth_bp

    app.register_blueprint(ingredients_bp)
    app.register_blueprint(food_bp)
    app.register_blueprint(recipe_bp)
    app.register_blueprint(template_bp)
    app.register_blueprint(auth_bp)

    return app
