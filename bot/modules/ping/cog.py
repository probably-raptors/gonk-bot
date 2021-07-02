from discord.ext import commands
import random


class PingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ping", pass_context=True)
    async def ping(self, ctx):
        """A simple command that responds to a ping"""

        with open("bot/modules/ping/responses.txt") as responses:
            await ctx.send(random.choice(responses.readlines()))


def setup(bot: commands.Bot):
    bot.add_cog(PingCog(bot))
