# ==============================
from vkbottle.bot import BotLabeler, Message

from db.models import Chat, Hedgehog
from components.keyboards import Mykeyboard as MK
from services.basic import Actions, Food, Info, Transfer, Work
# ==============================

basic = BotLabeler()
basic.vbml_ignore_case = True
# ==============================


@basic.chat_message(text="взять ёжика")
async def take_a_hedgehog_handler(m: Message, hedgehog: Hedgehog | None, chat: Chat):

    return await Actions.take_a_hedgehog(
        m, hedgehog, chat
    )


@basic.chat_message(text=["дать ёжику имя", "дать ёжику имя <name>"])
async def set_name_handler(
        _: Message, hedgehog: Hedgehog | None,
        chat: Chat, name: str | None = None):

    return await Actions.set_name(hedgehog, name)


@basic.chat_message(text="выкинуть ёжика")
async def remove_hedgehog_handler(_: Message, hedgehog: Hedgehog | None):

    return await Actions.remove_hedgehog(hedgehog)


@basic.chat_message(text="точно выкинуть ёжика")
async def exactly_remove_hedgehog_handler(m: Message, hedgehog: Hedgehog | None):

    await Actions.exactly_remove_hedgehog(m, hedgehog)
# ==============================


@basic.chat_message(payload={"command": "my_hedgehog"})
@basic.chat_message(text="мой ёжик")
async def my_hedgehog(m: Message, hedgehog: Hedgehog | None):

    if hedgehog is None:
        return "У вас нет ёжика"

    await m.answer(
        "Ваш ёжик:\n"
        f"Имя: {hedgehog.name}.\n"
        f"Cостояние: {hedgehog.condition}.\n"
        f"Настроение: {hedgehog.mood}.\n"
        f"Сытость: {hedgehog.hunger}.\n"
        f"Яблочки: {hedgehog.apples}.\n",
        keyboard=MK.my_hedgehog,
        attachment=hedgehog.picture
    )


@basic.chat_message(payload={"command": "hedgehog_info"})
@basic.chat_message(text="ёжик инфо")
async def hedgehog_information_handler(m: Message, hedgehog: Hedgehog | None):

    return await Info.hedgehog_information(m, hedgehog)
# ==============================


@basic.chat_message(payload={"command": "feed_hedgehog"})
@basic.chat_message(text="покормить ёжика")
async def feed_hedgehog_handler(m: Message, hedgehog: Hedgehog | None):

    return await Food.feed_hedgehog(hedgehog)
# ==============================


@basic.chat_message(text="отправить ёжика на работу")
@basic.chat_message(payload={"command": "send_to_work"})
async def send_to_work_handler(m: Message, hedgehog: Hedgehog | None):

    return await Work.send(hedgehog)


@basic.chat_message(text="забрать ёжика с работы")
@basic.chat_message(payload={"command": "pick_from_work"})
async def pick_from_work_handler(m: Message, hedgehog: Hedgehog):

    return await Work.pick(m, hedgehog)
# ==============================


@basic.chat_message(text="передать яблочки <quantity> <user>")
async def give_the_item_handler(m: Message, hedgehog:  Hedgehog, quantity: str, user: str):

    return await Transfer.give_the_item(m, hedgehog, quantity, user)
