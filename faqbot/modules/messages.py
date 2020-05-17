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


class FAQMessages:
    __en: Dict[Union[str, str], Union[str, str]] = {
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

    __ru: Dict[Union[str, str], Union[str, str]] = {
        'fb_welcome': 'Отправьте мне команду `/faq КЛЮЧ` и я поищу в своей базе данных ссылку или описание.',
        'fb_notoken': 'Не указан API токен, необходимый для работы. Передайте его при помощи переменных окружения!',
        'fb_pmex': 'Произошла ошибка при выполнении команды пользователя.',
        'fb_faqexpt': 'Произошло исключение во время поиска ключевого слова по базе данных.',
        'fb_faqerr': 'Не удалось выполнить ваш запрос. Попробуйте повторить попытку позднее!',
        'fb_addlog': 'Администратор {} ({}) добавил новое ключевое слово {} в базу данных.',
        'fb_alsaddlog': 'Администратор {} ({}) добавил новый алиас {} для ключевого слова {} в базу данных.',
        'fb_remlog': 'Администратор {} ({}) удалил ключевое слово {} и все его алиасы из базы данных.',
        'fb_alsremlog': 'Администратор {} ({}) удалил алиас {} из базы данных.',
        'fb_editlog': 'Администратор {} ({}) отредактировал описание ключевого слова {} в базе данных.',
        'fb_addmsg': 'Ключевое слово *{}* было успешно добавлено в базу данных.',
        'fb_alsaddmsg': 'Алиас *{}* для ключевого слова *{}* был успешно добавлен в базу данных.',
        'fb_remmsg': 'Ключевое слово *{}* и все его алиасы были успешно удалены из базы данных.',
        'fb_alsremmsg': 'Алиас *{}* был успешно удалён из базы данных.',
        'fb_editmsg': 'Описание ключевого слова *{}* было успешно обновлено в базе данных.',
        'fb_crashed': 'Бот завершился в аварийном режиме. Инициируем перезапуск через 30 секунд.',
        'fb_mlreq': 'Произошла ошибка при разборе запроса. Пожалуйста прочите документацию!',
        'fb_notfound': 'Не удалось найти записей, удовлетворяющих запрошенному ключевому слову!',
        'fb_listkw': 'Имеющиеся ключевые слова: {}.',
        'fb_addexists': 'Ключевое слово *{}* уже существует в базе данных. Никаких действий не было произведено.',
        'fb_notexists': 'Ключевое слово *{}* не существует в базе данных. Никаких действий не было произведено.',
        'fb_faqlink': 'Ответы на самые популярные вопросы вы всегда найдёте в нашем FAQ: {}'
    }

    __index: Dict[Union[str, str], Union[str, str]] = {
        'en': '__en',
        'ru': '__ru'
    }
