"""
In Python files, this is known as cfg ("import settings as cfg").
It holds user-specific information, and customizable options.

Any name with all uppercase letters is a variable that will not change while the bot is running.
Anything lowercase means that the property and it's value(s) will change (temporarily).
"""

'''You can change these values.'''
# Don't forget to remove your account login when pushing to GitHub or sharing.
login = ['', '']
prefix = ';' # Examples: / or ! etc.

# Enable to create a file called 'discord.log' and fill it with lots of things about what's happening in Discord.
DISCORD_LOGGING = False

'''These values do not need changing, but feel free to.'''
### Colors ###
colors = {
    'black': 0x000000,
    'white': 0xFFFFFF,  # required: general actions/information
    'red': 0xFF0000,    # required: errors
    'blue': 0x0000FF,   # resuired: calculations
    'green': 0x00FF00,  # required: successful operations
    'yellow': 0xFFFF00  # required: warnings
    # 'random': ________ reserved
}
embed_color = colors.get('black') # Initial embed color.

'''This information is bot-specific, so if you make any changes feel free to change any of this.'''
about_message = 'Selfbot \"Companion\"\nBy: lovesan\nVersion 0.4'
# The help message is a little messy, but that's because pretty printing dynamic values is hard without sacrifice.
help_message = {
    'e': [{'<message>', 'Embed a message with embed color.'}],
    'ec': [{'-r', 'Reset colors to default.'}, {'random', 'Use random colors for embeds.'}, {'-n <new color name> <new color hex>', 'Create a new color.'}, {'<color name>', 'Change the color to embed text with.'}],
    'ping': [{'[-v]': 'More information.'}, {'<hostname> [times to ping]': 'Ping a specific host.'}],
    'sh': [{'<command>': 'Run a shell command and embed the output.'}],
    'ev | eval': [{'<python>': 'Evaluate Python code and embed output.'}, {'': 'Evalute last Python program.'}]
}

'''These settings apply only to networking. You usually don\'t need to change them.'''
DEFAULT_PING_HOSTNAME = 'www.google.com'

'''You should look over these settings, as they control how "open bot" works for your bot.'''
ACCEPT_ONCE = True # If true, then when you accept a user, they are remembered and you no longer need to verify their commands.
verified_users = [] # When a user is verified for a command, all future ones are too. (with ACCEPT_ONCE, users are saved here)
