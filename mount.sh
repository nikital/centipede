#! /usr/bin/env bash

set -e

sudo ln -vhs "$1" /exports/crypt

VBoxManage snapshot crypt restore crypt
VBoxManage startvm crypt
# Wait for the VM to boot
nc -l 54736 > /dev/null

ssh nikita-crypt.local "sudo mount 1.1.1.1:/exports/crypt /media/volume"

echo -n "Enter Passphrase: "
read -s password
echo

ssh nikita-crypt.local "HISTFILE= echo $password | sudo cryptsetup luksOpen /media/volume/crypt crypt"
ssh nikita-crypt.local "sudo mount /dev/mapper/crypt /crypt"

mkdir -p /Volumes/crypt
sudo mount_nfs nikita-crypt.local:/crypt /Volumes/crypt

open /Volumes/crypt
