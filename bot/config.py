from dotenv import load_dotenv
import os

def init():
    global prefix, token, guild_id
    prefix = "./"
    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")
    guild_id = os.getenv("DISCORD_GUILD")
