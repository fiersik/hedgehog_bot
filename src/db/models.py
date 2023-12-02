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
    peer_id = IntegerField(unique=True)       # id чата
    newsletter = BooleanField(default=False)  # рассылка
    new_hedgehog = TextField(null=True)       # новый ёжик

    class Meta:
        table_name = "chats"
# ==============================


class User(BaseModel):
    """модель пользователя"""
    from_id = IntegerField(unique=True)                     # id пользователя
    vip = BooleanField(default=False)                       # vip статус
    deactivation_time: datetime = DateTimeField(null=True)  # время vip

    class Meta:
        table_name = "users"
# ==============================


class Hedgehog(BaseModel):
    """модель ёжика"""
    owner: User = ForeignKeyField(User)                # владелец
    chat: Chat = ForeignKeyField(Chat)                 # чат
    name = TextField(default="Мой ёжик")               # имя
    picture = TextField()                              # изображение
    lvl: int = IntegerField(default=1)                      # уровень
    xp: int = IntegerField(default=0)                       # опыт
    mood: int = IntegerField(default=30)                    # настроение
    condition = TextField(default="отличное")          # состояние
    apples: int = IntegerField(default=50)                  # яблочки
    golden_apples: int = IntegerField(default=0)            # золотые яблочки
    hunger: int = IntegerField(default=24)                  # голод
    death_time = DateTimeField(null=True)              # время смерти
    food_time: datetime = DateTimeField(null=True)     # время еды
    working_time: datetime = DateTimeField(null=True)  # время работы
    at_work = BooleanField(default=False)              # на работе

    class Meta:
        db_table = "hedgehogs"
# ==============================
