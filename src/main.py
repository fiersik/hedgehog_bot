# ==============================
from vkbottle.bot import Bot

from config import bot_api
from handlers import labelers, lw
# ==============================

bot = Bot(
    api=bot_api,
    loop_wrapper=lw
)

for labeler in labelers:
    bot.labeler.load(labeler)

if __name__ == "__main__":
    bot.run_forever()
