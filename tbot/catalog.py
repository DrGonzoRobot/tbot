# -*- coding: utf-8 -*-

import json
import logging
import aiohttp

from pydub import effects, AudioSegment

tbl = logging.getLogger('TBL')


DEFAULT = {"macros": {},
           "audio": {}}


def check_for_admin(ctx):
    return ctx.client.config['roles']['admin'] in [role.name for role in ctx.message.author.roles]


def setup_catalog(client):

    path = client.paths['catalog'].joinpath('catalog.json')

    if not path.exists():
        with path.open('w') as f:
            f.write(json.dumps(DEFAULT))
        tbl.info('Catalog created.')
        return DEFAULT

    with path.open() as f:
        catalog = json.load(f)

    tbl.info('Catalog loaded.')
    return catalog


def save_catalog(client):

    path = client.paths['catalog'].joinpath('catalog.json')
    with path.open('w') as f:
        f.write(json.dumps(client.catalog))


async def modify_macro(ctx):

    if ctx.line[0] in ctx.client.catalog['macros']:
        if ctx.message.author.name != ctx.client.catalog['macros'][ctx.line[0]]['creator']:
            if not check_for_admin(ctx):
                return "You cannot modify this %macro."

    creator = ctx.message.author.name
    macro = ctx.line[0]

    text = ' '.join(ctx.line[1:])

    # print(creator, macro, author, text)

    ctx.client.catalog['macros'][macro] = {"creator": creator,
                                           "text": text,
                                           "count": 1}

    save_catalog(ctx.client)
    return "%s saved." % macro


async def modify_audio(ctx):
    # print(ctx.message.attachments[0])

    if ctx.line[0] in ctx.client.catalog['audio']:
        if ctx.message.author.name != ctx.client.catalog['audio'][ctx.line[0]]['creator']:
            if not check_for_admin(ctx):
                return "You cannot modify this %clip."

    creator = ctx.message.author.name
    clip = ctx.line[0]

    async with aiohttp.ClientSession() as session:
        async with session.get(ctx.message.attachments[0].url) as resp:
            data = await resp.read()

    fname = ctx.message.attachments[0].filename
    path = ctx.client.paths['catalog'].joinpath('audio').joinpath(fname)
    with path.open('wb') as f:
        f.write(data)

    audio = AudioSegment.from_wav(str(path))
    effects.normalize(audio)
    effects.normalize(audio)
    audio.export(str(path), format="wav")

    ctx.client.catalog['audio'][clip] = {"creator": creator,
                                         "clip": str(path),
                                         "count": 1}

    save_catalog(ctx.client)
    return "%s saved." % clip


async def save(ctx):
    if len(ctx.line) >= 2:
        if ctx.line[0][0] == "%" and len(ctx.line[0]) > 1:
            status = await modify_macro(ctx)
            await ctx.message.channel.send(status)

    if len(ctx.line) == 1:
        if ctx.line[0][0] == "&" and ctx.message.attachments:
            if not check_for_admin(ctx):
                await ctx.message.channel.send("Only admins can add audio clips.")
                return
            if not ctx.message.attachments[0].filename.endswith('.wav'):
                await ctx.message.channel.send("Error: Clip is not a .wav")
                return
            status = await modify_audio(ctx)
            await ctx.message.channel.send(status)
