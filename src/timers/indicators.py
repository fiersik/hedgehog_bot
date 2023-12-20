from services.timers import Indicators
from vkbottle import LoopWrapper

lw = LoopWrapper()


@lw.interval(hours=8)
async def hunger():
    """голод ёжиков"""
    await Indicators.hunger()


@lw.interval(minutes=1)
async def of_death():
    """смерти голодных ёжиков"""
    await Indicators.death()
