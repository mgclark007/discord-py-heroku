import discord
from discord.ext import commands

from discord.ext.commands.core import command
from discord.utils import get

class Economy(commands.Cog):
	def __init__(self,client):
		self.client = client


	@commands.Cog.listener()
	async def on_ready(self):
		print("here comes the bot")
		await self.client.pg_con.execute("CREATE TABLE IF NOT EXISTS economy (userid BIGINT , money BIGINT)")
		await self.client.pg_con.execute("ALTER TABLE economy ADD COLUMN IF NOT EXISTS userid BIGINT NOT NULL")
		await self.client.pg_con.execute("ALTER TABLE economy ADD COLUMN IF NOT EXISTS money BIGINT")

	async def add(self,id,amount=0):
		bal = await self.client.pg_con.fetchrow("SELECT money FROM economy WHERE userid = $1",id)
		await self.client.pg_con.execute("UPDATE economy SET money = $1 WHERE userid = $2", amount+bal[0], id)

	# check user for existing. call command at start of every function, make sure every user is subject to this command
	async def check(self,id):
		user = await self.client.pg_con.fetchrow("SELECT * FROM economy WHERE userid = $1",id)
		if not user:
			await self.client.pg_con.execute("INSERT INTO economy (userid, money) VALUES ($1, $2) ", id, 2000)

	async def balance(self,id):
		bal = await self.client.pg_con.fetchrow("SELECT money FROM economy WHERE userid = $1",id)
		return bal[0]

	async def top(self):
		tops = await self.client.pg_con.fetchrow("SELECT * FROM economy ORDER BY money DESC NULLS LAST")
		return tops

	@commands.command()
	async def trial(self,ctx):
		id = ctx.author.id
		await self.check(id)
		await self.add(id,25)
		tops = await self.top()
		await ctx.send(self.balance(id))

def setup(client):
	client.add_cog(Economy(client))
