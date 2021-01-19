from discord.ext.commands import has_permissions, MissingPermissions
from .get_tokens import get_tokens
from discord.ext import commands
from discord.utils import get
import discord


class RolesCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, ctx: commands.Context, member: discord.Member):
        """Assigns the default role to new users"""
        print(f"{ member.name } has entered the nest!")
        await member.add_roles(ctx.guild.roles, name="Kit")

    @commands.command(name="add")
    @has_permissions(manage_roles=True)
    async def add_role(self, ctx: commands.Context):
        """A command to manually assign roles to members"""
        """./add [Member1, Member2, ...] [Roles1, Role2, ...]"""

        tokens = await get_tokens(ctx.message.content)

        for member in tokens["members"]:
            m = discord.utils.find(lambda m: m.name == member, ctx.guild.members)
            if m is not None:
                for role in tokens["roles"]:
                    r = discord.utils.find(lambda r: r.name == role, ctx.guild.roles)
                    if r is not None:
                        await m.add_roles(r)
                        # TODO: Raise exceptions for both ifs

    @commands.command(name="remove")
    @has_permissions(manage_roles=True)
    async def remove_role(self, ctx: commands.Context):
        """A command to manually remove roles from members"""
        """./remove [Members] [Roles]"""

        tokens = get_tokens(ctx.message.content)

        for member in tokens["members"]:
            m = discord.utils.find(lambda m: m.name == member, ctx.guild.members)
            if m is not None:
                for role in tokens["roles"]:
                    r = discord.utils.find(lambda r: r.name == role, ctx.guild.roles)
                    if r is not None:
                        await m.remove_roles(r)
                        # TODO: Raise exceptions for both ifs

    async def role_err(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You do not have permission to use this command")


def setup(bot: commands.Bot):
    bot.add_cog(RolesCog(bot))
