Change the .config.json file for setting the display options.

Script for opening on startup:

```bash
#! /bin/bash

eval 'ssh-agent'
ssh-add ~/Desktop/intus_github
cd ~/generate_display_html
git pull
source venv/bin/activate
python3.9 main.py
unclutter -idle 0
```