# -*- coding: utf-8 -*-
"""This module contains the TBot class which inherits from discord.Client."""

from discord import Client
from .context import Context
from .cmd_list import cmds
from .logs import start_log
from .config import setup_config, save_backup
from .profiles import setup_profiles
from .audio import setup_audio_config, play_clip
from .macro_utils import setup_macros, save_macros
from .bot_utils import debug_message
from .profiles import get_profile, save_profile, get_all_profiles
import logging
import sys
import os
import platform
import asyncio
from pathlib import Path, WindowsPath, PosixPath
import importlib.util as iu
import distutils.spawn
import random


class TBot(Client):
    """This is the main client class."""

    def __init__(self,
                 data_path=None,
                 backup_path=None,
                 clips_path=None,
                 ffmpeg_path=None,
                 debug=False):
        """
        :param data_path: (Optional) Absolute path string to a tb_data directory
        :type data_path: str or None
        """
        super(TBot, self).__init__()

        self._start_path = None
        self.start_path = sys.argv[0]

        self._data_path = None
        self.data_path = data_path

        self._backup_path = None
        self.backup_path = backup_path

        self._clips_path = None
        self.clips_path = clips_path

        start_log(self)
        
        self._tbl = None
        self.tbl = logging.getLogger('TBL')
        self.tbl.info('Logging started.')

        self._config = None
        self.config = setup_config(self.data_path)

        self._audio_config = None
        self.audio_config = setup_audio_config(self.data_path)

        self._ffmpeg_path = None
        self.ffmpeg_path = ffmpeg_path

        self._voice = None
        self.voice = None

        self._macros = None
        self.macros = setup_macros(self.data_path)

        self.tbl.info('Config loaded.')

        self._roles = None
        self.roles = self.config['ROLES']
        self.tbl.info('Roles loaded.')

        self._profiles = None
        self.profiles = setup_profiles(self.data_path)
        self.tbl.info('Profiles loaded.')

        self._cmds = None
        self.cmds = cmds
        self.tbl.info('Commands loaded.')

        self.debug = debug

        self.get_profile = get_profile
        self.save_profile = save_profile
        self.get_all_profiles = get_all_profiles

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

    @property
    def backup_path(self):
        return self._backup_path

    @backup_path.setter
    def backup_path(self, path):
        if path is not None:
            if path[-4:] != '.zip':
                path += '.zip'
            self._backup_path = Path(path)

    @property
    def clips_path(self):
        """
        Path where tb_data is located
        :return: clips_path
        :rtype: pathlib.Path
        """
        return self._clips_path

    @clips_path.setter
    def clips_path(self, path):
        if path is None:
            path = self._data_path.joinpath('clips')
            if path not in self._data_path.iterdir():
                path.mkdir()
        self._clips_path = Path(path)

    @property
    def ffmpeg_path(self):
        return self._ffmpeg_path

    @ffmpeg_path.setter
    def ffmpeg_path(self, path):
        if path:
            if platform.system() == "Windows":
                path = str(WindowsPath(path))
            elif platform.system() == "Linux":
                path = str(PosixPath(path))

            if distutils.spawn.find_executable(path):
                self.config['FFMPEG']['Path'] = path
                self._ffmpeg_path = path

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

    @property
    def profiles(self):
        return self._profiles

    @profiles.setter
    def profiles(self, obj):
        self._profiles = obj

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

    @property
    def audio_config(self):
        """
        Tbot config file
        :return: audio_config
        :rtype: configparser.ConfigParser
        """
        return self._audio_config

    @audio_config.setter
    def audio_config(self, obj):
        self._audio_config = obj

    @property
    def voice(self):
        return self._voice

    @voice.setter
    def voice(self, obj):
        self._voice = obj

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

    async def on_ready(self):
        banner = '''
        +=========================================+
        (╯°□°）╯︵ ┻━┻ [  TB v4.3  ] ┬─┬ ノ( ゜-゜ノ) 
        +=========================================+
        '''
        print(banner)

        if self.backup_path:
            while True:
                await save_backup(self.start_path, self.data_path, self.backup_path)
                await asyncio.sleep(60)

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

        elif message.content.startswith('%'):
            if ctx.cmd in self.macros:
                self.tbl.info('%s: %s' % (str(message.author), message.content))
                cnt = self.macros[ctx.cmd]['Count']
                self.macros[ctx.cmd]['Count'] = str(int(cnt) + 1)
                await save_macros(self, self.macros)
                await message.channel.send(self.macros[ctx.cmd]['Macro'])

        elif message.content.startswith('&'):
            if not self.ffmpeg_path:
                await message.channel.send('Audio is not configured for this bot.')
                return
            self.tbl.info('%s: %s' % (str(message.author), message.content))
            clip = None
            if ctx.cmd == "&random":
                clips = [clip for clip in self.audio_config.keys() if str(clip) != "DEFAULT"]
                clip = random.choice(clips)
                clip = self.audio_config[clip]['Clip']
            if ctx.cmd in self.audio_config:
                clip = self.audio_config[ctx.cmd]['Clip']
            if clip:
                await message.channel.send(clip)
                await play_clip(ctx, self.clips_path, clip)

        if self.debug:
            debug_message(ctx)
