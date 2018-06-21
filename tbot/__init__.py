# -*- coding: utf-8 -*-

from .client import TBot
from .context import Context

from .config import setup_config
from .logs import start_log

from .bot_utils import get_token, test
from .macro_utils import new_macro, list_macros

from .cmd_list import cmds