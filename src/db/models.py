# ==============================
from peewee import (
    SqliteDatabase,
    Model,

    PrimaryKeyField,
    ForeignKeyField,
    IntegerField,
    BooleanField,
    TextField,
    DateTimeField,
    TimeField

)
# ==============================

db = SqliteDatabase("hedgehog.db")
# ==============================


class BaseModel(Model):

    id = PrimaryKeyField()

    class Meta:
        database = db
# ==============================


class Chat(BaseModel):

    peer_id = IntegerField(unique=True)
    newsletter = BooleanField(default=False)
    new_hedgehog = TextField(null=True)

    class Meta:
        db_table = "chats"
# ==============================


class User(BaseModel):

    from_id = IntegerField(unique=True)
    vip = BooleanField(default=False)
    activation_time = DateTimeField(null=True)
    deactivation_time = DateTimeField(null=True)

    class Meta:
        db_table = "users"
# ==============================


class Hedgehog(BaseModel):

    owner = ForeignKeyField(User)
    chat = ForeignKeyField(Chat)
    name = TextField(default="Мой ёжик")
    picture = TextField()
    lvl = IntegerField(default=1)
    condition = TextField(default="отличное")
    apples = IntegerField(default=50)
    hunger = IntegerField(default=24)
    food_Time = TimeField(null=True)
    working_time = TimeField(null=True)

    class Meta:
        db_table = "hedgehogs"
# ==============================
