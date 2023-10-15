from .timers import lw

from .new_chat import new_chat
from .chat_admin import admin

from vkbottle.bot import BotLabeler

labelers: list[BotLabeler] = [new_chat, admin]

__all__ = (labelers, lw)
