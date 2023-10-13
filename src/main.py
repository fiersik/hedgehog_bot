#==============================
import asyncio
from vkbottle.bot import Bot

from config import bot_api
from handlers import labelers
#==============================

bot = Bot(
    api=bot_api
)

for labeler in labelers:
    bot.labeler.load(labeler)

if __name__ == "__main__":
    asyncio.run(bot.run_polling())