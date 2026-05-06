from datetime import datetime
from peewee import Model, CharField, IntegerField, FloatField, DateField, ForeignKeyField, AutoField
from app.extensions.extensions import db


class BaseModel(Model):
    id = AutoField()
    created_at = DateField(default=datetime.now)

    class Meta:
        database = db


class Ingredient(BaseModel):
    name = CharField()
    quantity = FloatField()
    unit = CharField()
    category = CharField()
    expiry_date = DateField(null=True)
    notes = CharField(null=True)
    updated_at = DateField(default=datetime.now)


class Food(BaseModel):
    name = CharField()
    description = CharField(null=True)
    food_type = CharField()
    serving_size = CharField(null=True)
    category = CharField()
    expiry_date = DateField(null=True)
    notes = CharField(null=True)
    updated_at = DateField(default=datetime.now)


class Recipe(BaseModel):
    title = CharField()
    description = CharField(null=True)
    prep_time_minutes = IntegerField()
    cook_time_minutes = IntegerField()
    servings = IntegerField()
    tips = CharField(null=True)


class RecipeIngredient(BaseModel):
    recipe = ForeignKeyField(Recipe, backref="ingredients")
    item = CharField()
    amount = CharField()
    unit = CharField(null=True)
    preparation = CharField(null=True)


class RecipeMissingIngredient(BaseModel):
    recipe = ForeignKeyField(Recipe, backref="missing_ingredients")
    item = CharField()
    amount = CharField()
    unit = CharField(null=True)
    substitute = CharField(null=True)


class RecipeInstruction(BaseModel):
    recipe = ForeignKeyField(Recipe, backref="instructions")
    step_number = IntegerField()
    instruction = CharField()


def init_db():
    with db:
        db.create_tables([Ingredient, Food, Recipe, RecipeIngredient, RecipeMissingIngredient, RecipeInstruction])
