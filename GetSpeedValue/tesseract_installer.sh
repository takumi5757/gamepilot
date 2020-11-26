#!/bin/sh

printf "password: "
read password

apt-get install automake ca-certificates g++ git libtool libleptonica-dev make pkg-config

git clone https://github.com/tesseract-ocr/tesseract.git

cd tesseract
./autogen.sh
./configure
make
echo "$password" | sudo -S make install
echo "$password" | sudo -S ldconfig