# -*- coding: utf-8 -*-

import logging
tbl = logging.getLogger('TBL')


def admin_cmd(cmd):
    def wrapper(ctx):
        user_roles = [role.name for role in ctx.message.author.roles]
        if not ctx.client.roles['Admin']:
            err = 'An Admin role is not setup for tbot, commands requiring Admin role will not work.'
            return ctx.message.author.send(err)
        elif ctx.client.roles['Admin'] in user_roles:
            return cmd(ctx)
        else:
            return ctx.message.author.send('You need to be an Admin to use this command.')
    return wrapper
