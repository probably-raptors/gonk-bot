from dotenv import load_dotenv
import os

def init():
    global prefix, admin_roles, default_role, token, guild_id

    # change this string to your preferred command prefix
    prefix = "./"

    # change these strings to your preferred admin and default roles
    admin_roles = ["Black Giant Squirrel", "Grizzled Squirrel"]
    default_role = "Kit"

    # leave these alone
    token = os.getenv("DISCORD_TOKEN")
    guild_id = os.getenv("DISCORD_GUILD")

    load_dotenv()