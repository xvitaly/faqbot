# coding=utf-8

# Russian Fedora FAQ bot for Telegram Messenger
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

from setuptools import setup, find_packages

setup(
    name='faqbot',
    version='1.0.0',
    packages=find_packages(),
    package_dir={
        'faqbot': 'faqbot',
    },
    url='https://github.com/xvitaly/rfaqbot',
    entry_points={
        'console_scripts': [
            'faqbot = faqbot.scripts.runbot:main',
        ],
    },
    license='GPLv3',
    install_requires=['pytelegrambotapi', 'requests', 'six'],
    author='Vitaly Zaitsev',
    author_email='vitaly@easycoding.org',
    description='FAQ bot for Telegram Messenger'
)
