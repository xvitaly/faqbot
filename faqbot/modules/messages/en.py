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

from typing import Dict, Union


class FAQMessagesEn:
    __messages: Dict[Union[str, str], Union[str, str]] = {
        'fb_welcome': 'Please send me `/faq keyword` command and I will search through my database for you.',
        'fb_notoken': 'No API token found. Cannot proceed. Forward API token using ENV option and try again!',
        'fb_pmex': 'Failed to handle command in private chat with bot.',
        'fb_faqexpt': 'An exception occurred when trying to execute database query.',
        'fb_faqerr': 'Failed to execute your query. Please try again later!',
        'fb_addlog': 'Admin {} ({}) has added a new keyword {} to the database.',
        'fb_alsaddlog': 'Admin {} ({}) has added a new alias {} for the keyword {} to the database.',
        'fb_remlog': 'Admin {} ({}) has removed keyword {} from the database.',
        'fb_alsremlog': 'Admin {} ({}) has removed alias {} from the database.',
        'fb_editlog': 'Admin {} ({}) has edited the keyword {} in the database.',
        'fb_addmsg': 'The keyword *{}* was added to the database.',
        'fb_alsaddmsg': 'A new alias *{}* for the keyword *{}* was added to the database.',
        'fb_remmsg': 'The keyword *{}* and all its aliases were removed from the database.',
        'fb_alsremmsg': 'The alias *{}* was removed from the database.',
        'fb_editmsg': 'The keyword *{}* was updated in the database.',
        'fb_crashed': 'Bot crashed. Scheduling restart in 30 seconds.',
        'fb_mlreq': 'Failed to execute your query. Please read bot documentation!',
        'fb_notfound': 'Cannot find anything matching the specified keyword in my database!',
        'fb_listkw': 'Available keywords: {}.',
        'fb_addexists': 'The *{}* keyword is already exists in our database. No actions will be performed.',
        'fb_notexists': 'The *{}* keyword does not exists in our database. No actions will be performed.',
        'fb_faqlink': 'You will find the answers for the most of questions in our unofficial FAQ: {}'
    }

    def get_message(self, key: str) -> str:
        """
        Get message depends on the specified language.
        :param key: Message key.
        :return: Localized string.
        """
        return self.__messages[key]
