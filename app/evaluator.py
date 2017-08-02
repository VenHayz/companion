"""
This file is a little bit more 'utility',
as it's sole purpose is just to evaluate different types of expressions.
"""

import discord, io, textwrap, traceback
from app import settings as cfg
from app.utils import _embed
from contextlib import redirect_stdout

async def python_eval(bot, message, marg):
    #result = eval(marg)

    env = {
        'discord': discord,
        'bot': bot,
        'message': message,
        'server': message.server
    }

    env.update(globals())

    stdout = io.StringIO()

    final = 'async def main_func_for_eval():\n%s' % textwrap.indent(marg, '  ')
    
    try:
        exec(final, env)
    except SyntaxError as e: # parsing errors are caught here
        em = _embed('Syntax Error', e.msg, cfg.colors.get('red'))
        await bot.send_message(message.channel, embed=em)

    func = env['main_func_for_eval']
    try:
        with redirect_stdout(stdout):
            ret = await func() # this is where the evaluation really happens
    except Exception as e: # actual problems at runtime handled here
        value = stdout.getvalue()
        em = _embed('Error', '```py\n{}{}\n```'\
        .format(value, traceback.format_exc()), cfg.colors.get('red'))
        await bot.send_message(message.channel, embed=em)
    else:
        value = stdout.getvalue()
        if ret is None:
            if value:
                em = _embed('Evaluated Python',\
                '{}'.format(value), cfg.colors.get('blue'))
                await bot.send_message(message.channel, embed=em)
        else:
            print('something is wrong...')