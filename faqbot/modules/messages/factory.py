# coding=utf-8

# FAQ bot for Telegram Messenger
# Copyright (c) 2019 - 2020 EasyCoding Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


class FAQMessagesFactory:
    def add_language(self, lang, handler):
        self.__handlers[lang] = handler

    def get_language(self, lang):
        producer = self.__handlers.get(lang)
        if not producer:
            return self.__handlers.get('en')
        return producer()

    def __init__(self):
        self.__handlers = {}
