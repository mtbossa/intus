Change the .config.json file with the data of the current display.

Script for opening on startup:

```bash
#! /bin/bash

cd /home/pi/generate_display_html
eval 'ssh-agent'
ssh-add bin/intus_github
git pull
source venv/bin/activate
python3.9 main.py
unclutter -idle 0
```
Create/copy /bin/autostart-display.desktop to:
    /home/pi/.config/autostart/autostart-display.desktop

Content:
```desktop
[Desktop Entry]
Encoding=UTF-8
Name=Display autostart
Comment=Automated process for update check and initialize the Python display
Exec= bash /home/pi/generate_display_html/bin/startup.sh
Terminal=true
```
bash= path/to/startup.sh