# bot.py
import os
import user as u
import users as j

import discord
from discord.utils import get
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

j.loadJSON()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    print(message)
    print(message.author)
    print(message.content)

    if (message.content == "hello son" and message.author.name == "poe0"):
        response = 'hello dad'
        await message.channel.send(response)
    elif (message.content == ".list" and j.isTrusted(message.author.name)):
        response = j.listUsers()
        await message.channel.send(response)
    elif (message.content == ".reload" and j.isTrusted(message.author.name)):
        response = "Reloading database"
        j.reloadJSON()
        await message.channel.send(response)
    elif (message.content == ".help"):
        response = "```.help - This message\n.announce to @everyone (Admin only)\n.emoji - Set your car emoji\n.list - List known server members```"
        await message.channel.send(response)
    elif (message.content.startswith(".announce") and j.isTrusted(message.author.name)):
        response = "@everyone " + message.content[9:]
        await message.channel.send(response)
    elif ((message.content.startswith(".add")) and message.author.name == "poe0"):
        list = message.content.split()
        if (len(list) == 4):
            response = "Adding " + list[1] + list[2] + list[3]
        else:
            response = "Usage: `username` `emoji` `trusted`"
        await message.channel.send(response)
    elif ((message.content.startswith(".emoji"))):
        list = message.content.split()
        if (len(list) == 2):
            response = "Setting your emoji to " + list[1]
            j.setEmoji(message.author.name, list[1])
        else:
            user = j.getUser(message.author.name)
            if (user != None):
                response = "Your emoji: " + user.emoji
            else:
                response = "You don't have an emoji! " "Set one using `.emoji <your_emoji>`"
        await message.channel.send(response)
    

@client.event
async def on_raw_reaction_add(payload):
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = await client.fetch_user(payload.user_id)
    print(payload.emoji)
    print(payload.user_id)
    print(user.name)
    if (str(payload.emoji) == "👍"):
        user = j.getUser(user.name)
        if (user != None):
            await message.add_reaction(user.emoji)

@client.event
async def on_raw_reaction_remove(payload):
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = await client.fetch_user(payload.user_id)
    me = await client.fetch_user(794329518604812338)
    print(payload.emoji)
    print(payload.user_id)
    print(user.name)
    if (str(payload.emoji) == "👍"):
        user = j.getUser(user.name)
        if (user != None):
            await message.remove_reaction(user.emoji, me)

client.run(TOKEN)

