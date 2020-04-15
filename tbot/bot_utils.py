# -*- coding: utf-8 -*-

from .rules import admin_cmd
from .profiles import get_from_profile, setup_profiles, setup_user, save_profiles
from .catalog import setup_catalog


async def test(ctx):
    await ctx.message.channel.send("This is a test of the TBot command system.")


@admin_cmd
async def admin(ctx):
    if not ctx.line:
        await ctx.message.channel.send('You are an admin.')
        return

    # get from profile
    if len(ctx.line) == 3:
        if ctx.line[0] == "get":
            user = ctx.line[1]
            if user in member_names(ctx):
                val = get_from_profile(ctx.client, user, ctx.line[2])
                await ctx.message.channel.send('%s: %s' % (ctx.line[2], val))
            return

    if len(ctx.line) >= 3:
        if ctx.line[0] == "title":
            user = ctx.line[1]
            if user in member_names(ctx):
                if user not in ctx.client.profiles['users']:
                    setup_user(ctx.client, user)
                ctx.client.profiles['users'][user]['title'] = " ".join(ctx.line[2:])
                save_profiles(ctx.client)
            return
        if ctx.line[0] == "flair":
            user = ctx.line[1]
            if user in member_names(ctx):
                if user not in ctx.client.profiles['users']:
                    setup_user(ctx.client, user)
                new = ''.join(ctx.line[2:])
                ctx.client.profiles['users'][user]['flair'] = new
                save_profiles(ctx.client)
            return

    # reload profiles
    if len(ctx.line) == 2:

        if ctx.line[0] == "reload":
            if ctx.line[1] == "profiles":
                ctx.client.profiles = setup_profiles(ctx.client)
            if ctx.line[1] == "catalog":
                ctx.client.catalog = setup_catalog(ctx.client)
            return


def member_names(ctx):
    return [member.name for member in ctx.message.guild.members]