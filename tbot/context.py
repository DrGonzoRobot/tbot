# -*- coding: utf-8 -*-
"""This module contains the Context class for handling commands."""


class Context:
    """A context object is created when a command message is read
    and is meant to be passed to the function for that command."""

    def __init__(self, client, message):
        self.__slots__ = ['client', 'message', 'line', 'cmd']

        self._client = None
        self.client = client

        self._message = None
        self.message = message

        self._line = None
        self.line = message

        self._cmd = None
        self.cmd = message

    @property
    def client(self):
        """
        :return: Client creating the Context object.
        :rtype: tbot.Tbot
        """
        return self._client

    @client.setter
    def client(self, obj):
        self._client = obj

    @client.deleter
    def client(self):
        del self._client

    @property
    def message(self):
        """
        :return: Message object containing command.
        :rtype: discord.Message
        """
        return self._message

    @message.setter
    def message(self, obj):
        self._message = obj

    @message.deleter
    def message(self):
        del self._message

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, obj):
        """
        :return: List containing message contents that come after command.
        :rtype: list
        """
        def _get_line(message):
            line = message.content.split(' ')
            if len(line) <= 1:
                return []
            return line[1:]

        self._line = _get_line(obj)

    @line.deleter
    def line(self):
        del self._line

    @property
    def cmd(self):
        """
        :return: String for command from message.
        :rtype: str
        """
        return self._cmd

    @cmd.setter
    def cmd(self, obj):
        self._cmd = obj.content.split(' ')[0]

    @cmd.deleter
    def cmd(self):
        del self._cmd
