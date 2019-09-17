# -*- coding: utf-8 -*-

import configparser
import logging
import discord
from pydub import AudioSegment, effects


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

    for clip in audio_config:
        if clip == "DEFAULT":
            continue
        if "Normalized" not in audio_config[clip]:
            audio_config[clip]['Normalized'] = 'N'
        if audio_config[clip]['Normalized'] == 'N':
            fname = audio_config[clip]['Clip']
            if fname.split('.')[-1] == 'mp3':
                sf = AudioSegment.from_mp3(str(data_path.joinpath('clips').joinpath(fname)))
                effects.normalize(sf)
                effects.normalize(sf)
                sf.export(str(data_path.joinpath('clips').joinpath(fname)), format="mp3")
                audio_config[clip]['Normalized'] = 'Y'
            if fname.split('.')[-1] == 'wav':
                sf = AudioSegment.from_wav(str(data_path.joinpath('clips').joinpath(fname)))
                effects.normalize(sf)
                effects.normalize(sf)
                sf.export(str(data_path.joinpath('clips').joinpath(fname)), format="wav")
                audio_config[clip]['Normalized'] = 'Y'
        fname = audio_config[clip]['Clip']
        sf = AudioSegment.from_mp3(str(data_path.joinpath('clips').joinpath(fname)))
        from pydub.utils import make_chunks

        def get_loudness(sound, slice_size=60 * 1000):
            return max(chunk.dBFS for chunk in make_chunks(sound, slice_size))

        print(get_loudness(sf))

    with audio_path.open(mode='w') as fin:
        audio_config.write(fin)

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

    src = discord.FFmpegPCMAudio(open(clips_path.joinpath(clip)),
                                 executable=ctx.client.config['FFMPEG']['Path'],
                                 pipe=True)

    ctx.client.voice.play(src, after=ctx.client.voice.stop())
