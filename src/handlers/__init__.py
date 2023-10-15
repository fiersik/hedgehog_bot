from .timers import lw

from .new_chat import new_chat

from vkbottle.bot import BotLabeler

labelers: list[BotLabeler] = [new_chat]

__all__ = (labelers, lw)
