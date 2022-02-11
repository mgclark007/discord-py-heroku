import os
from discord.ext import commands

# database
import sqlite3

bot = commands.Bot(command_prefix="!")
TOKEN = os.getenv("DISCORD_TOKEN")

# database read/write
async def writesingle(ctx, field, data):
    # initialize
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()

    # find field
    cursor.execute(f"SELECT {field} FROM main WHERE guild_id = {ctx.guild.id}")
    result = cursor.fetchone()

    # Prepare variables and sql
    if result is None:
        sql = (f"INSERT INTO main(guild_id, {field}) VALUES (?,?)")
        val = (ctx.guild.id, data)
        await ctx.send(f"Field {field} has been set to {data}")
    elif result is not None:
        sql = (f"UPDATE main SET {field} = ? WHERE guild_id = ?")
        val = (data, ctx.guild.id)
        await ctx.send(f"Field {field} has been updated to {data}")

    # execute command
    cursor.execute(sql, val)

    # save
    db.commit()

    # close
    cursor.close()
    db.close()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}({bot.user.id})")

@bot.command(name='setsword')
async def dosomething(ctx, data):
    await ctx.send("command received")
    await writesingle("equipped_sword", data)

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

if __name__ == "__main__":
    bot.run(TOKEN)

