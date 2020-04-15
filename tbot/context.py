# -*- coding: utf-8 -*-

import logging

tbl = logging.getLogger('TBL')


class Context:

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

        if any([self.cmd in self.client.cmds,
                self.cmd in self.client.catalog['macros'],
                self.cmd in self.client.catalog['audio']]):
            log = '%s: <%s> %s' % (self.message.author,
                                   self.cmd,
                                   self.line)
            if self.client.config['roles']['admin'] in [role.name for role in self.message.author.roles]:
                log = "(admin) " + log
            log = str("{%s} " % self.message.channel) + log
            tbl.info(log)

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, obj):
        self._client = obj

    @client.deleter
    def client(self):
        del self._client

    @property
    def message(self):
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
        return self._cmd

    @cmd.setter
    def cmd(self, obj):
        self._cmd = obj.content.split(' ')[0]

    @cmd.deleter
    def cmd(self):
        del self._cmd
