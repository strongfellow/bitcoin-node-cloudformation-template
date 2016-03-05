#!/bin/bash
sudo apt-get update


# Install dependencies
# https://github.com/bitcoin/bitcoin/blob/master/doc/build-unix.md
sudo apt-get install build-essential libtool autotools-dev automake pkg-config libssl-dev libevent-dev bsdmainutils
sudo apt-get install libboost-system-dev libboost-filesystem-dev libboost-chrono-dev libboost-program-options-dev libboost-test-dev libboost-thread-dev
sudo apt-get install libzmq3-dev

mkdir -p src && cd src
git clone https://github.com/bitcoin/bitcoin.git
cd bitcoin
git checkout tags/v0.12.0  -b v0.12.0

./autogen.sh
./configure --disable-wallet --with-zeromq
make
make install 
