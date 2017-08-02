### INFO ###
# in bot files, this file is known as cfg ("import settings as cfg")

### SETTINGS YOU SHOULD ALTER ###
login = ['lukemister777@mail.com', 'DiScOrD!@#$(4545?>)'] # don't forget to remove your account login when pushing to GitHub
prefix = ';' # Examples: / or ! etc.

DISCORD_LOGGING = False # enable to create a file called 'discord.log' and fill it with lots of things about what's happening in Discord

### DOES NOT NEED CHANGE, BUT YOU CAN ###
colors = {
    'black': 0x000000,
    'white': 0xFFFFFF,  # required: general actions/information
    'red': 0xFF0000,    # required: errors
    'blue': 0x0000FF,   # resuired: calculations
    'green': 0x00FF00,  # required: successful operations
    'yellow': 0xFFFF00  # required: warnings
    # 'random': ________ reserved
}
embed_color = colors.get('black') # initial embed color
about_message = 'Selfbot \"Companion\"\nBy: lovesan\nVersion 0.4'
help_message = {
    'e': [{'<message>', 'Embed a message with embed color.'}],
    'ec': [{'-r', 'Reset colors to default.'}, {'random', 'Use random colors for embeds.'}, {'-n <new color name> <new color hex>', 'Create a new color.'}, {'<color name>', 'Change the color to embed text with.'}],
    'ping': [{'[-v]': 'More information.'}, {'<hostname> [times to ping]': 'Ping a specific host.'}],
    'sh': [{'<command>': 'Run a shell command and embed the output.'}],
    'ev | eval': [{'<python>': 'Evaluate Python code and embed output.'}, {'': 'Evalute last Python program.'}]
}
default_ping_hostname = 'www.google.com'
