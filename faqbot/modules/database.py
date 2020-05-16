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
                       'WHERE "Keys"."Keyword" = ?;', (keyword,))
        return cursor.fetchone()

    def check_exists(self, keyword: str) -> bool:
        """
        Check if the specified keyword exists in database.
        :param keyword: Keyword to check.
        :return: Return True if exists.
        """
        cursor = self.__connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM "Keys" WHERE "Keys"."Keyword" = ?;', (keyword,))
        return cursor.fetchone()[0] > 0

    def __get_internal_id(self, keyword: str) -> int:
        """
        Get an internal ID of data.
        :param keyword: Keyword to check.
        :return: Internal id.
        """
        cursor = self.__connection.cursor()
        cursor.execute('SELECT "Keys"."ExtValue" FROM "Keys" WHERE "Keys"."Keyword" = ?;', (keyword,))
        result = cursor.fetchone()
        if not result:
            raise Exception('The required keyword does not exists in the database.')
        return int(result[0])

    def __set_value(self, keyword: str, new_value: str) -> None:
        """
        Set value for the specified keyword. Private method.
        :param keyword: Keyword to operate with.
        :param new_value: New value.
        """
        cursor = self.__connection.cursor()
        cursor.execute('UPDATE "Values" SET "Data" = ? WHERE "ID" = ?;', (new_value, self.__get_internal_id(keyword)))

    def __add_value(self, keyword: str, value: str) -> None:
        """
        Add a new value for the specified keyword. Private method.
        :param keyword: Keyword to operate with.
        :param value: New value.
        """
        cursor = self.__connection.cursor()
        cursor.execute('INSERT INTO "Values" ("ID", "Data") VALUES (NULL, ?);', (value,))
        cursor.execute('INSERT INTO "Keys" ("ID", "Keyword", "ExtValue") VALUES (NULL, ?, ?);', (keyword, cursor.lastrowid))
        self.__commit_database_changes()

    def __remove_value(self, keyword: str) -> None:
        """
        Remove keyboard from the database. Private method.
        :param keyword: Keyword to operate with.
        """
        kwid = self.__get_internal_id(keyword)
        if kwid > 0:
            cursor = self.__connection.cursor()
            cursor.execute('DELETE FROM "Keys" WHERE "ExtValue" = ?;', (kwid,))
            cursor.execute('DELETE FROM "Values" WHERE "ID" = ?;', (kwid,))
            self.__commit_database_changes()

    def __check_if_orphaned(self, kwid: int) -> bool:
        """
        Check if value is orphaned. Private method.
        :param kwid: Value ID.
        :return: Return True if orphaned.
        """
        cursor = self.__connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM "Values" WHERE "Values"."ID" = ?;', (kwid,))
        return not cursor.fetchone()[0] > 0

    def __remove_alias(self, alias: str) -> None:
        """
        Remove alias from the database.
        :param alias: Alias to operate with.
        """
        kwid = self.__get_internal_id(alias)
        if kwid > 0:
            cursor = self.__connection.cursor()
            cursor.execute('DELETE FROM "Keys" WHERE "Keyword" = ?;', (alias,))
            if self.__check_if_orphaned(kwid):
                cursor.execute('DELETE FROM "Values" WHERE "ID" = ?;', (kwid,))
            self.__commit_database_changes()

    def __add_alias(self, keyword: str, new_alias: str) -> None:
        """
        Add a new alias for the specified keyword. Private method.
        :param keyword: Keyword to operate with.
        :param new_alias: New alias.
        """
        kwid = self.__get_internal_id(keyword)
        if kwid > 0:
            cursor = self.__connection.cursor()
            cursor.execute('INSERT INTO "Keys" ("ID", "Keyword", "ExtValue") VALUES (NULL, ?, ?);', (new_alias, kwid))
            self.__commit_database_changes()

    def add_value(self, keyword: str, value: str) -> None:
        """
        Set value for the specified keyword.
        :param keyword: Keyword to operate with.
        :param value: New value.
        """
        self.__add_value(keyword, value)

    def set_value(self, keyword: str, new_value: str) -> None:
        """
        Set value for the specified keyword.
        :param keyword: Keyword to operate with.
        :param new_value: New value.
        """
        self.__set_value(keyword, new_value)

    def remove_value(self, keyword: str) -> None:
        """
        Remove keyboard from the database.
        :param keyword: Keyword to operate with.
        """
        self.__remove_value(keyword)

    def add_alias(self, keyword: str, new_alias: str) -> None:
        """
        Add a new alias for the specified keyword.
        :param keyword: Keyword to operate with.
        :param new_alias: New alias.
        """
        self.__add_alias(keyword, new_alias)

    def remove_alias(self, alias: str) -> None:
        """
        Remove alias from the database.
        :param alias: Alias to operate with.
        """
        self.__remove_alias(alias)

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

    def __commit_database_changes(self) -> None:
        """
        Save staged changes to file.
        """
        self.__connection.commit()

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
        self.__commit_database_changes()

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
