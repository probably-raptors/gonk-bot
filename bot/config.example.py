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
    'ADMIN_ROLES' : ["Black Giant Squirrel", "Grizzled Squirrel"],
    'DEFAULT_ROLE': "Kit",

    # Get tokens from discord dev portal/server, add them to
    'DISCORD_TOKEN' : "REPLACE ME",

    # DB config options, unless your dev environment is different, leave these alone
    'DBNAME': 'gonk_bot',
    'DBUSER': 'root',
    'DBPASS': '',
    'DBHOST': '',

    # API Keys
    'CMCKEY': '',
}
