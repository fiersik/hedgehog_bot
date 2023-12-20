# ==============================
from vkbottle.bot import Bot

from db.models import db, Chat, User, Hedgehog
from config import bot_api
from handlers.private_message import private_labelers
from handlers.chat_message import chat_labelers
from timers import lw
from components.middleware import all_middleware
# ==============================

bot = Bot(
    api=bot_api,
    loop_wrapper=lw
)

for labeler in chat_labelers:
    bot.labeler.load(labeler)
for labeler in private_labelers:
    bot.labeler.load(labeler)

for middleware in all_middleware:
    bot.labeler.message_view.register_middleware(middleware)

if __name__ == "__main__":
    db.create_tables([Chat, User, Hedgehog])
    bot.run_forever()
