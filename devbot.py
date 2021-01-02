# bot.py
import os
import requests
import discord
import json
import random
import threading
import time

from dotenv import load_dotenv
from operator import itemgetter

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
KEY = os.getenv('TARKOV_KEY')

headers = {'x-api-key': KEY}
client = discord.Client()
insult = ["idiot", "dummy", "stupid", "shithead", "Tyler"]
emoji = ["<:notlikethis:715327078031163464>", "<:monkahmm:715327077687230526>", "<:monkaw:715327077670322186>", "<a:bttv_111:715328133686886420>"]

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content
    case = msg.lower()
    if "!price" in case:
        str1 = case.replace("!price ","")
        if " " in str1:
            mItem = str1.replace(" ","+")
        else:
            mItem = str1
        #mItem = itemgetter(1)(list)
        print(mItem)
        url = "https://tarkov-market.com/api/v1/item?q={}".format(mItem)
        r = requests.get(url, headers=headers)
        json_data = json.loads(r.text)
        if len(r.text) < 4:
            rInsult = random.choice(insult)
            rEmoji = random.choice(emoji)
            mes = "Item {} not found you {} {}".format(mItem, rInsult, rEmoji)
            send = await message.channel.send(mes)
            time.sleep(5)
            await message.delete()
            await send.delete()
            await message.delete()
        else:
            for item in json_data:
                title = item['shortName']
                price = item['avg24hPrice']
                name = item['name']
                img = item['img']
                link = item['link']
                embed = discord.Embed(title="{}".format(title), description="{}".format(name), color=0x00ff00)
                embed.add_field(name="Link", value="{}".format(link), inline=False)
                embed.add_field(name="Price", value="{:,}".format(price), inline=False)
                embed.set_image(url="{}".format(img))
                send = await message.channel.send(embed=embed)
                time.sleep(15)
                await send.delete()
            await message.delete()

    elif case == "!tarkohelp":
        mes = "Please include the command you would like help with, example: !tarkohelp !price  --   You can get a list of commands with !tarkocommands"
        await message.channel.send(mes)

    elif "!tarkocommands" in case:
        mes = "price, owen, secret"
        await message.channel.send(mes)

    elif "!tarkohelp price" in case:
        mes = "try !price 'item name' to get the price of an item"
        await message.channel.send(mes)
        
    elif "!tarkohelp owen" in case:
        mes = "try !owen to see how evan is sassy with owen"
        await message.channel.send(mes)
        
    elif "!tarkohelp secret" in case:
        mes = "try !secret if you aint a bitch"
        await message.channel.send(mes)

    elif "!owen" in case:
        mes = "owen its one command please stop it please"
        await message.channel.send(mes)

    elif "!secret" in case:
        mes = "||if you clicked this you a bitch||"
        await message.channel.send(mes)

    elif "!glen" in case:
        mes = "https://clips.twitch.tv/ImpossibleInquisitiveSpindleRickroll"
        await message.channel.send(mes)

    elif "!shutup" in case:
        mes = "Shutup Tyler"
        await message.channel.send(mes)

client.run(TOKEN)
