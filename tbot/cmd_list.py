# -*- coding: utf-8 -*-
"""The cmd_list module exists to hold a cmds dictionary shared between modules."""

from .bot_utils import test
from .macro_utils import new_macro, list_macros, upvote, downvote


cmds = {'!test': test,
        '!new': new_macro,
        '!upvote': upvote,
        '!downvote': downvote,
        '!macros': list_macros}
"""dict: wake words mapped to functions."""
