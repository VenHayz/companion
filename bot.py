"""
This file is the core of the bot.
It handles basic mapping of commands to their literal definitions in "commands.py".
"""

import discord, logging, asyncio
from asyncio.coroutines import *
from app import settings as cfg, evaluator, utils, networking, system, chat
print('[!] Import successful.')

### DISCORD_LOGGING ###
if cfg.DISCORD_LOGGING:
    print('[DISCORD_LOGGING] Starting logger...')
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
    print('[DISCORD_LOGGING] Logger started.')
### BOT INIT ###
print('[!] Starting bot. Takes about 5 seconds...')
bot = discord.Client()

@bot.event
async def on_ready():
    print('[+] Logged in as %s\n[+] With ID: %s' %(bot.user.name,bot.user.id))

last_message_sent = None
last_python_program = None

### HANDLE BOT COMMANDS ###
@bot.event
async def on_message(message):
    global bot
    if message.author == bot.user or utils.enable_open_bot:
        global last_message_sent
        global last_python_program
        global open_bot_user_requests
        if message.content.startswith(cfg.prefix):
            if utils.enable_open_bot and message.author != bot.user \
            and not cfg.verified_users.__contains__(message.author):
                print('User ({}) is attempting to access open bot from {} in channel {}. Verify them with ;verify.'.format(message.author, message.server, message.channel))
                open_bot_user_requests = utils.open_bot_user_requests + {message.author.name: message.content}
            # let's say we had a command: ;ping -v www.google.com
            call = message.content[1::1].split()[0] # command name                  ("ping")
            carg = message.content[1::1].split()[1::1] # seperate arguments         ("-v", "www.google.com")
            marg = message.content[len(call)+2::1] # arguments as whole message     ("-v www.google.com")

            if not utils.enable_open_bot or message.author == bot.user:
                await bot.delete_message(message)

            # Chat
            if call == 'e': # embed a message
                await chat.embed(bot, message, marg)
            elif call == 'ec': # set embed colour
                await chat.embedsetcolor(bot, message, carg)

            # Evaluator
            elif call == 'eval' or call == 'ev':
                if (len(marg) + len(call)) > len(call):         # ;eval 256 + 256
                    await evaluator.python_eval(bot, message, marg)
                elif not last_python_program is None:           # (last message is used as python code) ;eval
                    await evaluator.python_eval(bot, message, last_python_program)
                else:
                    em = discord.Embed(title='Evaluate Python', description='Nothing to evaluate.\n' +\
                    'You can create a python program with embedded code:\n```python\nprint(2 ** 8)\n```', colour=cfg.colors.get('red'))
                    await bot.send_message(message.channel, embed=em)
            
            # Networking
            elif call == 'ping': # ping a hostname                                  (ah, this is the correct call)
                if len(carg) > 0:
                    await networking.ping(bot, message, carg) #                       (we send our arguments to that command (in commands.py) and it pings)
                else:
                    await networking.ping(bot, message) #                             (we can do a default ping, but the above is what it fits)                               
            
            # System
            elif call == 'sh': # execute and embed a shell script's output
                await system.executeshell(bot, message, marg)
            
            # Utils
            elif call == 'help': # request help info
                if len(carg) > 0:
                    await utils._help(bot, message, carg[0])
                else:
                    await utils._help(bot, message)
            elif call == 'about': # request about info
                await utils.about(bot, message)

            # Open bot functionalities.
            elif call == 'open':
                await utils.open_bot(bot, message, True)
            elif call == 'close':
                await utils.open_bot(bot, message, False)
            elif call == 'verify':
                if cfg.ACCEPT_ONCE and message.author == bot.user:
                    cfg.verified_users.append(open_bot_user_requests[len(open_bot_user_requests) - 1])
                    print('User {} has been verified and added to list of verified users. (Use ;verified to see who\'s verified.)')
                else:
                    pass
            elif call == 'verified':
                em = discord.Embed(title='Verified Users', description=cfg.verified_users, colour=cfg.colors.get('white'))
                await bot.send_message(message.channel, embed=em)

            else: # we don't know what they mean in their command
                em = discord.Embed(title='Unknown call \"%s\"'%call, description='Check the terminal for usage information.', colour=cfg.colors.get('yellow'))
                await bot.send_message(message.channel, embed=em)
                await utils._help(bot, message, 'nomessage')
            return

        last_message_sent = message.content
        
        # build the python program from the message (if there is one)
        if str(last_message_sent).startswith('```python') or str(last_message_sent).startswith('```py'):
            last_python_program = '\n'.join(str(last_message_sent).split('\n')[1:-1])

### START BOT ###
try:
    bot.run(cfg.login[0], cfg.login[1]) # the email and password are from "settings.py"
except:
    print('[!] Unable to connect to Discord. Ensure login information is correct, ' \
          'and you are connected to the internet.')
    exit(1)
