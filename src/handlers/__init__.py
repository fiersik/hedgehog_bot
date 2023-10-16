from .timers import lw

from .new_chat import new_chat
from .basic import basic
from .chat_admin import admin

from vkbottle.bot import BotLabeler

labelers: list[BotLabeler] = [new_chat, basic, admin]

__all__ = (labelers, lw)
