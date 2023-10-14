from .models import Chat, User, Hedgehog
# ==============================


class ChatMethod:

    @classmethod
    def add(cls, chat_id: int):

        _ = Chat(peer_id=chat_id).save()

    @classmethod
    def get(cls, chat_id: int) -> Chat:

        chat: Chat = Chat.get_or_create(Chat.peer_id == chat_id)
        return chat

    def new_hedgehog(cls, chat_id: int, picture: str | None):

        chat = cls.get(chat_id=chat_id)
        chat.new_hedgehog = picture
        chat.save()

    def newsletter(cls, chat_id: int, state: bool) -> bool:

        chat = cls.get(chat_id=chat_id)
        if chat.newsletter == state:
            return False
        else:
            chat.newsletter = state
            chat.save()
            return True


class UserMethod:

    def add(cls, from_id: int):

        _ = User(from_id=from_id).save()

    def get(cls, from_id: int) -> User:

        user: User = User.get_or_create(User.from_id == from_id)
        return user


class HedgehogMethod:

    def add(
            cls,
            from_id: int,
            chat_id: int,
            picture: str,
    ):

        owner = DB.user.get(from_id)
        chat = DB.chat.get(chat_id)

        _ = Hedgehog(
            owner=owner,
            chat=chat,
            picture=picture
        ).save()

    def get(
            cls,
            from_id: int,
            chat_id: int
    ) -> Hedgehog | None:

        owner = DB.user.get(from_id)
        chat = DB.chat.get(chat_id)

        hedgehog: Hedgehog = Hedgehog.get_or_none(
            (Hedgehog.owner == owner) & (Chat.chat == chat)
        )
        return hedgehog

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
