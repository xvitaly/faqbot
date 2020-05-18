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

import logging
import sys
import time
import telebot

from .modules.helpers import ParamExtractor
from .modules.database import FAQDatabase
from .modules.messages import FAQMessages
from .settings import Settings


class FAQBot:
    def __check_owner_feature(self, message) -> bool:
        """
        Check if message was sent by bot admin in private chat.
        :param message: Message to check.
        :return: Check results.
        """
        return message.chat.type == 'private' and message.from_user.id in self.__settings.admins

    def __check_private_chat(self, message) -> bool:
        """
        Check if message was sent in private chat.
        :param message: Message to check.
        :return: Check results.
        """
        return message.chat.type == 'private'

    def __extract_value(self, source: str) -> tuple:
        """
        Get a keyword and its value from the source string.
        :param source: Source string.
        :return: Tuple with keyword and its value.
        """
        index = source.index(' ')
        return source[:index], source[index + 1:]

    def __load_messages(self) -> None:
        """
        Create an instance of FAQMessages class.
        """
        self.__messages = FAQMessages()

    def __read_settings(self) -> None:
        """
        Read settings from JSON configuration file.
        """
        self.__schema = 1
        self.__settings = Settings(self.__schema)
        if not self.__settings.tgkey:
            raise Exception(self.__messages.get_message('fb_notoken', self.__settings.language))

    def __set_logger(self) -> None:
        """
        Set logger engine.
        """
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(self.__settings.get_logging_level())
        if self.__settings.logtofile:
            f_handler = logging.FileHandler(self.__settings.logtofile)
            f_handler.setFormatter(logging.Formatter(self.__settings.fmtlog))
            self.__logger.addHandler(f_handler)
        else:
            e_handler = logging.StreamHandler(sys.stdout)
            e_handler.setFormatter(logging.Formatter(self.__settings.fmterr))
            self.__logger.addHandler(e_handler)

    def __init_bot(self) -> None:
        """
        Initialize internal bot engine by creating an instance
        of TeleBot class.
        """
        self.__bot = telebot.TeleBot(self.__settings.tgkey)

    def __init_database(self) -> None:
        """
        Establish connection to the database by creating an
        instance of FAQDatabase class.
        """
        self.__database = FAQDatabase(self.__settings.database_file)

    def runbot(self) -> None:
        """
        Run bot forever.
        """
        # Initialize command handlers...
        @self.__bot.message_handler(func=self.__check_private_chat, commands=['start'])
        def handle_start(message) -> None:
            """
            Handle /start command in private chats.
            :param message: Message, triggered this event.
            """
            try:
                self.__bot.send_message(message.chat.id,
                                      self.__messages.get_message('fb_welcome', message.from_user.language_code),
                                      parse_mode='Markdown')
            except:
                self.__logger.exception(self.__messages.get_message('fb_pmex', self.__settings.language))

        @self.__bot.message_handler(func=self.__check_owner_feature, commands=['add'])
        def handle_add(message) -> None:
            """
            Handle /add command in private chats. Allow admins to add a new
            keyword to the main database. Restricted command.
            :param message: Message, triggered this event.
            """
            try:
                swreq = ParamExtractor(message.text)
                if swreq.index > 0:
                    kw = self.__extract_value(swreq.param)
                    if not self.__database.check_exists(kw[0]):
                        self.__database.add_value(kw[0], kw[1])
                        self.__logger.warning(self.__messages.get_message('fb_addlog', self.__settings.language).format(
                            message.from_user.first_name, message.from_user.id, kw[0]))
                        self.__bot.send_message(message.chat.id, self.__messages.get_message('fb_addmsg', message.from_user.language_code).format(kw[0]), parse_mode='Markdown')
                    else:
                        self.__bot.send_message(message.chat.id, self.__messages.get_message('fb_addexists', message.from_user.language_code).format(kw[0]), parse_mode='Markdown')
                else:
                    self.__bot.send_message(message.chat.id, self.__messages.get_message('fb_mlreq', message.from_user.language_code))
            except:
                self.__bot.send_message(message.chat.id, self.__messages.get_message('fb_mlreq', message.from_user.language_code))
                self.__logger.exception(self.__messages.get_message('fb_pmex', self.__settings.language))

        @self.__bot.message_handler(func=self.__check_owner_feature, commands=['alias_add'])
        def handle_alias_add(message) -> None:
            """
            Handle /alias_add command in private chats. Allow admins to add a new
            alias to existing entry in the main database. Restricted command.
            :param message: Message, triggered this event.
            """
            try:
                swreq = ParamExtractor(message.text)
                if swreq.index > 0:
                    kw = self.__extract_value(swreq.param)
                    if self.__database.check_exists(kw[0]) and not self.__database.check_exists(kw[1]):
                        self.__database.add_alias(kw[0], kw[1])
                        self.__logger.warning(
                            self.__messages.get_message('fb_alsaddlog', self.__settings.language).format(
                                message.from_user.first_name, message.from_user.id, kw[1], kw[0]))
                        self.__bot.send_message(message.chat.id, self.__messages.get_message('fb_alsaddmsg', message.from_user.language_code).format(kw[1], kw[0]), parse_mode='Markdown')
                    else:
                        self.__bot.send_message(message.chat.id, self.__messages.get_message('fb_addexists', message.from_user.language_code).format(kw[0]), parse_mode='Markdown')
                else:
                    self.__bot.send_message(message.chat.id, self.__messages.get_message('fb_mlreq', message.from_user.language_code))
            except:
                self.__bot.send_message(message.chat.id, self.__messages.get_message('fb_mlreq', message.from_user.language_code))
                self.__logger.exception(self.__messages.get_message('fb_pmex', self.__settings.language))

        @self.__bot.message_handler(func=self.__check_owner_feature, commands=['remove'])
        def handle_remove(message) -> None:
            """
            Handle /remove command in private chats. Allow admins to remove
            keyword from the main database. Restricted command.
            :param message: Message, triggered this event.
            """
            try:
                swreq = ParamExtractor(message.text)
                if swreq.index > 0:
                    if self.__database.check_exists(swreq.param):
                        self.__database.remove_value(swreq.param)
                        self.__logger.warning(self.__messages.get_message('fb_remlog', self.__settings.language).format(
                            message.from_user.first_name, message.from_user.id, swreq.param))
                        self.__bot.send_message(message.chat.id, self.__messages.get_message('fb_remmsg', message.from_user.language_code).format(swreq.param), parse_mode='Markdown')
                    else:
                        self.__bot.send_message(message.chat.id, self.__messages.get_message('fb_notexists', message.from_user.language_code).format(swreq.param), parse_mode='Markdown')
                else:
                    self.__bot.send_message(message.chat.id, self.__messages.get_message('fb_mlreq', message.from_user.language_code))
            except:
                self.__bot.send_message(message.chat.id, self.__messages.get_message('fb_mlreq', message.from_user.language_code))
                self.__logger.exception(self.__messages.get_message('fb_pmex', self.__settings.language))

        @self.__bot.message_handler(func=self.__check_owner_feature, commands=['alias_remove'])
        def handle_alias_remove(message) -> None:
            """
            Handle /alias_remove command in private chats. Allow admins to remove
            aliases from the main database. Restricted command.
            :param message: Message, triggered this event.
            """
            try:
                swreq = ParamExtractor(message.text)
                if swreq.index > 0:
                    if self.__database.check_exists(swreq.param):
                        self.__database.remove_alias(swreq.param)
                        self.__logger.warning(
                            self.__messages.get_message('fb_alsremlog', self.__settings.language).format(
                                message.from_user.first_name, message.from_user.id, swreq.param))
                        self.__bot.send_message(message.chat.id, self.__messages.get_message('fb_alsremmsg', message.from_user.language_code).format(swreq.param), parse_mode='Markdown')
                    else:
                        self.__bot.send_message(message.chat.id, self.__messages.get_message('fb_notexists', message.from_user.language_code).format(swreq.param), parse_mode='Markdown')
                else:
                    self.__bot.send_message(message.chat.id, self.__messages.get_message('fb_mlreq', message.from_user.language_code))
            except:
                self.__bot.send_message(message.chat.id, self.__messages.get_message('fb_mlreq', message.from_user.language_code))
                self.__logger.exception(self.__messages.get_message('fb_pmex', self.__settings.language))

        @self.__bot.message_handler(func=self.__check_owner_feature, commands=['edit'])
        def handle_edit(message) -> None:
            """
            Handle /edit command in private chats. Allow admins to edit keyword's
            description from the main database. Restricted command.
            :param message: Message, triggered this event.
            """
            try:
                swreq = ParamExtractor(message.text)
                if swreq.index > 0:
                    kw = self.__extract_value(swreq.param)
                    if self.__database.check_exists(kw[0]):
                        self.__database.set_value(kw[0], kw[1])
                        self.__logger.warning(
                            self.__messages.get_message('fb_editlog', self.__settings.language).format(
                                message.from_user.first_name, message.from_user.id, kw[0]))
                        self.__bot.send_message(message.chat.id, self.__messages.get_message('fb_editmsg', message.from_user.language_code).format(kw[0]), parse_mode='Markdown')
                    else:
                        self.__bot.send_message(message.chat.id, self.__messages.get_message('fb_notexists', message.from_user.language_code).format(kw[0]), parse_mode='Markdown')
                else:
                    self.__bot.send_message(message.chat.id, self.__messages.get_message('fb_mlreq', message.from_user.language_code))
            except:
                self.__bot.send_message(message.chat.id, self.__messages.get_message('fb_mlreq', message.from_user.language_code))
                self.__logger.exception(self.__messages.get_message('fb_pmex', self.__settings.language))

        @self.__bot.message_handler(func=self.__check_owner_feature, commands=['list'])
        def handle_list(message) -> None:
            """
            Handle /list command in private chats. Allow admins to retrieve the
            full list of keywords from the main database. Restricted command.
            :param message: Message, triggered this event.
            """
            try:
                kwlist = ', '.join(self.__database.list_keywords())
                self.__bot.send_message(message.chat.id, self.__messages.get_message('fb_listkw', message.from_user.language_code).format(kwlist))
            except:
                self.__bot.send_message(message.chat.id, self.__messages.get_message('fb_mlreq', message.from_user.language_code))
                self.__logger.exception(self.__messages.get_message('fb_pmex', self.__settings.language))

        @self.__bot.message_handler(func=lambda m: True, commands=['faq'])
        def handle_faq(message):
            """
            Handle /faq command in any chats. Search for the specified
            keyword in the main database. Public command.
            :param message: Message, triggered this event.
            """
            try:
                swreq = ParamExtractor(message.text)
                if swreq.index > 0:
                    dbvalue = self.__database.get_value(swreq.param)
                    msg_text = dbvalue if dbvalue else self.__messages.get_message('fb_notfound', message.from_user.language_code)
                    msg_id = message.reply_to_message.message_id if message.reply_to_message else message.message_id
                    self.__bot.send_message(message.chat.id, msg_text, reply_to_message_id=msg_id, parse_mode='Markdown')
                else:
                    self.__bot.send_message(message.chat.id, self.__messages.get_message('fb_faqlink', message.from_user.language_code).format(self.__settings.faqlink))
            except:
                self.__logger.exception(self.__messages.get_message('fb_faqexpt', self.__settings.language))
                self.__bot.reply_to(message, self.__messages.get_message('fb_faqerr', message.from_user.language_code))

        # Run bot forever...
        while True:
            try:
                self.__bot.polling(none_stop=True)
            except Exception:
                self.__logger.exception(self.__messages.get_message('fb_crashed', self.__settings.language))
                time.sleep(30.0)

    def __init__(self) -> None:
        """
        Main constructor of FAQBot class.
        """
        self.__load_messages()
        self.__read_settings()
        self.__set_logger()
        self.__init_bot()
        self.__init_database()
