from vkbottle import LoopWrapper

from components.tools import load_tasks
from .news import lw as news
from .indicators import lw as indicators


lw = LoopWrapper()

load_tasks(
    lw,
    *news.tasks,
    *indicators.tasks
)
