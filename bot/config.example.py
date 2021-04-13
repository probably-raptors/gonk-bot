# Config usage:
#   Copy this file and remove .example ==> 'cp config.example.py config.py'
#   See Mike or Bryan for any issues or questions.

# TOKENS:
#    Get tokens from discord dev portal/server, add them to
#    DISCORD_TOKEN

import os

CONFIG = {
    # ADMIN ID, right-click user -> copy id, primary admin of who
    # should be notified when certain errors occur
    'ADMIN_NOTIFY': 0,

    # DEV CHANNEL, right-click channel -> copy id ,channel where all
    # commands are allowed for dev purposes.
    'DEV_CHANNEL': 0,

    # change this string to your preferred command prefix
    'PREFIX': '.',

    # change these strings to your prefered admin and default roles
    'ADMIN_ROLES' : [],
    'DEFAULT_ROLE': '',

    # Get tokens from discord dev portal/server, add them to
    'DISCORD_TOKEN' : '',

    # DB config options, unless your dev environment is different,
    # leave these alone
    'DBNAME': '',
    'DBUSER': '',
    'DBPASS': '',
    'DBHOST': '',

    # API Keys
    'CMCKEY': '', # COINMARKETCAP

    # Sarcasm Cog banned channels
    'SARCASM_BAN': [
        # right-click channel -> copy id
    ],

    # Coin Watch cog channel
    # right-click channel -> copy id
    'WATCH_CHANNEL': 0,

}
