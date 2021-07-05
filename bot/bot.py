from discord.ext import commands
from config import CONFIG
import discord


bot = commands.Bot(CONFIG["PREFIX"], intents=discord.Intents.all())

extensions = [
    "modules.ping.cog",
    "modules.sarcasm.cog",
    "modules.roles.cog",
    "modules.watch.cog",
]

for extension in extensions:
    bot.load_extension(extension)


@bot.event
async def on_ready():
    print(f"################## GONK ##################")
    print(f"I am currently logged in as { bot.user }")


# Run the bot
bot.run(CONFIG["DISCORD_TOKEN"])
