#! /bin/bash
cd /home/pi/Intus/GenerateDisplayHtml || exit
eval 'ssh-agent' >> ~/Desktop/log.txt
ssh-add resoures/installation/intus_github >> ~/Desktop/log.txt
echo 'after this, sleep 5s' >> ~/Desktop/log.txt
sleep 5
python3.9 -m pip install --upgrade git+https://github.com/mtbossa/intus.git
echo 'after git pull, sleep 5s' >> ~/Desktop/log.txt
sleep 5
python3.9 -m intus
unclutter -idle 0