#! /usr/bin/env bash

set -e

# Allow sudo like a baws
echo "`whoami` ALL=(ALL) NOPASSWD: ALL" | sudo tee -ai /etc/sudoers

# Install SSH key
echo -n "Enter URL to pull the key from: "
read key_url
echo
mkdir .ssh
curl $key_url >> .ssh/authorized_keys

# Install internet services
sudo apt-get install avahi-daemon cryptsetup nfs-kernel-server

# Netcat on boot
# Ubuntu has 'exit 0' as the last line by default, replace it
sudo sed -i "$ c echo 1 | nc 1.1.1.1 54736" /etc/rc.local

# Prepare mount points
sudo mkdir /crypt
sudo mkdir /media/volume

# Export crypt mount
echo "/crypt 1.1.1.1(rw,sync,insecure,no_subtree_check,all_squash,anonuid=`id -u`,anongid=`id -g`)" | sudo tee -ai /etc/exports

echo "Setup complete, move the machine to Host-Only mode in subnet 1.1.1.* after poweroff."
echo "Press ENTER to poweroff."

read
sudo poweroff
