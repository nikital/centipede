#! /usr/bin/env bash

set -e

# Allow sudo like a baws
echo "`whoami` ALL=(ALL) NOPASSWD: ALL" | sudo tee -ai /etc/sudoers

# Install internet services
sudo apt-get install avahi cryptsetup nfs-kernel-server

# Netcat on boot
# Ubuntu has 'exit 0' as the last line by default, replace it
sudo sed -i "$ c echo 1 | nc 1.1.1.1 54736" /etc/rc.local

# Prepare mount points
sudo mkdir /crypt
sudo mkdir /media/volume

# Export crypt mount
echo "/crypt 1.1.1.1(rw,sync,insecure,no_subtree_check,all_squash,anonuid=`id -u`,anongid=`id -g`)" | sudo tee -ai /etc/exports