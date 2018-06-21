# -*- coding: utf-8 -*-


class Context:
    def __init__(self, client, message):
        self.__slots__ = ['client', 'message', 'line', 'cmd']

        self.client = client
        self.message = message
        self.line = self._get_line(message)
        self.cmd = message.content.split(' ')[0]

    @staticmethod
    def _get_line(message):
        line = message.content.split(' ')
        if len(line) <= 1:
            return []

        return line[1:]
