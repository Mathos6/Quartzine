#!/usr/bin/env bash


set -eu

IMAGE_DIR="$USER_HOME/.var/quartzine/disk"
IMAGE_URL="https://github.com/Mathos6/Quartzine/releases/download/vm-v1/alpine.gz"

if [ ! -d "$IMAGE_DIR" ] || [ -z "$(ls -A "$IMAGE_DIR" 2>/dev/null)" ]; then
    echo "[+] Dossier VM vide ou inexistant. Téléchargement de l'image Quartzine..."
    
    mkdir -p "$IMAGE_DIR"
    echo "[+] Téléchargement et décompression de l'image VM..."
    curl -L "$IMAGE_URL" | gzip -d > "$IMAGE_DIR/alpine"
    
    chown -R "$SUDO_USER:$SUDO_USER" "$USER_HOME/.var/quartzine"
fi

if [[ $EUID -ne 0 ]]; then
    echo "Lance ce script avec sudo"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
USER_HOME=$(eval echo "~$SUDO_USER")

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
rsync -av --exclude='vm/disk' "$SCRIPT_DIR"/../. /opt/Quartzine
mkdir "$USER_HOME"/.var/quartzine
cp -r "$SCRIPT_DIR"/../vm/disk "$USER_HOME"/.var/quartzine/

udevadm control --reload-rules

systemctl daemon-reload
systemctl enable --now quartzine.service
