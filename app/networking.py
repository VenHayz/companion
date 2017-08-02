"""
Internet-related functionality. Things like testing internet speed,
creating or connecting to sockets, and more.
"""

import os
from app import settings as cfg
from app.utils import _embed

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