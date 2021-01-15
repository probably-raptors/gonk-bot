import os
import config
import discord
from discord.ext import commands


config.init()

# Enable privledged intents for bot
intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(config.prefix, intents=intents)

# Enable all cogs in /modules
# Cog dir structure: /modules/<module_name>/cog.py
for folder in os.listdir("modules"):
    if os.path.exists(os.path.join("modules", folder, "cog.py")):
        bot.load_extension(f"modules.{folder}.cog")


@bot.event
async def on_ready():
    print("Squirrel Sweeper Bot reporting for duty, sir!")
    print("I am currently logged in as {0.user}".format(bot))


# Run the bot
bot.run(config.token)