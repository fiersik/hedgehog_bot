from datetime import datetime
import random

from db.func import DB
from config import bot_api, server_api, group_id, hedgehog_albom_id


class News:

    async def sending_hedgehogs():

        time = datetime.now()
        if time.hour % 2 and not time.minute:

            pictures = await server_api.photos.get(
                group_id,
                hedgehog_albom_id
            )
            picture = random.choice(pictures.items)
            attachment = f"photo{picture.owner_id}_{picture.id}"

            for ids in DB.chat.get_subscribers_id():

                await bot_api.messages.send(
                    peer_ids=ids,
                    message="""
        К вам забежал маленький ёжик.

        Напиши 'Взять ёжика', чтобы подобрать его к себе""",
                    attachment=attachment,
                    random_id=0
                )
            DB.chat.new_hedgehog(attachment)


class Statistics:

    async def hunger():

        for hedgehog in DB.hedgehog.get_all():
            if hedgehog.condition == "отличное":

                hedgehog.hunger -= 1
                hedgehog.save()

                if not hedgehog.hunger:
                    hedgehog.condition = "голоден"
                    hedgehog.death_time = datetime.now()
                    hedgehog.save()

                    chat_id = hedgehog.chat.peer_id
                    owner = hedgehog.owner.from_id

                    user_info = (await bot_api.users.get(owner))[0]
                    first_name = user_info.first_name
                    last_name = user_info.last_name
                    mention = f"[id{owner}|{first_name} {last_name}]"

                    message = f"О нет, {mention}, твой ёжик голоден!"

                    await bot_api.messages.send(
                        peer_id=chat_id,
                        message=message,
                        random_id=0
                    )

    async def death():

        for hedgehog in DB.hedgehog.get_all():
            if (hedgehog.death_time is not None
                    and hedgehog.death_time <= datetime.now()
                    and hedgehog.condition != "мёртв"):

                hedgehog.condition = "мёртв"
                hedgehog.save()

                chat_id = hedgehog.chat.peer_id
                owner = hedgehog.owner.from_id

                user_info = (await bot_api.users.get(owner))[0]
                first_name = user_info.first_name
                last_name = user_info.last_name
                mention = f"[id{owner}|{first_name} {last_name}]"

                message = f"О нет, {mention}, твой ёжик умерает от голода."

                await bot_api.messages.send(
                    peer_id=chat_id,
                    message=message,
                    random_id=0
                )