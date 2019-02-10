# -*- coding: utf-8 -*-
"""This module handles creating a log file."""

import logging.config


"""Default logging configuration."""
default_logging_ini = '''[loggers]
keys = root,TBL

[handlers]
keys = TBLHandler, TBLFileHandler

[formatters]
keys = TBLFormatter

[logger_root]
level = CRITICAL
handlers = TBLHandler

[logger_TBL]
level = DEBUG
handlers = TBLHandler, TBLFileHandler
qualname = TBL
propagate = 0

[handler_TBLHandler]
class = StreamHandler
level = DEBUG
formatter = TBLFormatter
args = (sys.stdout,)

[handler_TBLFileHandler]
class = FileHandler
level = DEBUG
formatter = TBLFormatter
args = ('%(logfile)s',)

[formatter_TBLFormatter]
format = %(asctime)s - %(levelname)s - %(message)s
'''


def start_log(client):
    """
    This function checks for a log file and creates one if it doesn't exist.

    :param client: Client object that is starting the log.
    :type client: tbot.Tbot
    :return: Logger object for logging.
    :rtype: logging.Logger
    """
    log_path = client.data_path.joinpath('tbl.log')
    if log_path not in client.data_path.iterdir():
        with log_path.open(mode='w') as fin:
            fin.write('# TBot Log Start!\n')
    ini_path = client.data_path.joinpath('logging.ini')
    if ini_path not in client.data_path.iterdir():
        with ini_path.open(mode='w') as fin:
            fin.write(default_logging_ini)
    logfile = str(log_path).replace('\\', '\\\\')
    try:
        logging.config.fileConfig(ini_path, defaults={'logfile': logfile})
    except TypeError:
        logging.config.fileConfig(str(ini_path), defaults={'logfile': logfile})
    tbl = logging.getLogger('TBL')

    return tbl
