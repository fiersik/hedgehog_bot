# ==============================
from vkbottle.bot import Bot

from config import bot_api
from handlers import labelers, lw
from components.middleware import all_middleware
# ==============================

bot = Bot(
    api=bot_api,
    loop_wrapper=lw
)

for labeler in labelers:
    bot.labeler.load(labeler)

for middleware in all_middleware:
    bot.labeler.message_view.register_middleware(middleware)

if __name__ == "__main__":
    bot.run_forever()
