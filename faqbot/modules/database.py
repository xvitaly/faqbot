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

import os
import sqlite3


class FAQDatabase:
    def get_value(self, keyword: str) -> str:
        """
        Get value from database by the specified keyword.
        :param keyword: Keyword to search.
        :return: Value from database.
        """
        cursor = self.__connection.cursor()
        cursor.execute('SELECT "Values"."Data" FROM "Keys" INNER JOIN "Values" ON "Values"."ID" = "Keys"."ExtValue"'
                       'WHERE "Keys"."Keyword" = ?', (keyword,))
        return cursor.fetchone()

    def check_exists(self, keyword: str) -> bool:
        """
        Check if the specified keyword exists in database.
        :param keyword: Keyword to check.
        :return: Return True if exists.
        """
        cursor = self.__connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM "Keys" WHERE "Keys"."Keyword"=?', (keyword,))
        return cursor.fetchone() > 0

    def __get_internal_id(self, keyword: str) -> int:
        """
        Get an internal ID of data.
        :param keyword: Keyword to check.
        :return: Internal id.
        """
        cursor = self.__connection.cursor()
        cursor.execute('SELECT "Keys"."ExtValue" FROM "Keys" WHERE "Keys"."Keyword"=?', (keyword,))
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

    def __connect_to_database(self) -> None:
        """
        Create a database connection.
        """
        self.__connection = sqlite3.connect(self.__dbfile, check_same_thread=False)

    def __create_database_file(self) -> None:
        """
        Create an empty database file on disk.
        """
        with open(self.__dbfile, 'w'):
            pass

    def __create_database_and_connect(self) -> None:
        """
        Create an empty database, add required tables and than create a
        database connection as required.
        """
        self.__create_database_file()
        self.__connect_to_database()
        cursor = self.__connection.cursor()
        cursor.execute('CREATE TABLE "Values" ("ID" INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, "Data" TEXT NOT NULL);')
        cursor.execute('CREATE TABLE "Keys" ("ID" INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, "Keyword" TEXT NOT NULL UNIQUE, "ExtValue" INTEGER, FOREIGN KEY("ExtValue") REFERENCES "Values"("ID"));')

    def __init__(self, dbfile: str) -> None:
        """
        Main constructor of FAQDatabase class.
        :param dbfile: Full path to SQLite database file.
        """
        self.__dbfile = dbfile
        if os.path.isfile(self.__dbfile):
            self.__connect_to_database()
        else:
            self.__create_database_and_connect()

    def __del__(self) -> None:
        """
        Main destructor of FAQDatabase class.
        """
        self.__connection.close()
