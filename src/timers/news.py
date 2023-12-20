from services.timers import News
from vkbottle import LoopWrapper

lw = LoopWrapper()


@lw.interval(minutes=1)
async def news():
    """рассылка ёжиков по чатам"""
    await News.sending_hedgehogs()


@lw.interval(seconds=5)
async def test():
    print("ОГО, ОНО РАБОТАЕТ")
