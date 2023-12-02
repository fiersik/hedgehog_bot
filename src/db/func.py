from .models import Chat, User, Hedgehog
from components.tools import gen_list
# ==============================


class ChatMethod:

    @classmethod
    def add(cls, chat_id: int):
        """создание записи чата"""
        chat = cls.get(chat_id)
        if chat is None:
            chat = Chat(peer_id=chat_id)
            chat.save()

    @classmethod
    def get(cls, chat_id: int) -> Chat | None:
        """получение записи чата"""
        chat: Chat | None = Chat.get_or_none(Chat.peer_id == chat_id)
        return chat

    def _get_subscribers():
        """получение подписчиков рассылки"""
        for chat in Chat.select().where(Chat.newsletter):
            yield chat

    @classmethod
    def get_subscribers_id(cls):
        """получение id подписчиков рассылки"""
        subs_id = [chat.peer_id for chat in cls._get_subscribers()]
        return gen_list(subs_id, 100)

    @classmethod
    def delele(cls, chat_id: int):
        """удаление записи чата"""
        chat = cls.get(chat_id)
        chat.delete_instance()

    @classmethod
    def new_hedgehog(cls, picture: str | None = None, chat_id: int | None = None):
        """указывает нового ёжика для рассылки"""
        if picture is None:
            chat = cls.get(chat_id)
            chat.new_hedgehog = None
            chat.save()
            return

        for chat in cls._get_subscribers():
            chat.new_hedgehog = picture
            chat.save()

    @classmethod
    def newsletter(cls, chat_id: int, state: bool) -> bool:
        """изменяет статус подписки на рассылку"""
        chat = cls.get(chat_id=chat_id)
        if chat.newsletter == state:
            return False
        else:
            chat.newsletter = state
            chat.save()
            return True


class UserMethod:

    @classmethod
    def add(cls, from_id: int) -> User:
        """создание записи пользователя"""
        user = User(from_id=from_id)
        user.save()
        return user

    @classmethod
    def get(cls, from_id: int) -> User:
        """получение записи пользователя"""
        user: User | None = User.get_or_none(User.from_id == from_id)
        if user is None:
            user = cls.add(from_id)

        return user

    @classmethod
    def delete(cls, from_id: int):
        """удаление записи пользователя"""
        user = cls.get(from_id)
        user.delete_instance()


class HedgehogMethod:

    @classmethod
    def add(
            cls,
            from_id: int,
            chat_id: int,
            picture: str,
    ):
        """создание записи ёжика"""
        owner = DB.user.get(from_id)
        chat = DB.chat.get(chat_id)

        hedgehog = Hedgehog(
            owner=owner,
            chat=chat,
            picture=picture
        )
        hedgehog.save()

    @classmethod
    def get(
            cls,
            from_id: int,
            chat_id: int
    ) -> Hedgehog | None:
        """получение записи ёжика"""
        owner = DB.user.get(from_id)
        chat = DB.chat.get(chat_id)

        hedgehog: Hedgehog = Hedgehog.get_or_none(
            (Hedgehog.owner == owner) & (Hedgehog.chat == chat)
        )
        return hedgehog

    def get_all():
        """получение всех ёжиков"""
        for hedgehog in Hedgehog.select():
            hedgehog: Hedgehog
            yield hedgehog

    @classmethod
    def delete(
            cls,
            from_id: int,
            chat_id: int
    ):
        """удаление записи ёжика"""
        hedgehog = cls.get(from_id, chat_id)
        hedgehog.delete_instance()

    @classmethod
    def up_mood(
            cls,
            mood: int,
            from_id: int | None = None,
            chat_id: int | None = None,
            hedgehog: Hedgehog = None
    ):
        """меняет настроения ёжика"""
        if hedgehog is None:
            hedgehog = cls.get(from_id, chat_id)
        hedgehog.mood += mood
        if hedgehog.mood > 30:
            upped_mood = mood - hedgehog.mood + 30
            hedgehog.mood = 30
        elif hedgehog.mood < 0:
            upped_mood = mood + - hedgehog.mood
            hedgehog.mood = 0
        else:
            upped_mood = mood
        hedgehog.save()
        return int(upped_mood)


class DB:

    chat = ChatMethod
    user = UserMethod
    hedgehog = HedgehogMethod
