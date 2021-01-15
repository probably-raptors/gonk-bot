from discord.ext import commands
import random


class PingCog(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.command(name="ping")
	async def ping(self, ctx: commands.Context):
		""" A simple command that responds to a ping """

		with open("modules/ping/responses.txt") as responses:
			await ctx.send(random.choice(responses.readlines()))


def setup(bot: commands.Bot):
	bot.add_cog(PingCog(bot))