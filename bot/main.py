import os
from discord.ext import commands

import random

import asyncio
import asyncpg
from asyncpg.pool import create_pool

client = commands.Bot(command_prefix="!")
TOKEN = os.getenv("DISCORD_TOKEN")

DATABASE_URL = os.environ['DATABASE_URL']


async def create_db_pool():
    client.pg_con = await asyncpg.create_pool(DATABASE_URL)
    #client.pg_con = await asyncpg.create_pool(database="economy",user="postgres",password="ass_app")


@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}({client.user.id})")

@client.command("setsword")
async def dosomething(ctx, data):
    await ctx.send("command received")
    #await writesingle(ctx, "equipped_sword", data)

# @client.command()
# async def ping(ctx):
#     await ctx.send("pong")



# april fools code
emotes = ["<:matthew:688543994732740613>", "<:kimkim13:892250398746877952>", "<:kimkim69:930313263621754960>", "<:jeangasm:872378627348631613>", "<:chris:925276627246657596>", "<:robert:930312594059845703>", "<:justindamn:876740972048953364>", "<:dead:871578603417137182>"]

@client.event
async def on_message(message):
    if "$" in message.content:
        await message.channel.send(random.choice(emotes))

if __name__ == "__main__":
    for files in os.listdir('./cogs'):
        if files.endswith('.py'):
            client.load_extension(f"cogs.{files[:-3]}")


    client.loop.run_until_complete(create_db_pool())
    client.run(TOKEN)

