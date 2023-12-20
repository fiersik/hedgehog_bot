# ==============================
from vkbottle.bot import Message, BotLabeler

from services import chat_new
# ==============================

new_chat = BotLabeler()
new_chat.vbml_ignore_case = True
# ==============================


@new_chat.chat_message(
    action=[
        "chat_invite_user",
        "chat_invite_user_by_link"
    ])
async def invite_handler(m: Message):

    await chat_new.invite(m)


@new_chat.chat_message(payload={"admin": "check"})
async def admin_check_handler(m: Message):

    await chat_new.admin_check(m)
