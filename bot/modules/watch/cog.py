from discord.ext import commands
import mysql.connector as mysql
import os, discord, db

class WatchCog(commands.Cog):
        def __init__(self, bot: commands.Bot):
                self.bot = bot

        @commands.command(name="watch", pass_context=True)
        async def on_watch(self, msg: discord.Message):
                # Only allow watch command in "crypto-prices" channel
                if msg.channel.id != 829037611841749063:
                        await msg.channel.send("Please send watch commands in <#829037611841749063>")
                        return

                dbh = db.get_dbh()
                cur = dbh.cursor(buffered=True)
                cur.close()
                
                await msg.channel.send("This is a test")
                return

def setup(bot: commands.Bot):
        bot.add_cog(WatchCog(bot))
