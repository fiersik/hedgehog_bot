from vkbottle.bot import BotLabeler

from .timers import lw

from .new_chat import new_chat
from .basic import basic
from .chat_admin import admin
from .creator import creator

labelers: list[BotLabeler] = [new_chat, basic, admin, creator]

__all__ = (labelers, lw)
