#! /bin/bash
cd /home/pi/generate_display_html
eval 'ssh-agent' >> ~/Desktop/log.txt
ssh-add bin/github/intus_github >> ~/Desktop/log.txt
sleep 5
git pull >> ~/Desktop/log.txt
sleep 5
source venv/bin/activate
cd generate_display_html
python3.9 main.py
unclutter -idle 0