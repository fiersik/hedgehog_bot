from vkbottle.bot import Message

from db.func import DB


class News:

    async def on(m: Message):

        if DB.chat.newsletter(m.peer_id, True):
            await m.answer(
                "Вы подписались на рассылку."
                "Каждые 2 часа вашей беседе будет приходить ёжик."
            )
            return

        await m.answer(
            "Вы уже подписаны на рассылку."
        )

    async def off(m: Message):

        if DB.chat.newsletter(m.peer_id, False):
            await m.answer(
                "Вы отписались от рассылки :("
            )
            return

        await m.answer("вы не подписаны на рассылку.")
