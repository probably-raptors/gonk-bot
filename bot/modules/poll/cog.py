from discord.ext.commands.core import has_permissions
from .poll import Poll
from discord.ext import commands
import discord


class PollCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.polls = {}

    @commands.command(name="poll", pass_context=True)
    @has_permissions(manage_messages=True)
    async def create_poll(self, ctx: commands.Context):
        """A command for users to create polls for other users to vote on"""
        """.poll Title Duration Option1 ... Option9"""
        poll = Poll(ctx.message)
        await ctx.send(embed=poll.embed)
        self.polls[ctx.message.id] = poll
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, ctx, payload: discord.RawReactionActionEvent):
        if payload.message_id in self.polls and not payload.member.bot:
            await self.vote(ctx.message, payload.member, payload.emoji)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.member in self.voters.keys:
            self.voters.pop(payload.member, None)


def setup(bot: commands.Bot):
    bot.add_cog(PollCog(bot))
