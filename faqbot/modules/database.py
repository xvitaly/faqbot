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

import sqlite3


class FAQDatabase:
    def get_value(self, keyword: str) -> str:
        """
        Get value from database by the specified keyword.
        :param keyword: Keyword to search.
        :return: Value from database.
        """
        cursor = self.__connection.cursor()
        cursor.execute('SELECT "Values"."Data" FROM "Meta" INNER JOIN "Values" ON "Values"."ID" = "Meta"."ExtValue"'
                       'WHERE "Meta"."Keyword" = ?', (keyword,))
        return cursor.fetchone()

    def check_exists(self, keyword: str) -> bool:
        """
        Check if the specified keyword exists in database.
        :param keyword: Keyword to check.
        :return: Return True if exists.
        """
        cursor = self.__connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM "Meta" WHERE "Meta"."Keyword"=?', (keyword,))
        return cursor.fetchone() > 0

    def __get_internal_id(self, keyword: str) -> int:
        """
        Get an internal ID of data.
        :param keyword: Keyword to check.
        :return: Internal id.
        """
        cursor = self.__connection.cursor()
        cursor.execute('SELECT "Meta"."ExtValue" FROM "Meta" WHERE "Meta"."Keyword"=?', (keyword,))
        return int(cursor.fetchone())

    def __set_value(self, keyword: str, new_value: str) -> None:
        """
        Set value for the specified keyword. Private method.
        :param keyword: Keyword to operate with.
        :param new_value: New value.
        """
        cursor = self.__connection.cursor()
        cursor.execute('UPDATE Keywords SET Description=? WHERE Keyword=?', (new_value, keyword))

    def __add_value(self, keyword: str, new_value: str) -> None:
        """
        Add a new value for the specified keyword. Private method.
        :param keyword: Keyword to operate with.
        :param new_value: New value.
        """
        cursor = self.__connection.cursor()
        cursor.execute('INSERT INTO Keywords (ID, Keyword, Description) VALUES (NULL, ?, ?)', (keyword, new_value))

    def set_value(self, keyword: str, new_value: str) -> None:
        """
        Set value for the specified keyword.
        :param keyword: Keyword to operate with.
        :param new_value: New value.
        """
        if self.check_exists(keyword):
            self.__set_value(keyword, new_value)
        else:
            self.__add_value(keyword, new_value)

    def remove_value(self, keyword: str) -> None:
        """
        Remove keyboard from the database.
        :param keyword: Keyword to operate with.
        """
        cursor = self.__connection.cursor()
        cursor.execute('DELETE FROM Keywords WHERE Keyword=?', (keyword,))

    def __init__(self, dbfile: str) -> None:
        """
        Main constructor of FAQDatabase class.
        :param dbfile: Full path to SQLite database file.
        """
        self.__connection = sqlite3.connect(dbfile, check_same_thread=False)
