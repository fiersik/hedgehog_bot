from vkbottle import LoopWrapper

from services.timers import News, Statistics

lw = LoopWrapper()


@lw.interval(minutes=1)
async def news():
    """рассылка ёжиков по чатам"""
    await News.sending_hedgehogs()


@lw.interval(hours=8)
async def hunger():
    """голод ёжиков"""
    await Statistics.hunger()


@lw.interval(minutes=1)
async def of_death():
    """смерти голодных ёжиков"""
    await Statistics.death()
