from flask_login import LoginManager
from peewee import SqliteDatabase


# Flask Login
login_manager = LoginManager()

# Database Initalization
db = SqliteDatabase(None)

