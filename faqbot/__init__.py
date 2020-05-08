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

    def __get_actual_username(self, message) -> str:
        """
        Get a real username of current message's sender.
        :param message: Message to check.
        :return: Real username.
        """
        return message.reply_to_message.new_chat_member.first_name if message.reply_to_message.new_chat_member else message.reply_to_message.from_user.first_name

    def __get_actual_userid(self, message) -> str:
        """
        Get a real ID of current message's sender.
        :param message: Message to check.
        :return: Real ID.
        """
        return message.reply_to_message.new_chat_member.id if message.reply_to_message.new_chat_member else message.reply_to_message.from_user.id

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
                self.bot.send_message(message.chat.id, self.__msgs['fb_swuadd'].format(swreq.param))
            except:
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
                self.bot.send_message(message.chat.id, self.__msgs['fb_swurem'].format(swreq.param))
            except:
                self.__logger.exception(self.__msgs['fb_pmex'])

        @self.bot.message_handler(func=self.__check_owner_feature, commands=['edit'])
        def handle_edit(message) -> None:
            """
            Handle /edit command in private chats. Allow admins to edit keyword's
            description from the main database. Restricted command.
            :param message: Message, triggered this event.
            """
            try:
                self.bot.send_message(message.chat.id, 'list')
            except:
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
                dbvalue = self.__database.get_value(swreq.param)
                msg_text = dbvalue if dbvalue else self.__msgs['fb_notfound']
                msg_id = message.reply_to_message.message_id if message.reply_to_message else message.message_id
                self.bot.send_message(message.chat.id, msg_text, reply_to_message_id=msg_id, parse_mode='Markdown')
            except:
                self.__logger.exception(self.__msgs['fb_pmex'])
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
            'fb_faqerr': 'Failed to execute your query. Please try again later!',
            'fb_swadd': 'Admin {} ({}) added new keyword {} to database.',
            'fb_swrem': 'Admin {} ({}) removed keyword {} from database.',
            'fb_swuadd': 'New keyword {} added to database.',
            'fb_swurem': 'Keyword {} removed from database.',
            'fb_swerr': 'Failed to add/remove keyword. Try again later.',
            'fb_swpm': 'You must specify a keyword to add/remove. Fix this and try again.',
            'fb_crashed': 'Bot crashed. Scheduling restart in 30 seconds.',
            'fb_notfound': 'Cannot find anything matching the specified keyword in my database!'
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
