# -*- coding: utf-8 -*-

import configparser
import logging
from configparser import ConfigParser

tbl = logging.getLogger('TBL')

default_config_ini = '''[VERSION]
Number = 3.5b
Name = TBot Beta Dev

[ROLES]
Admin = 
Banned = 

[BACKUP]
FilePath =
'''


def setup_config(data_path):
    config_path = data_path.joinpath('config.ini')
    config = configparser.ConfigParser(interpolation=None)
    if config_path not in data_path.iterdir():
        with config_path.open(mode='w') as fin:
            fin.write(default_config_ini)
            tbl.info('config.ini created.')
    config.read(config_path, encoding='utf-8')

    return config
