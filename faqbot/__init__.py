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

    def runbot(self) -> None:
        """
        Run bot forever.
        """
        # Initialize command handlers...
        @self.bot.message_handler(func=self.__check_private_chat, commands=['start'])
        def handle_start(message) -> None:
            """
            Handle /start command in private chats.
            :param message: Message, triggered this event.
            """
            try:
                self.bot.send_message(message.chat.id, self.__msgs['fb_welcome'], parse_mode='Markdown')
            except:
                self.__logger.exception(self.__msgs['fb_pmex'])

        @self.bot.message_handler(func=self.__check_owner_feature, commands=['add'])
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
                        self.__logger.warning(
                            self.__msgs['fb_addlog'].format(message.from_user.first_name, message.from_user.id, kw[0]))
                        self.bot.send_message(message.chat.id, self.__msgs['fb_addmsg'].format(kw[0]),
                                              parse_mode='Markdown')
                    else:
                        self.bot.send_message(message.chat.id, self.__msgs['fb_addexists'].format(kw[0]),
                                              parse_mode='Markdown')
                else:
                    self.bot.send_message(message.chat.id, self.__msgs['fb_mlreq'])
            except:
                self.bot.send_message(message.chat.id, self.__msgs['fb_mlreq'])
                self.__logger.exception(self.__msgs['fb_pmex'])

        @self.bot.message_handler(func=self.__check_owner_feature, commands=['alias_add'])
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
                            self.__msgs['fb_alsaddlog'].format(message.from_user.first_name, message.from_user.id,
                                                               kw[1], kw[0]))
                        self.bot.send_message(message.chat.id, self.__msgs['fb_alsaddmsg'].format(kw[1], kw[0]),
                                              parse_mode='Markdown')
                    else:
                        self.bot.send_message(message.chat.id, self.__msgs['fb_addexists'].format(kw[0]),
                                              parse_mode='Markdown')
                else:
                    self.bot.send_message(message.chat.id, self.__msgs['fb_mlreq'])
            except:
                self.bot.send_message(message.chat.id, self.__msgs['fb_mlreq'])
                self.__logger.exception(self.__msgs['fb_pmex'])

        @self.bot.message_handler(func=self.__check_owner_feature, commands=['remove'])
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
                        self.__logger.warning(
                            self.__msgs['fb_remlog'].format(message.from_user.first_name, message.from_user.id,
                                                            swreq.param))
                        self.bot.send_message(message.chat.id, self.__msgs['fb_remmsg'].format(swreq.param),
                                              parse_mode='Markdown')
                    else:
                        self.bot.send_message(message.chat.id, self.__msgs['fb_notexists'].format(swreq.param),
                                              parse_mode='Markdown')
                else:
                    self.bot.send_message(message.chat.id, self.__msgs['fb_mlreq'])
            except:
                self.bot.send_message(message.chat.id, self.__msgs['fb_mlreq'])
                self.__logger.exception(self.__msgs['fb_pmex'])

        @self.bot.message_handler(func=self.__check_owner_feature, commands=['edit'])
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
                            self.__msgs['fb_editlog'].format(message.from_user.first_name, message.from_user.id, kw[0]))
                        self.bot.send_message(message.chat.id, self.__msgs['fb_editmsg'].format(kw[0]),
                                              parse_mode='Markdown')
                    else:
                        self.bot.send_message(message.chat.id, self.__msgs['fb_notexists'].format(kw[0]),
                                              parse_mode='Markdown')
                else:
                    self.bot.send_message(message.chat.id, self.__msgs['fb_mlreq'])
            except:
                self.bot.send_message(message.chat.id, self.__msgs['fb_mlreq'])
                self.__logger.exception(self.__msgs['fb_pmex'])

        @self.bot.message_handler(func=lambda m: True, commands=['faq'])
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
                    msg_text = dbvalue if dbvalue else self.__msgs['fb_notfound']
                    msg_id = message.reply_to_message.message_id if message.reply_to_message else message.message_id
                    self.bot.send_message(message.chat.id, msg_text, reply_to_message_id=msg_id, parse_mode='Markdown')
                else:
                    self.bot.send_message(message.chat.id, self.__msgs['fb_faqlink'].format(self.__settings.faqlink))
            except:
                self.__logger.exception(self.__msgs['fb_faqexpt'])
                self.bot.reply_to(message, self.__msgs['fb_faqerr'])

        # Run bot forever...
        while True:
            try:
                self.bot.polling(none_stop=True)
            except Exception:
                self.__logger.exception(self.__msgs['fb_crashed'])
                time.sleep(30.0)

    def __init__(self) -> None:
        """
        Main constructor of FAQBot class.
        """
        self.__schema = 1
        self.__logger = logging.getLogger(__name__)
        self.__settings = Settings(self.__schema)
        self.__msgs = {
            'fb_welcome': 'Please send me `/faq keyword` command and I will search through my database for you.',
            'fb_notoken': 'No API token found. Cannot proceed. Forward API token using ENV option and try again!',
            'fb_pmex': 'Failed to handle command in private chat with bot.',
            'fb_faqexpt': 'An exception occurred when trying to execute database query.',
            'fb_faqerr': 'Failed to execute your query. Please try again later!',
            'fb_addlog': 'Admin {} ({}) has added a new keyword {} to the database.',
            'fb_alsaddlog': 'Admin {} ({}) has added a new alias {} for the keyword {} to the database.',
            'fb_remlog': 'Admin {} ({}) has removed keyword {} from the database.',
            'fb_editlog': 'Admin {} ({}) has edited the keyword {} in the database.',
            'fb_addmsg': 'The keyword *{}* was added to the database.',
            'fb_alsaddmsg': 'A new alias *{}* for the keyword *{}* was added to the database.',
            'fb_remmsg': 'The keyword *{}* and all its aliases were removed from the database.',
            'fb_editmsg': 'The keyword *{}* was updated in the database.',
            'fb_crashed': 'Bot crashed. Scheduling restart in 30 seconds.',
            'fb_mlreq': 'Failed to execute your query. Please read bot documentation!',
            'fb_notfound': 'Cannot find anything matching the specified keyword in my database!',
            'fb_addexists': 'The *{}* keyword is already exists in our database. No actions will be performed.',
            'fb_notexists': 'The *{}* keyword does not exists in our database. No actions will be performed.',
            'fb_faqlink': 'You will find the answers for the most of questions in our unofficial FAQ: {}'
        }
        if not self.__settings.tgkey:
            raise Exception(self.__msgs['fb_notoken'])
        self.__logger.setLevel(self.__settings.get_logging_level())
        if self.__settings.logtofile:
            f_handler = logging.FileHandler(self.__settings.logtofile)
            f_handler.setFormatter(logging.Formatter(self.__settings.fmtlog))
            self.__logger.addHandler(f_handler)
        else:
            e_handler = logging.StreamHandler(sys.stdout)
            e_handler.setFormatter(logging.Formatter(self.__settings.fmterr))
            self.__logger.addHandler(e_handler)
        self.bot = telebot.TeleBot(self.__settings.tgkey)
        self.__database = FAQDatabase(self.__settings.database_file)
