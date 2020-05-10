# Systemd service
 1. Create a new systemd unit `faqbot.service` in `/lib/systemd/system` directory:

 ```
 [Unit]
 Description=FAQ bot for Telegram Messenger
 After=network.target
 
 [Service]
 Type=simple
 Restart=always
 RestartSec=30
 User=faqbot
 Group=faqbot
 ExecStart=VENVPATH/bin/faqbot
 EnvironmentFile=/etc/faqbot/faqbot-env.conf
 
 [Install]
 WantedBy=multi-user.target
 ```

 You must change `User` and `Group` and set `VENVPATH` to path of create Python Virtual Environment.
 
 2. Copy `config/faqbot-env.conf` as `/etc/faqbot/faqbot-env.conf`, open it in any text editor and set API token in `APITOKEN` field, received from [@BotFather](https://t.me/BotFather).
 
 3. Reload system configuration:
 ```
 sudo systemctl daemon-reload
 ```

# Using systemd to control bot

Start bot:
```
sudo systemctl start faqbot.service
```

Stop bot:
```
sudo systemctl stop faqbot.service
```

Restart bot:
```
sudo systemctl restart faqbot.service
```

Enable bot autostart on system boot:
```
sudo systemctl enable faqbot.service
```

Disable bot autostart on system boot:
```
sudo systemctl disable faqbot.service
```
