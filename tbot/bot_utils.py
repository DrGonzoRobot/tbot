# -*- coding: utf-8 -*-
"""This module is for functions that help create bots and check they are running."""
from .rules import admin_cmd


def get_token(path):
    """
    Function for reading API secret token from text file.

    :arg path: The path string for file containing token
    :type path: str
    :returns: token
    :rtype: str
    :raises: TypeError if path is not a string
    """

    if not isinstance(path, str):
        raise TypeError("Path should be a string.")

    with open(path) as fin:
        chars = fin.read()
        token = "".join([char for char in chars if ord(char) < 128])

        return token


def debug_message(ctx):
    attrs = ['tts',
             'author',
             'content',
             'nonce',
             'embeds',
             'channel',
             'mention_everyone',
             'mentions',
             'channel_mentions',
             'role_mentions',
             'id',
             'attachments',
             'guild',
             'created_at',
             'jump_url']
    print('\n')
    for attr in attrs:
        print('%s: %s' % (attr, getattr(ctx.message, attr)))
    print('\n')


async def test(ctx):
    """
    This function can be used to check if Tbot is recognizing the !test command at least.

    :arg ctx: Context object for command.
    :type ctx: tbot.Context
    :returns: None
    :rtype: None
    :raises: None
    """
    await ctx.message.channel.send("This is a test of the TBot command system.")


@admin_cmd
async def admin(ctx):
    """
    This function can be used to check if Tbot is recognizing you're an admin.

    :arg ctx: Context object for command.
    :type ctx: tbot.Context
    :returns: None
    :rtype: None
    :raises: None
    """
    await ctx.message.channel.send("Woah. You're like an admin.")
