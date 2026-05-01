from peewee import SqliteDatabase, Model, CharField, IntegerField, DateField

db = SqliteDatabase("pantry.db")


class Ingredient(Model):
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



def init_db():
    with db:
        db.create_tables([Ingredient])
