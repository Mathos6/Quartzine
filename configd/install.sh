#!/usr/bin/env bash

set -e
sudo apt install libnotify-bin zenity python3 python3-pyudev qemu-kvm libguestfs-tools
pip install pyudev

sudo cp 99-my_udev_rules.rules /etc/udev/rules.d
sudo cp config /etc/quartzine/config
echo "Specify the path where you want want to create your virtual disk"
read -p  "> " path_to_virtual_disk
read -p "Where do your image file lives ? >" path_to_iso

echo "export path_to_virtual_disk=$path_to_virtual_disk" >> ~/.bash_profile
echo "export path_to_iso=$path_to_virtual disk" >> ~/.bash_profile
udevadm control --reload-rules
