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

		members = ctx.message.mentions
		roles = ctx.message.content.split()
		roles = roles[1:-2]
		for member in members:
			for r in roles:
				try:
					role = discord.utils.get(member.server.roles, name=r)
				except:
					await ctx.send("That role does not exist")
					continue
				await member.add_roles(role)
				print(f"Added role: { r } to Member: { member }")

	async def assign_role_err(self, ctx, error):
		if isinstance(error, MissingPermissions):
			await ctx.send("You do not have permission to use this command")


def setup(bot: commands.Bot):
	bot.add_cog(RolesCog(bot))