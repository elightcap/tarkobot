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
emoji = ["<:notlikethis:715327078031163464>", "<:monkahmm:715327077687230526>", "<:monkaw:715327077670322186>", "<a:bttv_111:715328133686886420>"]

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "!price" in message.content:
        list = message.content.split()
        mItem = itemgetter(1)(list)
        url = "https://tarkov-market.com/api/v1/item?q={}".format(mItem)
        r = requests.get(url, headers=headers)
        json_data = json.loads(r.text)
        if len(r.text) < 4:
            rInsult = random.choice(insult)
            rEmoji = random.choice(emoji)
            mes = "Item {} not found you {} {}".format(mItem, rInsult, rEmoji)
            await message.channel.send(mes)
        else:
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

    elif message.content == "!tarkohelp":
        mes = "Please include the command you would like help with, example: !tarkohelp !price  --   You can get a list of commands with !tarkocommands"
        await message.channel.send(mes)

    elif "!tarkocommands" in message.content:
        mes = "price, owen, secret"
        await message.channel.send(mes)

    elif "!tarkohelp price" in message.content:
        mes = "try !price 'item name' to get the price of an item"
        await message.channel.send(mes)
        
    elif "!tarkohelp owen" in message.content:
        mes = "try !owen to see how evan is sassy with owen"
        await message.channel.send(mes)
        
    elif "!tarkohelp secret" in message.content:
        mes = "try !secret if you aint a bitch"
        await message.channel.send(mes)

    elif "!owen" in message.content:
        mes = "owen its one command please stop it please"
        await message.channel.send(mes)

    elif "!secret" in message.content:
        mes = "||if you clicked this you a bitch||"
        await message.channel.send(mes)

client.run(TOKEN)
