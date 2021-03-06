from discord.ext import commands
from config import CONFIG
import discord
import random

class SarcasmCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def sarcastify(self, msg):
        new_msg = ''
        for i, c in enumerate(msg):
            if i % 2: new_msg += c.upper()
            else:     new_msg += c.lower()

        return new_msg

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        # REQUIRED, otherwise the bot will also trigger this cog
        if msg.author.bot or msg.channel.id in CONFIG['SARCASM_BAN']:
            return

        # change the range to (1, 1) for testing / trolling
        if random.randint(1, 100) == 1:
            new_msg = self.sarcastify(msg.content)
            await msg.channel.send(new_msg)

def setup(bot: commands.Bot):
    bot.add_cog(SarcasmCog(bot))
