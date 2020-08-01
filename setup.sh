#/bin/bash

git clone https://github.com/ch3njust1n/pystagram.git
cd pystagram
python setup.py build
sudo python setup.py install
cd ..
git clone https://github.com/nficano/pytube.git
cd pytube
python setup.py build
sudo python setup.py install