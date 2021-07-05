# How to use:
#   Copy this file to the same directory and rename it to "config.py" (no quotes)

import os

CONFIG = {
    # False for dev mode
    "BOT_LIVE": False,
    # ADMIN ID, right-click user -> copy id
    "ADMIN_NOTIFY": 0,
    # DEV CHANNEL: right-click channel -> copy id
    "DEV_CHANNEL": 0,
    # Change this string to your preferred command prefix
    # Spaces are valid in command prefixes but should be avoided
    "PREFIX": "/",
    # Change these strings to your prefered admin and default roles
    "ADMIN_ROLES": [],
    "DEFAULT_ROLE": "",
    # DISCORD_TOKEN: Available in the Discord Developer Portal for your bot
    "DISCORD_TOKEN": "",
    # DB config options
    "DBNAME": "",
    "DBUSER": "",
    "DBPASS": "",
    "DBHOST": "",
    # API Keys
    # COINMARKETCAP
    "CMCKEY": "",
    # Coin Watch cog channel
    # right-click channel -> copy id
    "WATCH_CHANNEL": 0,
    # Sarcasm Cog banned channels
    "SARCASM_BAN": [
        # right-click channel -> copy id
    ],
}
