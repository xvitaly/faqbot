# Installing bot into Python Virtual Environment
You can also install bot:
 1. Clone this repository:
 ```
 git clone https://github.com/xvitaly/faqbot.git faqbot
 git checkout master
 ```
 2. Get API token from [@BotFather](https://t.me/BotFather);
 3. Copy configuration file `config/faqbot.json` to `/etc/faqbot/faqbot.json`. You can edit it in any text editor;
 4. Create a new Python Virtual Environment:
 ```
 python3 -m venv faqbot
 ```
 5. Activate Virtual Environment:
 ```
 source faqbot/bin/activate
 ```
 6. Install bot using Python 3 in VENV:
 ```
 cd faqbot
 python3 setup.py install
 ```
 7. Run installed bot with defined API key:
 ```bash
 APIKEY=API_KEY /bin/faqbot
 ```
