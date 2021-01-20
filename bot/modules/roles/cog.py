from .functions import get_tokens, update_roles
from discord.ext.commands import has_permissions
from discord.ext import commands
import discord


class RolesCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, ctx, member: discord.Member):
        """An event listener to assign the default role to new users"""
        print(f"{ member.name } has entered the nest!")
        await member.add_roles(ctx.guild.roles, name="Kit")

    @commands.command(name="add", pass_context=True)
    @has_permissions(manage_roles=True)
    async def add_roles(self, ctx: commands.Context):
        """A command to manually assign roles to members"""
        """.add [Member1, Member2, ...] [Role1, Role2, ...]"""
        print("add_roles was called")
        tokens = get_tokens(ctx.message.content)
        await update_roles(ctx, tokens, flag="a")

    @commands.command(name="remove", pass_context=True)
    @has_permissions(manage_roles=True)
    async def remove_roles(self, ctx):
        """A command to manually remove roles from members"""
        """.remove [Member1, Member2, ...] [Role1, Role2, ...]"""

        tokens = get_tokens(ctx.message.content)
        await update_roles(ctx, tokens, flag="r")


def setup(bot: commands.Bot):
    bot.add_cog(RolesCog(bot))
