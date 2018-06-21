# -*- coding: utf-8 -*-

from discord import Embed
import configparser
import logging

tbl = logging.getLogger('TBL')


def setup_macros(client):
    macros_path = client.data_path.joinpath('macros.ini')
    macros = configparser.ConfigParser(interpolation=None)
    if macros_path not in client.data_path.iterdir():
        with macros_path.open(mode='w') as fin:
            fin.write('')
            tbl.info('macros.ini created.')
    macros.read(macros_path, encoding='utf-8')

    return macros


def save_macros(client, macros):
    macros_path = client.data_path.joinpath('macros.ini')
    with macros_path.open(mode='w') as fin:
        macros.write(fin)
    tbl.info('Macros saved.')

    return macros


async def new_macro(ctx):
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
        if prev_owner != owner:
            await ctx.message.channel.send('{0} has already been set by {1}'.format(name, prev_owner))
            return
    ctx.client.macros[name] = {'Owner': owner,
                               'Macro': ' '.join([str(char) for char in ctx.line[1:]]),
                               'Count': '0',
                               'Upvotes': '',
                               'Downvotes': ''}
    tbl.info('New macro created: {0}'.format(name))
    save_macros(ctx.client, ctx.client.macros)

    await ctx.message.channel.send('{0} has been set by {1}'.format(name, owner))
    return


async def list_macros(ctx):
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
            save_macros(ctx.client, ctx.client.macros)
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
            save_macros(ctx.client, ctx.client.macros)
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
