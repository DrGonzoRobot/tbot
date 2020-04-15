# -*- coding: utf-8 -*-

from .bot_utils import test, admin
from .catalog import save
from .badges import brag

CMDS = {'!test': test,
        '!save': save,
        '!admin': admin,
        '!brag': brag,
        '!badges': brag}
