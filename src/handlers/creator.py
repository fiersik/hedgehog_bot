from vkbottle.bot import BotLabeler, Message

from components.rules import creator_rule
from services.creator import News
# ==============================

creator = BotLabeler()
creator.vbml_ignore_case = True
creator.auto_rules.append(creator_rule())
# ==============================


@creator.message(text=["Запустить рассылку", "Запустить рассылку <text>"])
async def urgent_mailing(m: Message, text=None):

    return await News.start(m, text)


@creator.message(text="Рассылка инфо")
async def mailing_information(m: Message):

    await News.info(m)
