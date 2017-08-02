"""
System-related functions exist here.
Things like executing shell commands, setting system variables, automating tasks, and more.
"""

import subprocess as sub
from app import settings as cfg
from app.utils import _embed

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