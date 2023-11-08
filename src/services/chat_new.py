from vkbottle import VKAPIError
from vkbottle.bot import Message

from db.func import DB
from components.keyboards import Mykeyboard as MK


async def invite(m: Message):

    user_id = m.action.member_id or m.from_id
    if user_id == -m.group_id:

        DB.chat.add(m.peer_id)

        await m.answer(
            "Привет!\n"
            "Для работы мне необходимы права администратора.",
            keyboard=MK.start_keyboard
        )
    elif user_id > 0:

        users_info = (await m.ctx_api.users.get(user_id))[0]
        first_name = users_info.first_name
        last_name = users_info.last_name

        await m.answer(
            f"Привет {first_name} {last_name}"
        )


async def admin_check(m: Message):

    try:
        _ = await m.ctx_api.messages.get_conversation_members(m.peer_id)
    except VKAPIError[917]:
        await m.answer("права администратора не получены(")
    else:
        await m.answer("спасибо, я готов к работе")
