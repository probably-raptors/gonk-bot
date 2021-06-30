from discord.ext import commands
from config import CONFIG
import discord
import random
import re


class SarcasmCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def sarcastify(self, msg):
        """Convert message string to SaRcAsM tExT"""
        new_msg = ""
        for i, c in enumerate(msg):
            if i % 2:
                new_msg += c.upper()
            else:
                new_msg += c.lower()

        return new_msg

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return  # prevent the bot from sarcastifying it's own messages

        if msg.channel.id in CONFIG["SARCASM_BAN"]:
            return  # prevent the bot from sarcastifying in banned channels

        pattern = "<URL PATTERNS ARE SOOOOOO LONG>"
        if re.match(pattern, msg):
            return  # prevent bot from sarcastifying URLs

        if random.randint(1, 100) == 1:
            # change the range to (1, 1) for testing / trolling
            new_msg = self.sarcastify(msg.content)
            await msg.channel.send(new_msg)


def setup(bot: commands.Bot):
    bot.add_cog(SarcasmCog(bot))
