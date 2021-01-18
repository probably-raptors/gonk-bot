from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
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
	@has_permissions(manage_roles=True)
	async def assign_role(self, ctx: commands.Context):
		"""A command to manually assign roles to users"""
		tokens = ctx.message.content.split().pop()
		member = tokens[0]
		roles = tokens[1:]
		await member.add_roles(roles)

	async def assign_role_err(self, ctx, error):
		if isinstance(error, MissingPermissions):
			await ctx.send("You do not have permission to use this command")


def setup(bot: commands.Bot):
	bot.add_cog(RolesCog(bot))
