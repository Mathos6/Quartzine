#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

set -e
sudo apt install libnotify-bin zenity python3 python3-pyudev qemu-kvm libguestfs-tools

sudo cp 99-my_udev_rules.rules /etc/udev/rules.d
sudo cp quartzine.service /etc/systemd/system/

sudo mkdir -p /opt/Quartzine

# a modifier
sudo cp -r "$SCRIPT_DIR"/../* /opt/Quartzine/

echo "Specify the path where you want want to create your virtual disk"
read -p  "> " path_to_virtual_disk
read -p "Where do your image file lives ? >" path_to_iso

sudo systemctl daemon-reload
sudo systemctl enable quartzine.service
sudo systemctl start quartzine.service

udevadm control --reload-rules
sudo udevadm trigger
