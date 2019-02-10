# -*- coding: utf-8 -*-
"""This module contains the TBot class which inherits from discord.Client."""

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
    """This is the main client class."""

    def __init__(self, data_path=None):
        """
        :param data_path: (Optional) Absolute path string to a tb_data directory
        :type data_path: str or None
        """
        super(TBot, self).__init__()

        self._start_path = None
        self.start_path = sys.argv[0]

        self._data_path = None
        self.data_path = data_path

        start_log(self)
        
        self._tbl = None
        self.tbl = logging.getLogger('TBL')
        self.tbl.info('Logging started.')

        self._config = None
        self.config = setup_config(self.data_path)
        self._macros = None
        self.macros = setup_macros(self)
        self.tbl.info('Config loaded.')

        self._roles = None
        self.roles = self.config['ROLES']
        self.tbl.info('Roles loaded.')

        self._cmds = None
        self.cmds = cmds
        self.tbl.info('Commands loaded.')

        self.tbl.info('Initialized! Get ready for action!')

    def load_extensions(self, path=None):
        """
        This function loads extension scripts from a designated directory.
        :param path: (Optional) Absolute path string to an extensions directory
        :type path: str or None
        :return: None
        """
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

    @property
    def start_path(self):
        """
        Path where bot's main script was started
        :return: start_path
        :rtype: pathlib.Path
        """
        return self._start_path

    @start_path.setter
    def start_path(self, path):
        self._start_path = Path(os.path.dirname(path))

    @start_path.deleter
    def start_path(self):
        del self._start_path

    @property
    def data_path(self):
        """
        Path where tb_data is located
        :return: data_path
        :rtype: pathlib.Path
        """
        return self._data_path

    @data_path.setter
    def data_path(self, path):
        if path is None:
            path = self._start_path.joinpath('tb_data')
            if path not in self._start_path.iterdir():
                path.mkdir()
        self._data_path = Path(path)

    @data_path.deleter
    def data_path(self):
        del self._data_path
        
    @property
    def tbl(self):
        """
        Tbot logger
        :return: tbl
        :rtype: logging.Logger
        """
        return self._tbl

    @tbl.setter
    def tbl(self, obj):
        self._tbl = obj

    @tbl.deleter
    def tbl(self):
        del self._tbl

    @property
    def config(self):
        """
        Tbot config file
        :return: config
        :rtype: configparser.ConfigParser
        """
        return self._config

    @config.setter
    def config(self, obj):
        self._config = obj

    @config.deleter
    def config(self):
        del self._config

    @property
    def macros(self):
        """
        Macros storage
        :return: macros
        :rtype: configparser.ConfigParser
        """
        return self._macros

    @macros.setter
    def macros(self, obj):
        self._macros = obj

    @macros.deleter
    def macros(self):
        del self._macros

    @property
    def roles(self):
        """
        Roles for Admin and Banned users.
        :return: configparser.SectionProxy
        """
        return self._roles

    @roles.setter
    def roles(self, obj):
        self._roles = obj

    @roles.deleter
    def roles(self):
        del self._roles

    @property
    def cmds(self):
        """
        Cmds for bot client.
        :return: cmds
        :rtype: dict
        """
        return self._cmds

    @cmds.setter
    def cmds(self, obj):
        self._cmds = obj

    @cmds.deleter
    def cmds(self):
        del self._cmds

    @staticmethod
    async def on_ready():
        banner = '''
        +=========================================+
        (╯°□°）╯︵ ┻━┻ [  TB v3.51d  ] ┬─┬ ノ( ゜-゜ノ) 
        +=========================================+
        '''
        print(banner)

    async def on_message(self, message):
        """
        Message handling coroutine
        :param message: new message to be handled
        :type message: discord.Message
        :return: None
        """

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
                await save_macros(self, self.macros)
                await message.channel.send(self.macros[ctx.cmd]['Macro'])
