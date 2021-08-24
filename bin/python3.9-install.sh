#! /bin/bash
VERSION=3.9.6

sudo apt-get update
sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev
wget https://www.python.org/ftp/python/$VERSION/Python-$VERSION.tgz
tar xf Python-$VERSION.tgz
cd Python-$VERSION
./configure --prefix=/usr/local/opt/python-$VERSION --enable-optimizations
make -j 4
sudo make altinstall
cd ..
sudo rm -r Python-3.9.6
rm Python-$VERSION.tar.xz
. ~/.bashrc
