# -*- coding: utf-8 -*-

import logging
import json

tbl = logging.getLogger('TBL')

DEFAULT = {'users': {}}


def setup_profiles(client):

    path = client.paths['profiles'].joinpath('profiles.json')

    if not path.exists():
        with path.open('w') as f:
            f.write(json.dumps(DEFAULT))
        tbl.info('Profiles created.')
        return DEFAULT

    with path.open() as f:
        profiles = json.load(f)
    tbl.info('Profiles loaded.')

    return profiles


def setup_user(client, user):
    if user not in client.profiles['users']:
        client.profiles['users'][user] = {'title': "",
                                          'flair': "",
                                          'badges': {}}
    return client.profiles['users'][user]


def get_from_profile(client, user, key):
    user = setup_user(client, user)
    return user.get(key, None)


def set_to_profile(client, user, key, val):
    user = setup_user(client, user)
    user[key] = val
    save_profiles(client)


def save_profiles(client):
    path = client.paths['profiles'].joinpath('profiles.json')
    with path.open('w') as f:
        f.write(json.dumps(client.profiles))
