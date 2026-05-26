#!/usr/bin/env bash

set -e
apt install libnotify-bin zenity

cp 99-my_udev_rules.rules /etc/udev/rules.d
cp config /etc/quartzine/config
udevadm control --reload-rules
