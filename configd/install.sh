#!/usr/bin/env bash


set -eu

if [[ $EUID -ne 0 ]]; then
    echo "Lance ce script avec sudo"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

for file in quartzine.service 99-my_udev_rules.rules; do
    [[ -f "$SCRIPT_DIR/$file" ]] || {
        echo "$file manquant"
        exit 1
    }
done

apt install libnotify-bin zenity \
    python3 qemu-kvm libguestfs-tools -y

# J'utilise pyudev=0.24.3-1
# Je n'ai pas encore testé les nouvelles versions (s'il y en a)
# Je modifierai plus tard
apt install python3-pyudev=0.24.3-1 -y

mkdir -p /opt/Quartzine
cp "${SCRIPT_DIR}"/99-my_udev_rules.rules /etc/udev/rules.d
cp "${SCRIPT_DIR}"/quartzine.service /etc/systemd/system/


# a modifier
cp -r "$SCRIPT_DIR"/../. /opt/Quartzine/



udevadm control --reload-rules
udevadm trigger

systemctl daemon-reload
systemctl enable --now quartzine.service
