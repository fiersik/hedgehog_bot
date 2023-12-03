from time import time

from vkbottle.bot import Message

from db.func import DB


class News:

    async def start(m: Message, text: str):
        start_time = time()

        if text is None:
            return "Укажите текст рассылки."

        members = DB.chat.get_all_ids()

        for member in members:
            await m.ctx_api.messages.send(
                peer_ids=member,
                message=text,
                random_id=m.random_id,
                attachment=m.get_attachment_strings()
            )

        end_time = time()

        return f"Рассылка закончена.\nЗавершена за {round(end_time-start_time, 1)} сек."

    async def info(m: Message):
        members = list(DB.chat._get_subscribers())

        await m.answer(
            f"Бесед подписано на рассылку: {len(members)}\n"
            "Срочная рассылка доступна во всех беседах."
        )
