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
        msg = await ctx.send(embed=poll.embed, delete_after=int(poll.duration))
        for react in poll.reacts.values():
            await msg.add_reaction(react)

        # this is the id of the embed message, NOT the command-triggering message
        self.polls[msg.id] = poll
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.message_id in self.polls.keys() and not payload.member.bot:
            poll = self.polls.get(payload.message_id, None)
            if poll is not None:
                msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
                await poll.vote(payload.member, payload.emoji, msg)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        user = await self.bot.fetch_user(payload.user_id)
        if user.bot:
            return

        if payload.message_id in self.polls.keys():
            poll = self.polls.get(payload.message_id)
            member = await self.bot.fetch_user(payload.user_id)
            poll.unvote(member)


def setup(bot: commands.Bot):
    bot.add_cog(PollCog(bot))
