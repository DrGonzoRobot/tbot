# -*- coding: utf-8 -*-

import logging
tbl = logging.getLogger('TBL')
from discord import DMChannel


def admin_cmd(cmd):
    def wrapper(ctx):
        user_roles = [role.name for role in ctx.message.author.roles]
        admin = ctx.client.config['roles']['admin']
        if not admin:
            err = 'An Admin role is not setup for tbot, commands requiring Admin role will not work.'
            return ctx.message.author.send(err)
        elif admin in user_roles:
            return cmd(ctx)
        else:
            return ctx.message.author.send('You need to be an Admin to use this command.')
    return wrapper


def dm_cmd(cmd):
    def wrapper(ctx):
        if not isinstance(ctx.message.channel, DMChannel):
            err = 'This command is only for DM messages with the bot. Please right click the bot and use "message"'
            return ctx.message.author.send(err)
        else:
            return cmd(ctx)
    return wrapper