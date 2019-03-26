# tbot

Tbot is a very simple Discord bot using discord.py.
Meant for small servers with friends, tbot allows for the creation
of macros and commands that are easy to create, manage, and use.

## A Bot Script

You will need to create a script to start your bot, like so:

```py
from tbot import TBot, get_token

bot = TBot()
bot.run(get_token('token.txt'))
```

You can put your token into the run method as a string or use get_token
from the module to parse it from a plain text file only containing the token.
