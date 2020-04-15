# -*- coding: utf-8 -*-

import logging
from discord import FFmpegPCMAudio
from pathlib import Path


tbl = logging.getLogger('TBL')


async def play_clip(ctx, clip):
    path = Path(clip)
    if not path.is_file():
        await ctx.message.channel.send("Error: can't find clip file.")
        return

    if not ctx.message.author.voice:
        await ctx.message.channel.send("Error: you're not currently in a voice channel.")
        return

    if not ctx.client.voice:
        ctx.client.voice = await ctx.message.author.voice.channel.connect(timeout=5.0, reconnect=False)
        await ctx.client.voice.disconnect()
        ctx.client.voice = await ctx.message.author.voice.channel.connect(timeout=5.0, reconnect=True)

    src = FFmpegPCMAudio(path.open(),
                         executable="/usr/bin/ffmpeg",
                         pipe=True)
    try:
        ctx.client.voice.play(src, after=ctx.client.voice.stop())
    except:
        ctx.client.voice = await ctx.message.author.voice.channel.connect(timeout=5.0, reconnect=False)
        await ctx.client.voice.disconnect()
        ctx.client.voice = await ctx.message.author.voice.channel.connect(timeout=5.0, reconnect=True)
