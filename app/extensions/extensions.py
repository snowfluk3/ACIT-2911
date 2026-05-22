from flask import render_template
from flask_login import LoginManager
from peewee import SqliteDatabase


# Flask Login
login_manager = LoginManager()

# Database Initalization
db = SqliteDatabase(None)

# Helpers
def category_names(model, user_id):
    categories = (
        model
        .select(model.category)
        .where(model.user_id == user_id)
        .distinct()
    )

    return sorted({
        item.category.strip() 
        for item in categories 
        if item.category and item.category.strip()
    })

def _categories_oob(partial, categories):
    return render_template( 
        partial,
        categories=categories
    )
