# -*- coding: utf-8 -*-

import configparser
import logging
import discord


tbl = logging.getLogger('TBL')
"""Logger: global Tbot logger for package."""


def setup_audio_config(data_path):
    """
    :param data_path: Path for tb_data directory
    :type data_path: pathlib.Path
    :return: audio_config for client to use
    :rtype: configparser.ConfigParser
    """
    audio_path = data_path.joinpath('audio.ini')
    audio_config = configparser.ConfigParser(interpolation=None)
    if audio_path not in data_path.iterdir():
        with audio_path.open(mode='w') as fin:
            fin.write('')
            tbl.info('audio.ini created.')
    try:
        audio_config.read_file(audio_path.open(errors='ignore'))
    except TypeError:
        audio_config.read_file(open(str(audio_path), errors='ignore'))

    return audio_config


async def play_clip(ctx, clips_path, clip):
    if not clips_path.joinpath(clip).is_file():
        await ctx.message.channel.send('Clip does not exist.')
        return

    if not ctx.message.author.voice:
        return

    if not ctx.client.voice:
        ctx.client.voice = await ctx.message.author.voice.channel.connect(timeout=5.0, reconnect=False)
        await ctx.client.voice.disconnect()
        ctx.client.voice = await ctx.message.author.voice.channel.connect(timeout=5.0, reconnect=False)

    print(ctx.client.config['FFMPEG']['Path'])
    src = discord.FFmpegPCMAudio(open(clips_path.joinpath(clip)),
                                 executable=ctx.client.config['FFMPEG']['Path'],
                                 pipe=True)
    ctx.client.voice.play(src, after=ctx.client.voice.stop())
