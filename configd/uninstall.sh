#!/usr/bin/env bash



set -eu

if [[ $EUID -ne 0 ]]; then
  echo "Lance ce script avec sudo"
  exit 1
fi

systemctl disable quartzine.service
rm /etc/udev/rules.d/99-my_udev_rules.rules

rm -r /opt/Quartzine

udevadm control --reload-rules
udevadm trigger

systemctl daemon-reload
