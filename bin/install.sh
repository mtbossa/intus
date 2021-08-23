#! /bin/bash
cd /home/pi/generate_display_html || exit
git remote set-url origin git@github.com:mtbossa/generate_display_html.git
chmod 400 bin/github/intus_github
mkdir -p /home/pi/.config/autostart && cp bin/autostart-display.desktop /home/pi/.config/autostart/autostart-display.desktop