#==============================
import os
from vkbottle import API
#==============================

BOT_TOKEN = os.environ.get("HEDGEHOG_BOT_TOKEN")
SERVER_TOKEN = os.environ.get("HEDGEHOG_SERVER_TOKEN")
#==============================

bot_api = API(BOT_TOKEN)
server_api = API(SERVER_TOKEN)
#==============================