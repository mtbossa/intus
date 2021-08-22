#! /bin/bash

cd /home/pi/generate_display_html || exit
eval 'ssh-agent'
ssh-add bin/intus_github
git pull
source venv/bin/activate
python3.9 main.py
unclutter -idle 0