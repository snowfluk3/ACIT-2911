from datetime import datetime
from peewee import Model, CharField, IntegerField, FloatField, DateField, DateTimeField, ForeignKeyField, AutoField
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions.extensions import db

class BaseModel(Model):
    class Meta:
        database = db

class User(UserMixin, BaseModel):
    id = AutoField()
    username = CharField(unique=True)
    email = CharField(unique=True)
    password_hash = CharField()
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = "users"

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super(User, self).save(*args, **kwargs)

    def get_id(self):
        return str(self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(str(self.password_hash), password)


class Ingredient(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref="ingredients")
    name = CharField()
    emoji = CharField(default="🥫")
    quantity = FloatField()
    unit = CharField()
    category = CharField()
    expiry_date = DateField(null=True)
    notes = CharField(null=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = "ingredients"


class Food(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref="foods")
    name = CharField()
    emoji = CharField(default="🍽️")
    description = CharField(null=True)
    food_type = CharField()
    serving_size = CharField(null=True)
    category = CharField()
    expiry_date = DateField(null=True)
    notes = CharField(null=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = "food"


class Recipe(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref="recipes")
    title = CharField()
    description = CharField(null=True)
    prep_time_minutes = IntegerField()
    cook_time_minutes = IntegerField()
    servings = IntegerField()
    tips = CharField(null=True)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = "recipes"


class RecipeIngredient(BaseModel):
    id = AutoField()
    recipe = ForeignKeyField(Recipe, backref="ingredients")
    item = CharField()
    amount = CharField()
    unit = CharField(null=True)
    preparation = CharField(null=True)

    class Meta:
        table_name = "recipe_ingredients"


class RecipeMissingIngredient(BaseModel):
    id = AutoField()
    recipe = ForeignKeyField(Recipe, backref="missing_ingredients")
    item = CharField()
    amount = CharField()
    unit = CharField(null=True)
    substitute = CharField(null=True)

    class Meta:
        table_name = "recipe_missing_ingredients"


class RecipeInstruction(BaseModel):
    id = AutoField()
    recipe = ForeignKeyField(Recipe, backref="instructions")
    step_number = IntegerField()
    instruction = CharField()

    class Meta:
        table_name = "recipe_instructions"


def _ensure_column(table_name, column_name, column_sql):
    existing_columns = {column.name for column in db.get_columns(table_name)}
    if column_name not in existing_columns:
        db.execute_sql(f"ALTER TABLE {table_name} ADD COLUMN {column_sql}")


def init_db():
    with db:
        db.create_tables([Ingredient, Food, Recipe, RecipeIngredient, RecipeMissingIngredient, RecipeInstruction, User])
        _ensure_column("ingredients", "emoji", "emoji TEXT NOT NULL DEFAULT '🥫'")
        _ensure_column("food", "emoji", "emoji TEXT NOT NULL DEFAULT '🍽️'")
