# -*- coding: utf-8 -*-

import json
import logging

DEFAULT = {'roles': {'admin': None,
                     'banned': None},
           'ffmpeg': None}

tbl = logging.getLogger('TBL')


def setup_config(client):

    path = client.paths['configs'].joinpath('config.json')

    if not path.exists():
        with path.open('w') as f:
            f.write(json.dumps(DEFAULT))
        tbl.info('Config created.')
        return DEFAULT

    with path.open() as f:
        config = json.load(f)
    tbl.info('Config loaded.')

    return config
