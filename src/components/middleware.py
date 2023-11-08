from vkbottle import BaseMiddleware
from vkbottle.bot import Message
from db.func import DB


class GetHedgehogMiddleware(BaseMiddleware[Message]):

    async def pre(self):

        hedgehog = DB.hedgehog.get(
            self.event.from_id,
            self.event.peer_id
        )

        self.send({"hedgehog": hedgehog})


class GetChatMiddleware(BaseMiddleware[Message]):

    async def pre(self):

        chat = DB.chat.get(self.event.peer_id)

        self.send({"chat": chat})


all_middleware = [GetHedgehogMiddleware, GetChatMiddleware]
