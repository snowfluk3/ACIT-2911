from datetime import datetime
from peewee import Model, CharField, IntegerField, FloatField, DateField, ForeignKeyField, AutoField
from app.extensions.extensions import db

class BaseModel(Model):
    class Meta:
        database = db

class Ingredient(Model):
    id = AutoField()
    name = CharField()
    quantity = FloatField()
    unit = CharField()
    category = CharField()
    expiry_date = DateField(null=True)
    notes = CharField(null=True)
    created_at = DateField(default=datetime.now)
    updated_at = DateField(default=datetime.now)

    class Meta:
        database = db


class Food(Model):
    id = AutoField()
    name = CharField()
    description = CharField(null=True)
    food_type = CharField()
    serving_size = CharField(null=True)
    category = CharField()
    expiry_date = DateField(null=True)
    notes = CharField(null=True)
    created_at = DateField(default=datetime.now)
    updated_at = DateField(default=datetime.now)

    class Meta:
        database = db


class Recipe(Model):
    id = AutoField()
    title = CharField()
    description = CharField(null=True)
    prep_time_minutes = IntegerField()
    cook_time_minutes = IntegerField()
    servings = IntegerField()
    tips = CharField(null=True)
    created_at = DateField(default=datetime.now)

    class Meta:
        database = db


class RecipeIngredient(Model):
    id = AutoField()
    recipe = ForeignKeyField(Recipe, backref="ingredients")
    item = CharField()
    amount = CharField()
    unit = CharField(null=True)
    preparation = CharField(null=True)

    class Meta:
        database = db


class RecipeMissingIngredient(Model):
    id = AutoField()
    recipe = ForeignKeyField(Recipe, backref="missing_ingredients")
    item = CharField()
    amount = CharField()
    unit = CharField(null=True)
    substitute = CharField(null=True)

    class Meta:
        database = db


class RecipeInstruction(Model):
    id = AutoField()
    recipe = ForeignKeyField(Recipe, backref="instructions")
    step_number = IntegerField()
    instruction = CharField()

    class Meta:
        database = db


def init_db():
    with db:
        db.create_tables([Ingredient, Food, Recipe, RecipeIngredient, RecipeMissingIngredient, RecipeInstruction])
