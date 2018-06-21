# -*- coding: utf-8 -*-

from .bot_utils import test
from .macro_utils import new_macro, list_macros, upvote, downvote


cmds = {'!test': test,
        '!new': new_macro,
        '!upvote': upvote,
        '!downvote': downvote,
        '!macros': list_macros}
