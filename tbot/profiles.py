from .rules import admin_cmd
import json
import logging

tbl = logging.getLogger('TBL')


def setup_profiles(data_path):
    profiles_path = data_path.joinpath('profiles/')
    if profiles_path not in data_path.iterdir():
        profiles_path.mkdir(parents=True, exist_ok=True)
        tbl.info("Profile directory created.")
    return profiles_path


def get_profile(ctx, member):
    if '#' not in member:
        tbl.info("Member username not in the correct format.")
        return
    fname = str(member) + ".json"
    profile_path = ctx.client.profiles.joinpath(fname)
    if profile_path not in ctx.client.profiles.iterdir():
        with profile_path.open(mode='w') as fout:
            profile = {'name': str(member)}
            fout.write(json.dumps(profile))
            tbl.info("Profile %s created." % fname)
            return profile
    with profile_path.open(mode='r') as fin:
        profile = json.load(fin)
    return profile


def save_profile(ctx, profile):
    fname = str(profile['name']) + ".json"
    profile_path = ctx.client.profiles.joinpath(fname)
    with profile_path.open(mode='w') as fout:
        fout.write(json.dumps(profile))
    with profile_path.open(mode='r') as fin:
        profile = json.load(fin)
    tbl.info('Profile %s saved.' % fname)
    return profile


def get_all_profiles(ctx):
    profiles = []
    for fname in ctx.client.profiles.iterdir():
        with fname.open(mode='r') as fin:
            profiles += [json.load(fin)]
    return profiles


@admin_cmd
async def debug_profile(ctx):
    if not ctx.line:
        return
    member = ctx.line[0]
    profile = get_profile(ctx, member)
    await ctx.message.channel.send(str(profile))
