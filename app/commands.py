"""
This file handles the instructions commands execute.
These are executed by "bot.py" in their callings, with the proper arguments for the job.
"""

# imports
import discord, subprocess as sub, asyncio, random, os, time, socket
from sys import stdout
from app import settings as cfg
import asyncio.coroutines

# temporary settings (e.g. when random colors are enabled, it's not persistent)
use_random_colors = False
colors_backup = cfg.colors.copy() # used for resetting user colors
py_environment = None

### UTILS ###
def _embed(title, message, color):
    """
    A wrapper to discord.Embed to make embed code shorter and simpler.
    """
    if title == '':
        return discord.Embed(description=message, colour=color)
    return discord.Embed(title=title, description=message, colour=color)

### COMMANDS ###
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

### COMMANDS / EMBED ###
async def embed(bot, message, marg): # embed a message
    if use_random_colors is True:
        new_random_color = int('0x%06x' % random.randint(0, 0xFFFFFF), 16)
        em = _embed('', marg, new_random_color)
        await bot.send_message(message.channel, embed=em)
        return
    else:
        em = _embed('', marg, cfg.embed_color)
        await bot.send_message(message.channel, embed=em)
        return

async def embedsetcolor(bot, message, carg): # set embed color
    global use_random_colors
    global use_auto_embeds
    if len(carg) > 1:
        if carg[0] == '-n': # new color
            # ;ec -n purple 0x9900FF
            if not len(carg) == 3: # incorrect syntax
                em = _embed('Error', 'Incorrect syntax.', cfg.colors.get('red'))
                await bot.send_message(message.channel, embed=em)
                return
            new_color_name = carg[1] # purple
            new_color_hex = int(str(carg[2]).lower(), 0) # 0x9900FF
            try: # success
                cfg.colors.update({new_color_name: new_color_hex})
                em = _embed('Success', 'Assigned color \"%s\" to %s.'%(new_color_name, hex(new_color_hex)), new_color_hex)
                await bot.send_message(message.channel, embed=em)
                return
            except:
                em = _embed('Error', 'Could not update color \"%s\" to %s.\n\nUsage `ec -n <new color name> <new color hex>`.\nExample: `ec -n purple 0x9900FF`.'%(new_color_name, new_color_hex), cfg.colors.get('red'))
                await bot.send_message(message.channel, embed=em)
                return
    if carg[0] == '-r': # reset colors
        if not len(carg) == 1:
            em = _embed('Error', 'Incorrect syntax.\n\nUsage: `ec -r`.', cfg.colors.get('red'))
            await bot.send_message(message.channel, embed=em)
            return
        try:
            cfg.colors = colors_backup
            print(colors_backup)
            em = _embed('Success', 'Reset colors to default.', cfg.colors.get('green'))
            await bot.send_message(message.channel, embed=em)
            return
        except:
            em = _embed('Error', 'Incorrect syntax.\n\nUsage: `ec -r`.', cfg.colors.get('red'))
            await bot.send_message(message.channel, embed=em)
            return
    if carg[0] == 'random': # random colors
        use_random_colors = True
        em = _embed('Success', 'Enabled random embed colors.', cfg.colors.get('green'))
        await bot.send_message(message.channel, embed=em)
        return
    color = carg[0]
    try:
        cfg.embed_color = cfg.colors.get(color)
        em = _embed('Success', 'Assigned embed color to %s.'%hex(cfg.embed_color), cfg.embed_color)
        await bot.send_message(message.channel, embed=em)
    except:
        em = _embed('Error', 'Could not find color \"%s\".\n\n`help ec` will list available colors.'%(color), cfg.colors.get('red'))
        await bot.send_message(message.channel, embed=em)
        pass
    use_random_colors = False # keep from printing random colors if using specific colors

### COMMANDS / SYSTEM ###
async def executeshell(bot, message, marg):
    lines = None
    try:
        child = sub.Popen(marg, stdout=sub.PIPE)
        lines = child.communicate()
        returnCode = child.returncode
    except:
        try:
            em = _embed(marg, str(lines).strip(), cfg.colors.get('red'))
            await bot.send_message(message.channel, embed=em)
            return
        except:
            em = _embed(marg, 'Could not obtain command output. Possibly too long to send over Discord. Attempting to display in terminal instead.', cfg.colors.get('white'))
            await bot.send_message(message.channel, embed=em)
            return
    msg = ''
    lines = lines[0:len(lines)-1] # remove odd 'None'
    for line in lines:
        msg += '%s'%(str(bytes(line).strip().decode()))
    em = None
    try:
        if returnCode == 1:
            em = _embed(marg, '%s\nReturned: %d'%(msg, returnCode), cfg.colors.get('red'))
        elif returnCode == 0:
            em = _embed(marg, '%s\nReturned: %d'%(msg, returnCode), cfg.colors.get('green'))
        else:
            em = _embed(marg, '%s\nReturned: %d'%(msg, returnCode), cfg.colors.get('yellow'))
        child.kill() # lovestokillchildren.jpeg
        await bot.send_message(message.channel, embed=em)
    except:
        em = _embed(marg, 'Could not obtain command output. Possibly too long to send over Discord. Attempting to display in terminal instead.', cfg.colors.get('red'))
        await bot.send_message(message.channel, embed=em)
        return

async def doeval(bot, message, marg):
    result = eval(marg)

    em = None
    if len(marg) < 15: # pretty printing
        em = _embed(marg, result, cfg.colors.get('blue'))
    else:
        em = _embed('Evaluated Python', result, cfg.colors.get('blue'))
    await bot.send_message(message.channel, embed=em)

### COMMANDS / NETWORKING ###
async def ping(bot, message, carg=None):
    async def error():
        msg = 'Usage: `ping [hostname [number of pings]]`'
        em = _embed('Error', msg, cfg.colors.get('red'))
        await bot.send_message(message.channel, embed=em)
        return
    host = cfg.default_ping_hostname
    times = 1
    fullDetails = False
    ### ARGUMENT PARSING ###
    if not carg == None:
        if '-v' in carg:
            fullDetails = True
            if len(carg) == 2:
                host = carg[1]
            elif len(carg) == 3:
                host = carg[1]
                times = carg[2]
            else:
                await error()
        elif len(carg) > 1:
            host = carg[0]
            times = carg[1]
        elif len(carg) == 1:
            host = carg[0]
        else:
            await error()
    ping = os.popen('ping %s -n %s' %(host, times))
    if not fullDetails:
        result = ping.readlines()
        result = result[-1].strip()
        result = result[0:len(result)-1] # remove trailing comma
        em = _embed('Ping', '%s\n%s'%(host,result), cfg.colors.get('white'))
        await bot.send_message(message.channel, embed=em)
    else: # verbose
        msg = ''
        result = ping.readlines()
        for line in result:
            msg += '%s\n'%(str(line).strip())
        em = _embed('Ping Verbose', '%s\n%s'%(host,msg), cfg.colors.get('white'))
        await bot.send_message(message.channel, embed=em)
