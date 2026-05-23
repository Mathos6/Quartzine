cp 99-my_udev_rules.rules /etc/udev/rules.d
cp config /etc/quartzine/config
udevadm control --reload-rules
