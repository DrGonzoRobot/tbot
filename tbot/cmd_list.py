# -*- coding: utf-8 -*-
"""The cmd_list module exists to hold a cmds dictionary shared between modules."""

from .bot_utils import test, admin
from .macro_utils import new_macro, list_macros, upvote, downvote

from .profiles import debug_profile


cmds = {'!test': test,
        '!admin': admin,
        '!new': new_macro,
        '!upvote': upvote,
        '!downvote': downvote,
        '!macros': list_macros,
        '!profile': debug_profile}
"""dict: wake words mapped to functions."""
