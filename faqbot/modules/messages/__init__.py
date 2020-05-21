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

from .factory import FAQMessagesFactory
from .en import FAQMessagesEn
from .ru import FAQMessagesRu


class FAQMessages:
    def __init_factory(self) -> None:
        """
        Create the factory instance.
        """
        self.__factory = FAQMessagesFactory()

    def __add_languages(self) -> None:
        """
        Create the language mapping for the factory.
        """
        self.__factory.add_language('en', FAQMessagesEn)
        self.__factory.add_language('ru', FAQMessagesRu)
        self.__factory.add_language('uk', FAQMessagesRu)
        self.__factory.add_language('be', FAQMessagesRu)
        self.__factory.add_language('kk', FAQMessagesRu)

    def get_message(self, key: str, lang: str = 'en') -> str:
        """
        Get message depends on the specified language.
        :param key: Message key.
        :param lang: Required language (EN as a fallback).
        :return: Localized string.
        """
        return self.__factory.get_language(lang).get_message(key)

    def __init__(self) -> None:
        """
        Main constructor of the FAQMessages class.
        """
        self.__init_factory()
        self.__add_languages()
