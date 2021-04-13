# Config usage:
#   Copy this file and remove .example ==> 'cp config.example.py config.py'
#   See Mike or Bryan for any issues or questions.

# TOKENS:
#    Get tokens from discord dev portal/server, add them to
#    DISCORD_TOKEN and DISCORD_GUILD

import os

CONFIG = {
    # change this string to your preferred command prefix
    'PREFIX': ".",

    # change these strings to your prefered admin and default roles
    'ADMIN_ROLES' : [],
    'DEFAULT_ROLE': "",

    # Get tokens from discord dev portal/server, add them to
    'DISCORD_TOKEN' : "REPLACE ME",

    # DB config options, unless your dev environment is different, leave these alone
    'DBNAME': 'gonk_bot',
    'DBUSER': 'root',
    'DBPASS': '',
    'DBHOST': '',

    # API Keys
    'CMCKEY': 'REPLACE ME',

    # Sarcasm Cog banned channels
    'SARCASM_BAN': [
        # right-click channel -> copy id
    ],
}
