# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path
import logging
import importlib.util as iu
from asyncio import sleep

from discord import Client

from .logs import start_log
from .context import Context
from .cmd_list import CMDS
from .config import setup_config
from .catalog import setup_catalog
from .audio import play_clip
from .badges import setup_badges, check_badges
from .profiles import setup_profiles, setup_user
from .events import setup_events, check_events


class TBot(Client):

    def __init__(self,
                 data_path=None,
                 debug=False):

        super(TBot, self).__init__()

        self._paths = None
        self.paths = {'start': sys.argv[0],
                      'data': data_path}

        start_log(self)

        self._tbl = None
        self.tbl = logging.getLogger('TBL')
        self.tbl.info('Logging started.')

        self._cmds = None
        self.cmds = CMDS

        self._config = None
        self.config = setup_config(self)

        self._catalog = None
        self.catalog = setup_catalog(self)

        self._voice = None
        self.voice = None

        self._profiles = None
        self.profiles = setup_profiles(self)

        self._badges = None
        self.badges = setup_badges(self)

        self._events = None
        self.events = setup_events(self)

        self.debug = debug

    def load_extensions(self, path=None):
        ext_path = self.paths['start'].joinpath('extensions')
        if path:
            path = Path(path)
            if path.exists():
                ext_path = path
        scripts = [path for path in ext_path.iterdir() if str(path).endswith('.py')]
        for script in scripts:
            spec = iu.spec_from_file_location(script.name.split('.')[0], script)
            if spec:
                mod = iu.module_from_spec(spec)
                spec.loader.exec_module(mod)
                self.cmds.update(mod.CMDS)

    #######
    # Paths

    @property
    def paths(self):
        return self._paths

    @paths.setter
    def paths(self, pathd):

        # start
        pathd['start'] = Path(os.path.dirname(pathd['start']))

        # data
        if not pathd['data']:
            path = pathd['start'].joinpath('tb_data')
            if not path.exists():
                path.mkdir()
            pathd['data'] = path

        # populate tb_data
        folders = ['logs',
                   'profiles',
                   'configs',
                   'catalog',
                   'catalog/audio',
                   'catalog/events',
                   'badges',
                   'badges/awards']

        for folder in folders:
            path = pathd['data'].joinpath(folder)
            if not path.exists():
                path.mkdir()
            pathd[folder] = pathd['data'].joinpath(folder)

        self._paths = pathd

    #####
    # TBL

    @property
    def tbl(self):
        return self._tbl

    @tbl.setter
    def tbl(self, obj):
        self._tbl = obj

    ######
    # CMDS

    @property
    def cmds(self):
        return self._cmds

    @cmds.setter
    def cmds(self, obj):
        self._cmds = obj

    ########
    # Config

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, obj):
        self._config = obj

    #########
    # Catalog

    @property
    def catalog(self):
        return self._catalog

    @catalog.setter
    def catalog(self, obj):
        self._catalog = obj

    ##########
    # Profiles

    @property
    def profiles(self):
        return self._profiles

    @profiles.setter
    def profiles(self, obj):
        self._profiles = obj

    ########
    # Badges

    @property
    def badges(self):
        return self._badges

    @badges.setter
    def badges(self, obj):
        self._badges = obj

    #######
    # Voice

    @property
    def voice(self):
        return self._voice

    @voice.setter
    def voice(self, obj):
        self._voice = obj

    ########
    # Events

    @property
    def events(self):
        return self._events

    @events.setter
    def events(self, obj):
        self._events = obj

    ########
    # Events

    async def on_ready(self):

        banner = '''
        +=========================================+
        [                 TB v5.0                 ]
        +=========================================+
        '''
        print(banner)

        while True:
            await check_events(self)
            await sleep(10)

    async def on_message(self, message):

        # First Law of Discord Robotics
        if message.author.bot:
            return
        
        # Silence Deplorable Users
        if 'TextChannel' in str(message.channel.__class__):
            if self.config['roles']['banned'] in [role.name for role in message.author.roles]:
                return

        ctx = Context(self, message)
        setup_user(self, ctx.message.author.name)

        if ctx.cmd in self.cmds:
            await self.cmds[ctx.cmd](ctx)

        if ctx.cmd in self.catalog['macros']:
            await ctx.message.channel.send(self.catalog['macros'][ctx.cmd]['text'])
            self.catalog['macros'][ctx.cmd]['count'] += 1

        if ctx.cmd in self.catalog['audio']:
            await play_clip(ctx, self.catalog['audio'][ctx.cmd]['clip'])

        await check_badges(self, ctx)
