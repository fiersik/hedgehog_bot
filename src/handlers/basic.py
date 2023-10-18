# ==============================
from datetime import datetime, timedelta

from vkbottle.bot import BotLabeler, Message

from config import DB, bot_api
# ==============================

basic = BotLabeler()
basic.vbml_ignore_case = True
# ==============================


@basic.chat_message(text="взять ёжика")
async def take_a_hedgehog(m: Message):

    user_hedgehog = DB.hedgehog.get(m.from_id, m.peer_id)
    chat_new_hedgehog = DB.chat.get(m.peer_id).new_hedgehog

    if user_hedgehog:
        return "У вас уже есть ёжик"
    if chat_new_hedgehog is None:
        return "В вашей беседе нет свободного ёжика"

    DB.hedgehog.add(
        m.from_id,
        m.peer_id,
        chat_new_hedgehog
    )
    DB.chat.new_hedgehog(chat_id=m.peer_id)
    return "Теперь у вас есть милый ёжик, посмотрите на него командой 'мой ёжик'"


@basic.chat_message(text="выкинуть ёжика")
async def remove_hedgehog(m: Message):

    if DB.hedgehog.get(m.from_id, m.peer_id) is None:
        return "У вас нет ёжика"

    await m.answer(
        "Вы навсегда потеряете своего ёжика и его статистику.\n"
        "Если вы уверены в своём решение, пропишите 'точно выкинуть ёжика'"
    )


@basic.chat_message(text="точно выкинуть ёжика")
async def exactly_remove_hedgehog(m: Message):

    if DB.hedgehog.get(m.from_id, m.peer_id) is None:
        return "У вас нет ёжика"

    user_info = (await bot_api.users.get(m.from_id))[0]
    first_name = user_info.first_name
    last_name = user_info.last_name

    DB.hedgehog.delete(m.from_id, m.peer_id)

    await m.answer(
        f"О нет, [id{m.from_id}|{first_name} {last_name}].\n"
        "Ну ты и негодяй.\n"
        "У тебя больше нет ёжика."
    )
# ==============================


@basic.chat_message(payload={"command": "my_hedgehog"})
@basic.chat_message(text="мой ёжик")
async def my_hedgehog(m: Message):

    hedgehog = DB.hedgehog.get(m.from_id, m.peer_id)
    if hedgehog is None:
        return "У вас нет ёжика"

    await m.answer(
        "Ваш ёжик:\n"
        f"Имя: {hedgehog.name}.\n"
        f"Cостояние: {hedgehog.condition}.\n"
        f"Сытость: {hedgehog.hunger}.\n"
        f"Яблочки: {hedgehog.apples}.\n",
        attachment=hedgehog.picture
    )
# ==============================


@basic.chat_message(payload={"command": "feed_hedgehog"})
@basic.chat_message(text="покормить ёжика")
async def feed_hedgehog(m: Message):

    hedgehog = DB.hedgehog.get(m.from_id, m.peer_id)
    food_time = hedgehog.food_time
    now_time = datetime.now()

    if hedgehog is None:
        return "У вас ещё нет ёжиа."
    if hedgehog.condition == "мёртв":
        return "Ваш ёжик мёртв :("
    if hedgehog.hunger == 24:
        return "Ваш ёжик не голоден."

    if food_time is None or food_time <= now_time:

        hedgehog.hunger += 1
        hedgehog.food_time = now_time + timedelta(hours=4)
        hedgehog.death_time = None
        hedgehog.condition = "отличное"
        hedgehog.save()

        return "Вы покормили вашего ёжика, он вам очень благодарен!"
    else:
        return "Кормить ёжика можно раз в 4 часа, попробуйте позже."
