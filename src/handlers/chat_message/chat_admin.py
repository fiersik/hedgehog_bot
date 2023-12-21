# ==============================
from vkbottle.bot import Message, BotLabeler

from components.rules import admin_rule
from services.admin import News
# ==============================

admin = BotLabeler()
admin.vbml_ignore_case = True
admin.auto_rules.append(admin_rule())
# ==============================


@admin.chat_message(text="подписаться на рассылку")
async def news_handler(m: Message):

    await News.on(m)


@admin.chat_message(text="Отписаться от рассылки")
async def no_news_handler(m: Message):

    await News.off(m)