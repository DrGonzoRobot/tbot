# -*- coding: utf-8 -*-

import importlib.util as iu
import logging

from discord import File, Embed

tbl = logging.getLogger('TBL')


def setup_badges(client):
    badges = []
    path = client.paths['badges']
    scripts = [script for script in path.iterdir() if str(script).endswith('.py')]
    for script in scripts:
        spec = iu.spec_from_file_location(script.name.split('.')[0], script)
        if spec:
            mod = iu.module_from_spec(spec)
            spec.loader.exec_module(mod)
            badges += [mod.Badge()]
            tbl.info("%s badge loaded." % badges[-1].name)

    return badges


async def check_badges(client, ctx):
    if not client.badges:
        return
    for badge in client.badges:
        award = await badge.trigger(ctx)
        if award:
            msg = "%s has leveled up a badge!\n%s\n%s" % (award[0],
                                                          badge.flavor,
                                                          badge.levels[award[1]]['award']['text'])
            e = Embed(title="%s has leveled up a badge!" % award[0])
            e.add_field(name="badge: ",
                        value="%s" % badge.flavor,
                        inline=False)
            e.add_field(name="lvl: %s - " % award[1],
                        value="%s" % badge.levels[award[1]]['award']['text'],
                        inline=False)
            await ctx.message.channel.send(embed=e)

            if badge.levels[award[1]]['award']['image']:
                path = client.paths['badges'].joinpath('awards').joinpath(badge.levels[award[1]]['award']['image'])
                with path.open('rb') as f:
                    fname = File(f)
                await ctx.message.channel.send(":trophy:", file=fname)


async def brag(ctx):
    badges = ctx.client.profiles['users'][ctx.message.author.name]['badges']
    title = ctx.client.profiles['users'][ctx.message.author.name]['title']
    flair = ctx.client.profiles['users'][ctx.message.author.name]['flair']
    e = Embed(title="%s" % ctx.message.author.name)
    if title:
        e.add_field(name="Title: ",
                    value=title,
                    inline=False)
    if flair:
        e.add_field(name="Flair: ",
                    value=flair,
                    inline=False)
    for key in badges:
        e.add_field(name="%s: %s" % (key, badges[key]['title']),
                    value="lvl: %s\nxp: %s\n%s" % (badges[key]['lvl'], badges[key]['xp'], badges[key]['flair']),
                    inline=False)
    await ctx.message.channel.send(embed=e)