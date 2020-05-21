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


class FAQMessagesRu:
    __messages: Dict[Union[str, str], Union[str, str]] = {
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

    def get_message(self, key: str) -> str:
        return self.__messages[key]
