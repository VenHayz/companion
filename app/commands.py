import discord, subprocess as sub, asyncio, random, os, time, socket
from app import settings as cfg
from asyncio.coroutines import *

colors_backup = cfg.colors # used for resetting user colors
py_environment = None

### INFO ###
# you always need to pass an argument, 'bot', if you need to send messages

### COMMANDS ###
async def _help(bot, message, arg=None): #'_help' bc 'help' is already a python command
    em = discord.Embed(title='Help',description='Check the terminal.',colour=cfg.colors.get('white'))
    await bot.send_message(message.channel, embed=em)
    if arg == None: # no specific command help
        print('### HELP ###')
        for line in cfg.help_message:
            print('%s%s\t(%s)'%(cfg.prefix, line, cfg.help_message.get(line)))
        print('### HELP ###')
    else:
        em = discord.Embed(title='Error',description='Unknown command to request help for.',colour=cfg.colors.get('red'))
        await bot.send_message(message.channel, embed=em)

async def about(bot, message): # request about info
    em = discord.Embed(title='About',description=cfg.about_message,colour=cfg.colors.get('white'))
    await bot.send_message(message.channel, embed=em)

### COMMANDS / EMBED ###
async def embed(bot, message, marg): # embed a message
    em = discord.Embed(description=marg, colour=cfg.embed_color)
    await bot.send_message(message.channel, embed=em)

async def embedsetcolor(bot, message, carg): # set embed color
    if len(carg) > 1:
        if carg[0] == '-n': # definitely new color
            # ;ec -n purple 0x9900FF
            if not len(carg) == 3: # incorrect syntax
                error()
            new_color_name = carg[1] # purple
            new_color_hex = int(str(carg[2]).lower(), 0) # 0x9900FF
            try: # success
                cfg.colors.update({new_color_name: new_color_hex})
                em = discord.Embed(title='Success',description='Assigned color \"%s\" to %s.'%(new_color_name, hex(new_color_hex)), colour=new_color_hex)
                await bot.send_message(message.channel, embed=em)
                return
            except:
                em = discord.Embed(title='Error', description='Could not update color \"%s\" to %s.\n\nUsage `ec -n <new color name> <new color hex>`\nExample: `ec -n purple 0x9900FF`' %(new_color_name, new_color_hex), colour=cfg.colors.get('red'))
                await bot.send_message(message.channel, embed=em)
                return
    if carg[0] == '-r': # reset colors
        # ;ec -r
        if not len(carg) == 1:
            em = discord.Embed(title='Error',description='Incorrect syntax.\n\nUsage: `ec -r`')
            await bot.send_message(message.channel, embed=em)
            return
        try:
            cfg.colors = colors_backup
            em = discord.Embed(title='Success',description='Reset colors to default.', colour=cfg.colors.get('green'))
            await bot.send_message(message.channel, embed=em)
            return
        except:
            em = discord.Embed(title='Error',description='Incorrect syntax.\n\nUsage: `ec -r`')
            await bot.send_message(message.channel, embed=em)
            return
    color = carg[0]
    try:
        cfg.embed_color = cfg.colors.get(color)
        em = discord.Embed(title='Success',description='Assigned embed color to %s'%(hex(cfg.embed_color)), colour=cfg.embed_color)
        await bot.send_message(message.channel, embed=em)
    except:
        em = discord.Embed(title='Error', description='Could not find color \"%s\".\n\n`help ec` will list available colors.' %(color), colour=cfg.colors.get('red'))
        await bot.send_message(message.channel, embed=em)

### COMMANDS / SYSTEM ###
async def executeshell(bot, message, marg):
    lines = None
    try:
        child = sub.Popen(marg, stdout=sub.PIPE)
        lines = child.communicate()
        returnCode = child.returncode
        if cfg.BOT_DEBUG:
            print('[!]Attempting shell command \"%s\":\n |-Message: \"%s\"\n |-Return code: %d.'%(marg, lines, returnCode))
    except:
        try:
            em = discord.Embed(title=marg, description=str(lines).strip(), colour=cfg.colors.get('red'))
            await bot.send_message(message.channel, embed=em)
            return
        except:
            em = discord.Embed(title=marg, description='Could not obtain command output. Possibly too long to send over Discord. Attempting to display in terminal instead.', colour=cfg.colors.get('red'))
            await bot.send_message(message.channel, embed=em)
            return
    msg = ''
    lines = lines[0:len(lines)-1] # remove odd 'None'
    for line in lines:
        msg += '%s'%(str(bytes(line).strip().decode()))
    em = None
    try:
        if returnCode == 1:
            em = discord.Embed(title=marg, description='%s\nReturned: %d'%(msg, returnCode), colour=cfg.colors.get('red'))
        elif returnCode == 0:
            em = discord.Embed(title=marg, description='%s\nReturned: %d'%(msg, returnCode), colour=cfg.colors.get('green'))
        else:
            em = discord.Embed(title=marg, description='%s\nReturned: %d'%(msg, returnCode), colour=cfg.colors.get('yellow'))
        child.kill() # lovestokillchildren.jpeg
        await bot.send_message(message.channel, embed=em)
    except:
        em = discord.Embed(title=marg, description='Could not obtain command output. Possibly too long to send over Discord. Attempting to display in terminal instead.', colour=cfg.colors.get('red'))
        await bot.send_message(message.channel, embed=em)
        return

async def doeval(bot, message, marg):
    py_environment = sub.Popen('python', stdout=sub.PIPE, stdin=sub.PIPE, stderr=sub.PIPE) # create env
    result = py_environment.communicate(input='print(\'test\')')[0]
    print(result)

    em = discord.Embed(title='Eval', description=result, colour=cfg.colors.get('blue'))
    await bot.send_message(message.channel, embed=em)

    py_environment.kill()

### COMMANDS / NETWORKING ###
async def ping(bot, message, carg=None):
    async def error():
        msg = 'Usage: `ping [hostname [number of pings]]`'
        em = discord.Embed(title='Error', description=msg, colour=cfg.colors.get('red'))
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
        em = discord.Embed(title='Ping', description='%s\n%s'%(host,result), colour=cfg.colors.get('white'))
        await bot.send_message(message.channel, embed=em)
    else: # verbose
        msg = ''
        result = ping.readlines()
        for line in result:
            msg += '%s\n'%(str(line).strip())
        em = discord.Embed(title='Ping Verbose', description='%s\n%s'%(host,msg), colour=cfg.colors.get('white'))
        await bot.send_message(message.channel, embed=em)
