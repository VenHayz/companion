### INFO ###
# in bot files, this file is known as cfg ('import settings as cfg')

### SETTINGS YOU SHOULD ALTER ###
login = ['', '']
prefix = ';'

BOT_DEBUG = True # disable for performance; enable for more logging
DISCORD_LOGGING = False # enable to create a file called 'discord.log' and fill it with lots of things about what's happening in Discord

### DOES NOT NEED CHANGE, BUT YOU CAN ###
colors = {
    'black': 0x000000,
    'white': 0xFFFFFF,  # required: general actions/information
    'red': 0xFF0000,    # required: errors
    'blue': 0x0000FF,   # resuired: calculations
    'green': 0x00FF00,  # required: successful operations
    'yellow': 0xFFFF00  # required: warnings
}
embed_color = colors.get('black') # initial embed color
about_message = 'Selfbot \"Companion\"\nBy: lovesan\nVersion 0.1'
help_message = {
    'e <message>': 'Embed text with embed color.',
    'ec <[-n <new_color_name> <new_color_hex>]|<color_name>>': 'Change the color to embed text with.',
    'ping [-v] [hostname [times to ping]]': 'Test the networking speed of the bot.',
    'sh <command>': 'Run a shell command and embed the output.'
}
default_ping_hostname = 'www.google.com'
