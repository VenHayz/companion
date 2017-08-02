"""
Anything chat-specific exists here. Embedding a message, setting embed colors, the asthetics.
"""

import discord, random
from app import settings as cfg
from app.utils import _embed

use_random_colors = False
colors_backup = cfg.colors.copy() # used for resetting user colors

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