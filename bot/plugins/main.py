from .. import API_TOKEN, bot
from telethon import events
import requests
import json

allowed_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
regions = '''1 - Вінницька область
2 - Волинська область
3 - Дніпропетровська область
4 - Донецька область
5 - Житомирська область
6 - Закарпатська область
7 - Запорізька область
8 - Івано-Франківська область
9 - Київська область
10 - Кіровоградська область
11 - Луганська область
12 - Львівська область
13 - Миколаївська область
14 - Одеська область
15 - Полтавська область
16 - Рівненська область
17 - Сумська область
18 - Тернопільська область
19 - Харківська область
20 - Херсонська область
21 - Хмельницька область
22 - Черкаська область
23 - Чернівецька область
24 - Чернігівська область
25 - Київ
'''

def printanswer(id, name, is_alert):
    if is_alert:
        alert = "❌ Тривога!"
    if not is_alert:
        alert = "✅ Немає тривоги!"
    return f'''{name}:
    Статус: {alert}'''

def parse_args(message):
    return message.split()[1:]

@bot.on(events.NewMessage(incoming=True, pattern="/start"))
async def start(event):
    await event.reply("Привіт! Я бот для отримання даних про повітряні тривоги в Україні!\nВикористовуй /triv <id регіона (не обов'язково, можно отримати через /ids)>")

@bot.on(events.NewMessage(incoming=True, pattern="/triv"))
async def triv(event):
    headers = {"X-API-Key": API_TOKEN}
    args = parse_args(event.text)
    x = requests.get("https://alerts.com.ua/api/states", headers=headers)
    try:
        if not args[0]:
            pass # just exit if no argument supplied
        
        if int(args[0]) in allowed_ids:
            region = int(args[0])
        else:
            await event.reply("Невірний ID регіону!") # If cannot convert argument to int, exit
            return

        await event.reply(f"Giving results on {args[0]}")
        x = requests.get(f"https://alerts.com.ua/api/states/{region}", headers=headers)

    except:
        pass
    try:
        if args[0]:    
            final = json.loads(x.text)
            id = final['state']['id']
            name = final['state']['name']
            is_alert = final['state']['alert']
            reply = printanswer(id=id, name=name, is_alert=is_alert)
            await event.reply(reply)
        else:
            await event.reply(requests.get(f"https://alerts.com.ua/api/states/{region}", headers=headers).text)
    except:
        reply = ""
        for region in range(1, 25):
            req = requests.get(f"https://alerts.com.ua/api/states/{region}", headers=headers)
            parsed = json.loads(req.text)

            id = parsed['state']['id']
            name = parsed['state']['name']
            is_alert = parsed['state']['alert']

            reply += printanswer(id=id, name=name, is_alert=is_alert) + "\n"

        await event.reply(reply)
@bot.on(events.NewMessage(incoming=True, pattern="/ids"))
async def list_regions(event):
    await event.reply(regions)

@bot.on(events.InlineQuery)
async def no_pattern(event):
    builder = event.builder
    
    headers = {"X-API-Key": API_TOKEN}
    x = requests.get("https://alerts.com.ua/api/states", headers=headers)
    reply = ""

    for region in range(1, 25):
        req = requests.get(f"https://alerts.com.ua/api/states/{region}", headers=headers)
        parsed = json.loads(req.text)

        id = parsed['state']['id']
        name = parsed['state']['name']
        is_alert = parsed['state']['alert']

        reply += printanswer(id=id, name=name, is_alert=is_alert) + "\n"

    await event.answer([builder.article("Всі регіони", text=reply)])