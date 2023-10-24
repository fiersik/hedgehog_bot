# ==============================
from datetime import datetime

from peewee import (
    SqliteDatabase,
    Model,

    AutoField,
    ForeignKeyField,
    IntegerField,
    BooleanField,
    TextField,
    DateTimeField,
)
# ==============================

db = SqliteDatabase("hedgehog.db", autoconnect=True)
# ==============================


class BaseModel(Model):
    """базовая модель"""
    id = AutoField()

    class Meta:
        database = db
# ==============================


class Chat(BaseModel):
    """модель чата"""
    peer_id = IntegerField(unique=True)
    newsletter = BooleanField(default=False)
    new_hedgehog = TextField(null=True)

    class Meta:
        table_name = "chats"
# ==============================


class User(BaseModel):
    """модель пользователя"""
    from_id = IntegerField(unique=True)
    vip = BooleanField(default=False)
    deactivation_time: datetime = DateTimeField(null=True)

    class Meta:
        table_name = "users"
# ==============================


class Hedgehog(BaseModel):
    """модель ёжика"""
    owner: User = ForeignKeyField(User)
    chat: Chat = ForeignKeyField(Chat)
    name = TextField(default="Мой ёжик")
    picture = TextField()
    lvl = IntegerField(default=1)
    xp = IntegerField(default=0)
    condition = TextField(default="отличное")
    apples = IntegerField(default=50)
    hunger = IntegerField(default=24)
    death_time = DateTimeField(null=True)
    food_time: datetime = DateTimeField(null=True)
    working_time: datetime = DateTimeField(null=True)
    at_work = BooleanField(default=False)

    class Meta:
        db_table = "hedgehogs"
# ==============================
