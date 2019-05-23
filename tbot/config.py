# -*- coding: utf-8 -*-
"""This module creates a configuration file for managing who can use Admin commands."""

import configparser
import logging
from zipfile import ZipFile
import os

tbl = logging.getLogger('TBL')
"""Logger: global Tbot logger for package."""

"""Default configuration if config.ini is not found."""
default_config_ini = '''[VERSION]
Number = 3.5d
Name = TBot Beta Dev

[ROLES]
Admin = 
Banned = 

[BACKUP]
Path = 

[FFMPEG]
Path =
'''


def setup_config(data_path):
    """
    :param data_path: Path for tb_data directory
    :type data_path: pathlib.Path
    :return: config for client to use
    :rtype: configparser.ConfigParser
    """
    config_path = data_path.joinpath('config.ini')
    config = configparser.ConfigParser(interpolation=None)
    if config_path not in data_path.iterdir():
        with config_path.open(mode='w') as fin:
            fin.write(default_config_ini)
            tbl.info('config.ini created.')
    try:
        config.read_file(config_path.open(errors='ignore'))
    except TypeError:
        config.read_file(open(str(config_path), errors='ignore'))

    return config


def setup_backup(start_path, data_path, backup_path):
    with ZipFile(backup_path, 'w') as backup:
        os.chdir(data_path)
        for fname in data_path.iterdir():
            backup.write(os.path.basename(fname))
        os.chdir(start_path)


async def save_backup(start_path, data_path, backup_path):
    with ZipFile(backup_path, 'w') as backup:
        os.chdir(data_path)
        for fname in data_path.iterdir():
            backup.write(os.path.basename(fname))
        os.chdir(start_path)
