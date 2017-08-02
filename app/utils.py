"""
Anything that doesn't fit category-wise with any other modules.
"""

import discord
from sys import stdout
from app import settings as cfg

async def _help(bot, message, arg=None): # '_help' bc 'help' is already a python command
    if not arg == 'nomessage': # used by "bot.py" for usage
        em = _embed('Help', 'Check the terminal.', cfg.colors.get('white'))
        await bot.send_message(message.channel, embed=em)
    if arg == None or arg == 'nomessage': # no specific command help
        print('\nHelp\nUsage:')

        # print all commands (usage)
        for usage in cfg.help_message:
            print('\t%s%s' % (cfg.prefix, usage))
            for options in cfg.help_message.get(usage):#()
                stdout.flush()
                print('\t\t%s' % options)
    else:
        em = _embed('Error','Unknown command to request help for.',cfg.colors.get('red'))
        await bot.send_message(message.channel, embed=em)

async def about(bot, message): # request about info
    em = _embed('About',cfg.about_message,cfg.colors.get('white'))
    await bot.send_message(message.channel, embed=em)

open_bot_user_requests = {} # unverified users making requests are pushed here (user: command)
enable_open_bot = False # if True, then the bot can be used by anyone

async def open_bot(bot, message, toggle):
    global enable_open_bot
    em = None
    if toggle is True:
        enable_open_bot = True
        em = _embed('Opened Bot', '', cfg.colors.get('red'))
    else:
        enable_open_bot = False
        em = _embed('Closed Bot', '', cfg.colors.get('green'))
    await bot.send_message(message.channel, embed=em)

def _embed(title, message, color):
    """
    A wrapper to discord.Embed to make embed code shorter and simpler.
    """
    if title == '':
        return discord.Embed(description=message, colour=color)
    elif message == '':
        return discord.Embed(title=title, colour=color)
    return discord.Embed(title=title, description=message, colour=color)