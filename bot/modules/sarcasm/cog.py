from discord.ext import commands
import discord
import random


class SarcasmCog(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	def sarcastify(self, msg: str):
		new_msg = ""
		cap = False
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
		
		# REQUIRED, otherwise the bot will also trigger this cog
		if msg.author.bot:
			return

		# change the range to (1, 1) for testing / trolling
		r = random.randint(1, 100)
		if r == 1:
			new_msg = self.sarcastify(msg.content)
			await msg.channel.send(new_msg)


def setup(bot: commands.Bot):
	bot.add_cog(SarcasmCog(bot))