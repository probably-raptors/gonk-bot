from discord.ext import commands
import discord
import random


class SarcasmCog(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	def sarcastify(self, msg: discord.Message):
		new_msg = ""
		cap = True
		for c in msg:
			if cap:
				new_msg += c.upper()
			else:
				new_msg += c.lower()
			if c != " ":
				cap = not cap
		return new_msg

	@commands.Cog.listener()
	async def on_message(self, msg: discord.Message):
		r = random.randint(1, 100)
		if r == 1:
			new_msg = self.sarcastify(msg)
			await msg.send(new_msg)