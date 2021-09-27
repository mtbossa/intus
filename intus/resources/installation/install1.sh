#! /bin/bash
python3.9 -m -m pip install git+https://github.com/mtbossa/intus.git
cd /home/pi/Intus/GeneretaDisplayHtml || exit
chmod +x resources/installation/startup.sh
chmod 400 resources/installation/intus_github
mkdir -p /home/pi/.config/autostart && cp resources/installation/autostart-display.desktop /home/pi/.config/autostart/autostart-display.desktop