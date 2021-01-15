from discord.ext import commands

class AssignRolesCog(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.command(name="assign")
	async def assign_role(self, ctx: commands.Context):
		""" A simple command that assigns roles """

def setup(bot: commands.Bot):
	bot.add_cog(AssignRolesCog(bot))
