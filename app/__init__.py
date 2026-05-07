from flask import Flask
from .extensions.extensions import login_manager, db
from .routes.auth import find_user_by_id

def create_app():
    app = Flask(__name__)
    app.secret_key = "secret"

    db.init("database/database.db")
    login_manager.init_app(app)

    # Load User
    @login_manager.user_loader
    def load_user(user_id):
        return find_user_by_id(user_id)

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