import os
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!")
TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}({bot.user.id})")

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

if __name__ == "__main__":
    bot.run(TOKEN)


@client.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == 'm':
        response = 'gooo'
        await message.channel.send(response)