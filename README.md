# FAQ bot

[![GitHub version](https://badge.fury.io/gh/xvitaly%2Ffaqbot.svg)](https://github.com/xvitaly/faqbot/releases)
[![GitHub issues](https://img.shields.io/github/issues/xvitaly/faqbot.svg?label=issues&maxAge=60)](https://github.com/xvitaly/faqbot/issues)
---

FAQ bot for the [Telegram](https://telegram.org/) messenger will find keywords from its database and automatically post them to groups, super-groups or private chats.

Warning! Do not use `dev` branch in production due to possible breaking changes. Use `master` instead.

# License
GNU General Public License version 3. You can find it here: [LICENSE](LICENSE). External libraries can use another licenses, compatible with GNU GPLv3.

# Requirements
 * Python 3.6+;
 * [python-pytelegrambotapi](https://github.com/eternnoir/pyTelegramBotAPI);
 * [python-requests](https://github.com/requests/requests);
 * [python-six](https://github.com/benjaminp/six).

# Documentation
 * [List of available bot actions](docs/available-bot-actions.md).
 * [Installation in Python virtual environment](docs/virtualenv-installation.md).
 * [Controling this bot using systemd](docs/controling-with-systemd.md).
 * [Configuration file documentation](docs/schema-documentation.md).
 * [Configuration using environment options](docs/bot-environment-options.md).
 * [Building Fedora package](docs/building-fedora-package.md).
