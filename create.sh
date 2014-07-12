#! /usr/bin/env bash

set -e

mkdir -p "$1"
sudo ln -vhs "$1" /exports/crypt

VBoxManage snapshot crypt restore crypt
VBoxManage startvm crypt
# Wait for the VM to boot
nc -l 54736 > /dev/null

ssh nikita-crypt.local "sudo mount 1.1.1.1:/exports/crypt /media/volume"

# Drop the user to SSH to handle the creation
ssh nikita-crypt.local

VBoxManage controlvm crypt poweroff
VBoxManage snapshot crypt restore crypt

sudo rm /exports/crypt
