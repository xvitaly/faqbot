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


import json
import os
import logging


class Settings:
    @property
    def logtofile(self) -> str:
        """
        Get log file name. If not set or empty, stderr will be used.
        :return: Log file name.
        """
        return self.__data['logtofile']

    @property
    def tgkey(self) -> str:
        """
        Get Telegram Bot API token.
        :return: Bot API token.
        """
        return os.getenv('APIKEY')

    @property
    def admins(self) -> list:
        """
        Get bot admins list. This users can execute any bot command and even
        control supergroups using special bot actions.
        :return: Bot admins list.
        """
        return self.__data['admins']

    @property
    def fmtlog(self) -> str:
        """
        Get custom formatter for file logs.
        :return: Custom formatter for text logs.
        """
        return self.__data['logfilefmt']

    @property
    def faqlink(self) -> str:
        """
        Get FAQ hyperlink.
        :return: FAQ hyperlink.
        """
        return self.__data['faqlink']

    @property
    def fmterr(self) -> str:
        """
        Get custom formatter for stderr (journald) logs.
        :return: Custom formatter for stderr logs.
        """
        return self.__data['stderrfmt']

    @property
    def database_file(self) -> str:
        """
        Get fully-qualified path to SQLite database file.
        :return: Fully-qualified path to main configuration file.
        """
        return str(os.path.join(self.get_cfgpath(), '{}.db'.format(self.__appname)))

    def save(self) -> None:
        """
        Save current settings to JSON file.
        """
        with open(self.__cfgfile, 'w') as f:
            json.dump(self.__data, f)

    def load(self) -> None:
        """
        Load settings from JSON file.
        """
        with open(self.__cfgfile, 'r') as f:
            self.__data = json.load(f)

    def __check_schema(self, schid) -> bool:
        """
        Check JSON config schema version.
        :param schid: New schema version.
        :return: True if equal.
        """
        return self.__data['schema'] >= schid

    def get_cfgpath(self) -> str:
        """
        Get directory where bot's configuration are stored.
        User can override this setting by exporting CFGPATH
        environment option.
        :return: Full directory path.
        """
        cfgpath = os.getenv('CFGPATH')
        if cfgpath:
            if os.path.exists(cfgpath):
                return cfgpath
        return os.path.join('/etc' if os.name == 'posix' else os.getenv('APPDATA'), self.__appname)

    @staticmethod
    def get_logging_level() -> int:
        """
        Get current log level. User can override this setting by exporting
        LOGLEVEL environment option.
        :return: Log level.
        """
        try:
            loglevel = os.getenv("LOGLEVEL")
            if loglevel:
                return getattr(logging, loglevel)
        except Exception:
            pass
        return logging.INFO

    def __find_cfgfile(self) -> None:
        """
        Get fully-qualified path to main configuration file.
        """
        self.__cfgfile = str(os.path.join(self.get_cfgpath(), '{}.json'.format(self.__appname)))

    def __init__(self, schid) -> None:
        """
        Main constructor of Settings class.
        :param schid: Required schema version.
        """
        self.__appname = 'faqbot'
        self.__data = {}
        self.__find_cfgfile()
        if not os.path.isfile(self.__cfgfile):
            raise Exception('Cannot find JSON config {}! Create it using sample from repo.'.format(self.__cfgfile))
        self.load()
        if not self.__check_schema(schid):
            raise Exception('Schema of JSON config {} is outdated! Update config from repo.'.format(self.__cfgfile))
