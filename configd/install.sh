#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

set -e
sudo apt install libnotify-bin zenity python3 qemu-kvm libguestfs-tools

# J'utilise pyudev=0.24.3-1
# Je n'ai pas encore testé les nouvelles versions (s'il y en a)
sudo apt install python3-pyudev=0.24.3-1

sudo mkdir -p /opt/Quartzine
sudo cp 99-my_udev_rules.rules /etc/udev/rules.d
sudo cp quartzine.service /etc/systemd/system/


# a modifier
sudo cp -r "$SCRIPT_DIR"/../* /opt/Quartzine/
echo "Specify the path where you want want to create your virtual disk"



udevadm control --reload-rules
sudo udevadm trigger

sudo systemctl daemon-reload
sudo systemctl enable quartzine.service
sudo systemctl start quartzine.service

