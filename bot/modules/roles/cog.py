from discord.ext import commands
import config
import discord


class RolesCog(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_member_join(self, member: discord.Member):
		"""Assigns the default role to new users"""
		print(f"{ member.name } has entered the nest!")
		await member.add_roles(config.default_role)

	@commands.command(name="assign")
	async def assign_role(self, ctx: commands.Context):
		"""A command to manually assign roles to users"""
		if ctx.author not in config.admin_roles:
			await ctx.send("Only admins may use this command")
		else:
			tokens = ctx.message.content.split().pop()
			member = tokens[0]
			roles = tokens[1:]

			for role in roles:
				await member.add_roles(role)


def setup(bot: commands.Bot):
	bot.add_cog(RolesCog(bot))
