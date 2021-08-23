#! /bin/bash
cd /home/pi/generate_display_html || exit
eval 'ssh-agent' >> log.txt
ssh-add bin/github/intus_github >> log.txt
git pull >> log.txt
source venv/bin/activate >> log.txt
cd generate_display_html || exit >> log.txt
python3.9 main.py >> log.txt
unclutter -idle 0 >> log.txt