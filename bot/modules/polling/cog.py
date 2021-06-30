from bot.modules.polling.poll import Poll
from discord.ext import commands
import discord


class PollingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.polls = {}

    @commands.command(name="poll", pass_context=True)
    async def create_poll(self, ctx: commands.Context):
        """A command for users to create polls for other users to vote on"""
        """.poll Title, Duration, [Option1, Option2, ... Option9]"""

        poll = Poll(ctx.message)
        self.msg = await ctx.send(embed=poll.embed, delete_after=poll.duration)
        self.polls[self.msg] = poll
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_raw_reaction_add(
        self, reaction: discord.Reaction, member: discord.Member
    ):
        if reaction.message in self.polls and not member.bot:
            await self.polls[reaction.message].vote(reaction, member)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(
        self, reaction: discord.Reaction, member: discord.Member
    ):
        if reaction.message in self.polls and not member.bot:
            await self.polls[reaction.message].unvote(reaction, member)


def setup(bot: commands.Bot):
    bot.add_cog(PollingCog(bot))
