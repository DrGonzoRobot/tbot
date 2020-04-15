# -*- coding: utf-8 -*-

import logging
from datetime import datetime
import importlib.util as iu

tbl = logging.getLogger('TBL')


def setup_events(client):
    events = []
    path = client.paths['catalog'].joinpath('events')
    scripts = [script for script in path.iterdir() if str(script).endswith('.py')]
    for script in scripts:
        spec = iu.spec_from_file_location(script.name.split('.')[0], script)
        if spec:
            mod = iu.module_from_spec(spec)
            spec.loader.exec_module(mod)
            events += [mod.Event()]
            tbl.info("%s event loaded." % events[-1].name)

    return events


async def check_events(client):
    if not client.events:
        return
    for event in client.events:
        await event.trigger(client, datetime.now())
