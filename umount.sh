#! /usr/bin/env bash

set -e

sudo diskutil unmount /Volumes/crypt
ssh nikita-crypt.local "\
sync\
&& sudo service nfs-kernel-server stop\
&& sudo umount /crypt\
&& sudo cryptsetup luksClose crypt\
&& sudo umount /media/volume\
"

VBoxManage controlvm crypt poweroff
VBoxManage snapshot crypt restore crypt

sudo rm /exports/crypt
