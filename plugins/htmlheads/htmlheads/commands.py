#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from outwiker.pages.wiki.parser.command import Command


class TitleCommand (Command):
    """
    Команда для вставки тега <title>
    """
    def __init__ (self, parser):
        """
        parser - экземпляр парсера
        """
        Command.__init__ (self, parser)


    @property
    def name (self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return u"title"


    def execute (self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место команды в вики-нотации
        """
        title = u"<title>{}</title>".format (params)
        self.parser.appendToHead (title)
        return u""