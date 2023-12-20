from vkbottle.bot import BotLabeler

from .basic import basic
from .chat_admin import admin
from .new_chat import new_chat

chat_labelers: list[BotLabeler] = [basic, admin, new_chat]
