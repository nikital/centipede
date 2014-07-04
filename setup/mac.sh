#! /usr/bin/env bash

set -e

sudo mkdir /exports
echo "/exports/crypt -rw -mapall=`id -nu`:`id -ng` -network 1.1.1.0 -mask 255.255.255.255" | sudo tee -ai /etc/exports
