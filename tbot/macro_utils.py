# -*- coding: utf-8 -*-

from discord import Embed
import configparser
import logging

tbl = logging.getLogger('TBL')
"""Logger: global Tbot logger for package."""


def setup_macros(data_path):
    """
    Setup function loads client macros or creates a blank macros.ini file in tb_data.
    :param client: Tbot client
    :return: macros
    :rtype: configparser.Configparser
    """
    macros_path = data_path.joinpath('macros.ini')
    macros = configparser.ConfigParser(interpolation=None)
    if macros_path not in data_path.iterdir():
        with macros_path.open(mode='w') as fin:
            fin.write('')
            tbl.info('macros.ini created.')
    try:
        macros.read_file(macros_path.open(errors='ignore'))
    except TypeError:
        macros.read_file(open(str(macros_path), errors='ignore'))

    return macros


async def save_macros(client, macros):
    """
    Writes macro Configparser to macros.ini file.
    :param client: Tbot client
    :param macros: macros
    :return: None
    """
    macros_path = client.data_path.joinpath('macros.ini')
    with macros_path.open(mode='w') as fin:
        macros.write(fin)
    tbl.info('Macros saved.')
    macros.read_file(macros_path.open(errors='ignore'))


async def new_macro(ctx):
    """
    Creates a new macro cmd.
    :param ctx: Message context calling command.
    :return: None
    """
    err = '!new %name your macro'
    if len(ctx.line) < 2:
        await ctx.message.channel.send(err)
        return
    if ctx.line[0][0] != '%':
        await ctx.message.channel.send(err)
        return
    name = ctx.line[0]
    owner = ctx.message.author.name
    if name in ctx.client.macros:
        prev_owner = ctx.client.macros[name]['Owner']
        if ctx.client.roles['Admin']:
            user_roles = [role.name for role in ctx.message.author.roles]
            if ctx.client.roles['Admin'] in user_roles:
                prev_owner = owner
        if prev_owner != owner:
            await ctx.message.channel.send('{0} has already been set by {1}'.format(name, prev_owner))
            return
    ctx.client.macros[name] = {'Owner': owner,
                               'Macro': ' '.join([str(char) for char in ctx.line[1:]]),
                               'Count': '0',
                               'Upvotes': '',
                               'Downvotes': ''}
    tbl.info('New macro created: {0}'.format(name))
    await save_macros(ctx.client, ctx.client.macros)

    await ctx.message.channel.send('{0} has been set by {1}'.format(name, owner))
    return


async def list_macros(ctx):
    """
    Sends a current list of macros.
    :param ctx: Message context calling command.
    :return: None
    """
    title = 'TBot Macros'
    e = Embed(title=title)
    for macro in ctx.client.macros:
        if macro != 'DEFAULT':
            owner = ctx.client.macros[macro]['Owner']
            text = ctx.client.macros[macro]['Macro']
            ups = len(ctx.client.macros[macro]['Upvotes'].split(',')) - 1
            downs = len(ctx.client.macros[macro]['Downvotes'].split(',')) - 1
            e.add_field(name=macro,
                        value='''Owner: {0}
                                 Text: {1}
                                 Karma: {2}'''.format(owner, text, ups-downs))

    await ctx.message.author.send(embed=e)
    await ctx.message.channel.send('*sent {0} a list of macros.*'.format(ctx.message.author.name))
    return


async def upvote(ctx):
    """
    Gives an upvote to the macro.
    :param ctx: Message context calling command.
    :return: None
    """
    err = '!upvote %macro'
    if len(ctx.line) != 1:
        await ctx.message.channel.send(err)
        return
    name = ctx.line[0]
    if name in ctx.client.macros:
        ups = ctx.client.macros[name]['Upvotes'].split(',')
        downs = ctx.client.macros[name]['Downvotes'].split(',')
        voter = str(ctx.message.author)
        if voter not in ups:
            if voter in downs:
                ctx.client.macros[name]['Downvotes'] = ','.join([down for down in downs if down != voter])
            ctx.client.macros[name]['Upvotes'] = ','.join(ups + [voter])
            await save_macros(ctx.client, ctx.client.macros)
            ups = len(ctx.client.macros[name]['Upvotes'].split(',')) - 1
            downs = len(ctx.client.macros[name]['Downvotes'].split(',')) - 1
            tbl.info("Karma +1 for {0}, new Karma: {1}".format(name, ups - downs))
            await ctx.message.channel.send('+1 for {0}, Karma: {1}'.format(name, ups - downs))
            return
        else:
            await ctx.message.channel.send("You've already upvoted this macro!")
            return
    else:
        await ctx.message.channel.send('"{0}" is not a macro, yet.'.format(name))
        return


async def downvote(ctx):
    """
    Gives a downvote to the macro.
    :param ctx: Message context calling command.
    :return: None
    """
    err = '!downvote %macro'
    if len(ctx.line) != 1:
        await ctx.message.channel.send(err)
        return
    name = ctx.line[0]
    if name in ctx.client.macros:
        ups = ctx.client.macros[name]['Upvotes'].split(',')
        downs = ctx.client.macros[name]['Downvotes'].split(',')
        voter = str(ctx.message.author)
        if voter not in downs:
            if voter in ups:
                ctx.client.macros[name]['Upvotes'] = ','.join([up for up in ups if up != voter])
            ctx.client.macros[name]['Downvotes'] = ','.join(downs + [voter])
            await save_macros(ctx.client, ctx.client.macros)
            ups = len(ctx.client.macros[name]['Upvotes'].split(',')) - 1
            downs = len(ctx.client.macros[name]['Downvotes'].split(',')) - 1
            tbl.info("Karma -1 for {0}, new Karma: {1}".format(name, ups - downs))
            await ctx.message.channel.send('-1 for {0}, Karma: {1}'.format(name, ups - downs))
            return
        else:
            await ctx.message.channel.send("You've already downvoted this macro!")
            return
    else:
        await ctx.message.channel.send('"{0}" is not a macro, yet.'.format(name))
        return
