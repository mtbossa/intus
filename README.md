Script for opening on startup:

```bash
#! /bin/bash

cd /home/pi/intus
eval 'ssh-agent'
ssh-add bin/intus_github
git pull
source venv/bin/activate
python3.9 __main__.py
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

Download:
```git
git clone --single-branch --branch main https://github.com/mtbossa/generate_display_html.git

login: mtbossa
pat: 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
```

Build:
```
python -m pip install build

python -m build --sdist
```
To change the code:
```
Create venv

Activate it

pip install -e .
```
Now, every change will be applied
when python -m intus, without the need
to install again

For installing from git:

```
python -m pip install git+https://github.com/mtbossa/intus.git

Update:
python -m pip install --upgrade git+https://github.com/mtbossa/intus.git 
```