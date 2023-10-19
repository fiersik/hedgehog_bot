from .models import Chat, User, Hedgehog
# ==============================


class ChatMethod:

    @classmethod
    def add(cls, chat_id: int):

        chat = cls.get(chat_id)
        if chat is None:
            chat = Chat(peer_id=chat_id)
            chat.save()

    @classmethod
    def get(cls, chat_id: int) -> Chat | None:

        chat: Chat | None = Chat.get_or_none(Chat.peer_id == chat_id)
        return chat

    def _get_subscribers():

        for chat in Chat.select().where(Chat.newsletter):
            yield chat

    @classmethod
    def get_subscribers_id(cls):

        subs_id = [chat.peer_id for chat in cls._get_subscribers()]

        for i in range((len(subs_id) + 99) // 100):
            yield subs_id[i*100:(i+1)*100]

    @classmethod
    def delele(cls, chat_id: int):

        chat = cls.get(chat_id)
        chat.delete_instance()

    @classmethod
    def new_hedgehog(cls, picture: str | None = None, chat_id: int | None = None):

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

        user = User(from_id=from_id)
        user.save()
        return user

    @classmethod
    def get(cls, from_id: int) -> User:

        user: User | None = User.get_or_none(User.from_id == from_id)
        if user is None:
            user = cls.add(from_id)

        return user

    @classmethod
    def delete(cls, from_id: int):

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

        owner = DB.user.get(from_id)
        chat = DB.chat.get(chat_id)

        hedgehog: Hedgehog = Hedgehog.get_or_none(
            (Hedgehog.owner == owner) & (Hedgehog.chat == chat)
        )
        return hedgehog

    def get_all():
        for hedgehog in Hedgehog.select():
            hedgehog: Hedgehog
            yield hedgehog

    @classmethod
    def delete(
            cls,
            from_id: int,
            chat_id: int
    ):

        hedgehog = cls.get(from_id, chat_id)
        hedgehog.delete_instance()

    @classmethod
    def apples(
            cls,
            from_id: int,
            chat_id: int,
            number: int
    ):

        hedgehog = cls.get(from_id=from_id, chat_id=chat_id)
        hedgehog.apples = hedgehog.apples + number
        hedgehog.save()


class DB:

    chat = ChatMethod
    user = UserMethod
    hedgehog = HedgehogMethod
