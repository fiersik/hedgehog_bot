# ==============================
from vkbottle.bot import Message, BotLabeler

from config import DB
from modules import admin_rule
# ==============================

admin = BotLabeler()
admin.vbml_ignore_case = True
# ==============================


@admin.chat_message(admin_rule(), text="подписаться на рассылку")
async def news(m: Message):
    if DB.chat.newsletter(m.peer_id, True):
        await m.answer(
            "Вы подписались на рассылку."
            "Каждые 2 часа вашей беседе будет приходить ёжик."
        )
        return

    await m.answer(
        "Вы уже подписаны на рассылку."
    )


@admin.chat_message(admin_rule(), text="Отписаться от рассылки")
async def no_news(m: Message):

    if DB.chat.newsletter(m.peer_id, False):
        await m.answer(
            "Вы отписались от рассылки :("
        )
        return

    await m.answer("вы не подписаны на рассылку.")
