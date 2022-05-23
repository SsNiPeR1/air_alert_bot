from .. import API_TOKEN, bot
from telethon import events, Button
import requests

@bot.on(events.NewMessage(incoming=True, pattern="/start"))
async def start(event):
    await event.reply("Hello!")

@bot.on(events.NewMessage(incoming=True, pattern="/triv"))
async def triv(event):
    params = {"X-API-Key": API_TOKEN}
    x = requests.get("https://alerts.com.ua/api/states", headers=params)
    await event.reply(x.text)