from datetime import datetime, timedelta
import random
import re

from vkbottle.bot import Message

from components.keyboards import Mykeyboard as MK
from db.models import Chat, Hedgehog
from db.func import DB


class Actions:

    async def take_a_hedgehog(m: Message, hedgehog: Hedgehog | None, chat: Chat):

        if hedgehog:
            return "У вас уже есть ёжик"

        if chat.new_hedgehog is None:
            return "В вашей беседе нет свободного ёжика"

        DB.hedgehog.add(
            m.from_id,
            m.peer_id,
            chat.new_hedgehog
        )
        DB.chat.new_hedgehog(chat_id=m.peer_id)
        return "Теперь у вас есть милый ёжик, посмотрите на него командой 'мой ёжик'"

    async def set_name(hedgehog: Hedgehog, name: str):

        if hedgehog is None:
            return "У вас нет ёжика"
        if name is None:
            return "укажите имя для ёжика\nНапример: дать ёжику имя Раппи"

        if not name.isalpha():  # содержит не только буквенные символы
            return "Неверный формат имени."

        hedgehog.name = name
        hedgehog.save()

        return f"Теперь вашего ёжика зовут {name}."

    async def remove_hedgehog(hedgehog: Hedgehog):

        if hedgehog is None:
            return "У вас нет ёжика"
        mes = (
            "Вы навсегда потеряете своего ёжика и его статистику.\n" +
            "Если вы уверены в своём решение, пропишите 'точно выкинуть ёжика'"
        )
        return mes

    async def exactly_remove_hedgehog(m: Message, hedgehog: Hedgehog):

        if hedgehog is None:
            return "У вас нет ёжика"

        user_info = (await m.ctx_api.users.get(m.from_id))[0]
        first_name = user_info.first_name
        last_name = user_info.last_name

        DB.hedgehog.delete(m.from_id, m.peer_id)

        await m.answer(
            f"О нет, [id{m.from_id}|{first_name} {last_name}].\n"
            "Ну ты и негодяй.\n"
            "У тебя больше нет ёжика."
        )


class Food:

    async def feed_hedgehog(hedgehog: Hedgehog):

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


class Info:

    async def hedgehog_information(m: Message, hedgehog: Hedgehog):

        food_time = hedgehog.food_time
        work_time = hedgehog.working_time
        now_time = datetime.now()

        if hedgehog is None:
            return "У вас нет ёжиа."
        if hedgehog.condition == "мёртв":
            return "Ваш ёжик мёртв :("

        if hedgehog.hunger == 24:
            feeding_info = "Не голоден."
            feeding = False
        elif (food_time is None or food_time <= now_time):
            feeding_info = "Можно покормить.\n"
            feeding = True
        else:
            time_f = food_time - datetime.now()
            time_f = time_f.seconds
            hour_f = time_f / 60 // 60
            minutes_f = (time_f - hour_f*60*60) // 60
            feeding_info = f"Можно покормить через {int(hour_f)} ч. {int(minutes_f)} м.\n"
            feeding = False

        if not hedgehog.at_work:
            working_info = "Можно отправить на работу."
            send_working = True
            pick_working = False
        elif work_time < now_time:
            working_info = "Можно забрать с работы."
            send_working = False
            pick_working = True
        else:
            time_w = work_time - datetime.now()
            time_w = time_w.seconds
            hour_w = time_w / 60 // 60
            minutes_w = (time_w - hour_w*60*60) // 60
            working_info = f"Можно забрать с работы через {int(hour_w)} ч. {int(minutes_w)} м.\n"
            send_working = False
            pick_working = False

        info = feeding_info + "\n" + working_info

        await m.answer(
            info,
            keyboard=MK.hedgehog_info(feeding, send_working, pick_working)
        )


class Transfer:

    async def give_the_item(m: Message, hedgehog:  Hedgehog, quantity: str, user: str):

        user_id = int(re.findall(r"[0-9]+", user)[0])
        if user_id == m.from_id:
            return "Вы не можете передать яблочки самому себе."

        user_hedgehog = DB.hedgehog.get(user_id, m.peer_id)

        quantity = int(quantity)

        if hedgehog is None:
            return "У вас нет ёжика."
        if user_hedgehog is None:
            return "У данного пользователя нет ёжика в этой беседе."
        if hedgehog.apples < quantity:
            return "У вас недостаточно яблочек."

        hedgehog.apples -= quantity
        hedgehog.save()
        user_hedgehog.apples += quantity
        user_hedgehog.save()
        return f"Яблочек передано - {quantity}"


class Work:

    async def send(hedgehog: Hedgehog):

        if hedgehog is None:
            return "У вас ещё нет ёжика."
        if hedgehog.condition == "мёртв":
            return "Ваш ёжик мёртв :("

        work_time = hedgehog.working_time
        now_time = datetime.now()

        if hedgehog.at_work:
            if work_time < now_time:
                return "сначала заберите ёжика с работы."
            return "Ваш ёжик уже на работе"

        if work_time is None or work_time < now_time:
            hedgehog.at_work = True
            hedgehog.working_time = now_time + timedelta(hours=3)
            hedgehog.save()

            return "Ваш ёжик отправился на работу, не забудьте забрать его через 3 часа."

    async def pick(m: Message, hedgehog: Hedgehog):

        if hedgehog is None:
            return "У вас ещё нет ёжика."
        if hedgehog.condition == "мёртв":
            return "Ваш ёжик мёртв :("
        if not hedgehog.at_work:
            "Ваш ёжик сейчас не на работе."

        now_time = datetime.now()

        if hedgehog.working_time < now_time:

            add_apples = random.randrange(40, 80, 5)

            hedgehog.at_work = False
            hedgehog.apples += add_apples
            hedgehog.save()

            await m.answer(
                "Вы забрали вашего ёжика с работы.\n\n"
                f"+{add_apples} яблочек."
            )
        else:
            return "Ваш ёжик ещё не закончил работу."
