# -*- coding: utf-8 -*-
"""This module creates a configuration file for managing who can use Admin commands."""

import configparser
import logging

tbl = logging.getLogger('TBL')
"""Logger: global Tbot logger for package."""

"""Default configuration if config.ini is not found."""
default_config_ini = '''[VERSION]
Number = 3.5d
Name = TBot Beta Dev

[ROLES]
Admin = 
Banned = 
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
        config.read(config_path, encoding='utf-8')
    except TypeError:
        config.read(str(config_path), encoding='utf-8')

    return config
