# -*- coding: utf-8 -*-


def get_token(path):
    try:
        with open(path) as fin:
            chars = fin.read()
            token = "".join([char for char in chars if ord(char) < 128])

            return token

    except FileNotFoundError:
        raise FileNotFoundError


async def test(ctx):
    await ctx.message.channel.send('This is a test of the TBot command system.')
