from telethon import TelegramClient
import json
import logging
import time

try:
    config = json.loads(open("config.json").read())
except:
    print("config.json was not found. Please create it in the root folder.")

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# Basics
API_ID = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"
API_TOKEN = config['api_token']
BOT_TOKEN = config['bot_token']

bot = TelegramClient("UA_airalertbot", API_ID, API_HASH).start(bot_token=BOT_TOKEN) 