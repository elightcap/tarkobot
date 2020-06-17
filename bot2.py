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
insult = ["idiot", "dummy", "stupid", "shithead"]

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
                title = item['shortName']
                price = item['avg24hPrice']
                name = item['name']
                img = item['img']
                link = item['link']
                embed = discord.Embed(title="{}".format(title), description="{}".format(name), color=0x00ff00)
                embed.add_field(name="Link", value="{}".format(link), inline=False)
                embed.add_field(name="Price", value="{}".format(price), inline=False)
                embed.set_image(url="{}".format(img))
                await message.channel.send(embed=embed)

        except:
            rInsult = random.choice(insult)
            mes = "Item {} not found you {}".format(mItem, rInsult)
            await message.channel.send(mes)

    elif "!tarkohelp" in message.content:
        mes = "try !price 'item name' to get the price of an item"
        await message.channel.send(mes)

    elif "!owen" in message.content:
        mes = "owen its one command please stop it please"
        await message.channel.send(mes)

client.run(TOKEN)
