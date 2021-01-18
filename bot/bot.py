from discord.ext import commands
import discord
import random
import config
import os

config.init()

# Enable privledged intents for bot
intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(config.prefix, intents=intents)

# Enable all cogs in /modules
# Cog dir structure: /modules/<module_name>/cog.py
for folder in os.listdir("bot/modules"):
	if os.path.exists(os.path.join("bot/modules", folder, "cog.py")):
		try:
			bot.load_extension(f"modules.{ folder }.cog")
		except:
			print(f"Could not find a cog in { folder }")


@bot.event
async def on_ready():
	print("##### GONK #####")
	print(f"I am currently logged in as { bot.user }")


# Run the bot
bot.run(config.token)