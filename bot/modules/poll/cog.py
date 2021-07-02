from discord.ext.commands.core import has_permissions
from bot.modules.poll.poll import Poll
from discord.ext import commands
from discord import client
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
    async def on_raw_reaction_add(self, payload: discord.onRawReactionEvent):
        if payload.user_id not in self.voters:
            self.voters[payload.user_id] = payload.emoji.name
        else:
            channel = client.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = client.get_user(payload.user_id)
            emoji = client.get_emoji(payload.emoji.id)
            await message.remove_reaction(emoji, user)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.onRawReactionEvent):
        if payload.user_id in self.voters:
            self.voters.pop(payload.user_id)


def setup(bot: commands.Bot):
    bot.add_cog(PollingCog(bot))
