from datetime import datetime
import random

from vkbottle import LoopWrapper

from config import bot_api, server_api, DB

lw = LoopWrapper()


@lw.interval(minutes=1)
async def news():

    time = datetime.now()
    if not time.hour % 2 and not time.minute:

        pictures = await server_api.photos.get(
            -219000856,
            299084525,
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
        DB.chat.new_hedgehog(picture)
