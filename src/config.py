# ==============================
import os

from vkbottle import API

from db import DB  # noqa: F401
# ==============================

BOT_TOKEN = os.environ.get("HEDGEHOG_BOT_TOKEN")
SERVER_TOKEN = os.environ.get("HEDGEHOG_SERVER_TOKEN")
# ==============================

group_id = -219000856
hedgehog_albom_id = 300010322
# ==============================

bot_api = API(BOT_TOKEN)
server_api = API(SERVER_TOKEN)
# ==============================
