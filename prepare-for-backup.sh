#!/bin/bash
set -e
set -x

A="/data/bitcoin/.bitcoin"
B="/data/bitcoin/BACKUP"
sudo systemctl stop bitcoind
sudo -u bitcoin mkdir -p $B
sudo -u bitcoin mv $A/blocks $B
sudo -u bitcoin mv $A/chainstate $B
sudo -u bitcoin rm -rf $A
sudo -u bitcoin mv $B $A
