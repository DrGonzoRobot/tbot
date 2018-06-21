# -*- coding: utf-8 -*-

from discord import Client
from .context import Context
from .cmd_list import cmds
from .logs import start_log
from .config import setup_config
from .macro_utils import setup_macros, save_macros
import logging
import sys
import os
from pathlib import Path
import importlib.util as iu


class TBot(Client):

    def __init__(self, data_path=None):
        super(TBot, self).__init__()

        self._start_path = Path(os.path.dirname(sys.argv[0]))
        self._data_path = None
        self._setup_data(data_path)

        start_log(self)
        self.tbl = logging.getLogger('TBL')
        self.tbl.info('Logging started.')

        self.config = setup_config(self._data_path)
        self.macros = setup_macros(self)
        self.tbl.info('Config loaded.')

        self.roles = self.config['ROLES']
        self.tbl.info('Roles loaded.')

        self.cmds = cmds
        self.tbl.info('Commands loaded.')

        self.tbl.info('Initialized! Get ready for action!')

    def load_extensions(self, path=None):
        ext_path = self._start_path.joinpath('extensions')
        if path:
            path = Path(path)
            if path.exists():
                ext_path = path
        mods = [path for path in ext_path.iterdir()]
        for mod in mods:
            spec = iu.spec_from_file_location(mod.name.split('.')[0], mod)
            if spec:
                foo = iu.module_from_spec(spec)
                spec.loader.exec_module(foo)
                self.cmds.update(foo.CMDS)

    def _setup_data(self, data_path):
        if not data_path:
            data_path = self._start_path.joinpath('tb_data')
            if data_path not in self._start_path.iterdir():
                data_path.mkdir()
        self.data_path = Path(data_path)

    @property
    def data_path(self):
        return self._data_path

    @data_path.setter
    def data_path(self, path):
        if not path.exists():
            raise NotADirectoryError
        self._data_path = path

    @staticmethod
    async def on_ready():
        banner = '''
        +=========================================+
        (╯°□°）╯︵ ┻━┻ [  TB v3.5  ] ┬─┬ ノ( ゜-゜ノ) 
        +=========================================+
        '''
        print(banner)

    async def on_message(self, message):

        # First Law of Discord Robotics
        if message.author.bot:
            return

        # Silence Deplorable Users
        if 'TextChannel' in str(message.channel.__class__):
            if self.roles['Banned'] in [role.name for role in message.author.roles]:
                return

        ctx = Context(self, message)

        if message.content.startswith('!') or message.content.startswith('$'):
            if ctx.cmd in self.cmds:
                self.tbl.info('%s: %s' % (str(message.author), message.content))
                await self.cmds[ctx.cmd](ctx)

        if message.content.startswith('%'):
            if ctx.cmd in self.macros:
                self.tbl.info('%s: %s' % (str(message.author), message.content))
                cnt = self.macros[ctx.cmd]['Count']
                self.macros[ctx.cmd]['Count'] = str(int(cnt) + 1)
                self.macros = save_macros(self, self.macros)
                await message.channel.send(self.macros[ctx.cmd]['Macro'])
