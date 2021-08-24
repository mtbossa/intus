#! /bin/bash
cd /home/pi/generate_display_html || exit
eval 'ssh-agent' >> ~/Desktop/log.txt
ssh-add bin/github/intus_github >> ~/Desktop/log.txt
sleep 5
echo 'waiting 5s' >> ~/Desktop/log.txt
git pull >> ~/Desktop/log.txt
echo 'waiting 5s again' >> ~/Desktop/log.txt
sleep 5
source venv/bin/activate
cd generate_display_html || exit
python3.9 main.py
unclutter -idle 0