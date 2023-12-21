from services.timers import News
from vkbottle import LoopWrapper

lw = LoopWrapper()


@lw.interval(minutes=1)
async def news():
    """рассылка ёжиков по чатам"""
    await News.sending_hedgehogs()
