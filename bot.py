import os
import config
import discord
from discord.ext import commands


config.init()

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(config.prefix, intents=intents)


@bot.event
async def on_ready():
    print("Squirrel Sweeper Bot reporting for duty, sir!")
    print("I am currently logged in as {0.user}".format(bot))


@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


bot.run(config.token)