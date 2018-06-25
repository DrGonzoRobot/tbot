# tbot

Tbot is a very simple Discord bot using discord.py.
Meant for small servers with friends, tbot allows for the creation
of macros and commands that are easy to create, manage, and use.

## Dependencies

Tbot only uses Python 3.6 and the "rewrite" branch of discord.py, 
so you'll need to install Python 3.6 for your platfrom and 
discord.py@rewrite from GitHub:

```
pip install git+https://github.com/Rapptz/discord.py.git@rewrite
```

or if you don't have git, and you're installing from a downloaded zip

```
pip install discord.py-rewrite.zip
```

## A Bot Script

You will need to create a script to start your bot, like so:

```py
from tbot import TBot, get_token

bot = TBot()
bot.run(get_token('token.txt'))
```

You can put your token into the run method as a string or use get_token
from the module to parse it from a plain text file only containing the token.
