# bot.py
import os
import requests
import discord
import json
import random

from dotenv import load_dotenv
from operator import itemgetter

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
KEY = os.getenv('TARKOV_KEY')

headers = {'x-api-key': KEY}
client = discord.Client()
insult = ["idiot", "dummy", "stupid", "shithead", "Tyler"]

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "!price" in message.content:
        list = message.content.split()
        mItem = itemgetter(1)(list)
        try:
            url = "https://tarkov-market.com/api/v1/item?q={}".format(mItem)
            r = requests.get(url, headers=headers)
            json_data = json.loads(r.text)

            for item in json_data:
                price = item['avg24hPrice']
                name = item['name']
                img = item['img']
                link = item['link']
                mes = "The price for {} is {:,} rubles".format(name,price)
                await message.channel.send(mes)

        except:
            rInsult = random.choice(insult)
            mes = "Item {} not found you {}".format(mItem, rInsult)
            await message.channel.send(mes)

client.run(TOKEN)
