from discord.ext.commands.core import has_permissions
from discord.ext import commands
from .poll import Poll
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
        msg = await ctx.send(embed=poll.embed, delete_after=poll.duration)
        for i, opt in enumerate(poll.options):
            await msg.add_reaction(poll.reacts[i])

        self.polls[ctx.message.id] = poll
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, ctx, payload: discord.RawReactionActionEvent):
        if payload.message_id in self.polls and not payload.member.bot:
            await self.vote(ctx.message, payload.member, payload.emoji)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, ctx, payload: discord.RawReactionActionEvent):
        if ctx.message.id in self.polls.keys:
            self.unvote(self, payload)


def setup(bot: commands.Bot):
    bot.add_cog(PollCog(bot))
