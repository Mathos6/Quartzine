#!/usr/bin/env bash


set -eu

if [[ $EUID -ne 0 ]]; then
    echo "Lance ce script avec sudo"
    exit 1
fi

USER_HOME=$(eval echo "~$SUDO_USER")
IMAGE_DIR="$USER_HOME/.var/quartzine/disk"
IMAGE_URL="https://github.com/Mathos6/Quartzine/releases/download/vm-v1/alpine.gz"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REAL_USER=${SUDO_USER:-$USER}


for file in quartzine.service 99-my_udev_rules.rules; do
    [[ -f "$SCRIPT_DIR/$file" ]] || {
        echo "Erreur: $file manquant dans $SCRIPT_DIR"
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
rsync -av --exclude='vm/disk' "$SCRIPT_DIR"/../. /opt/Quartzine


cp "${SCRIPT_DIR}"/99-my_udev_rules.rules /etc/udev/rules.d
cp "${SCRIPT_DIR}"/quartzine.service /etc/systemd/system/


if [ ! -d "$IMAGE_DIR" ] || [ -z "$(ls -A "$IMAGE_DIR" 2>/dev/null)" ]; then
    echo "[+] Dossier VM vide ou inexistant. Téléchargement de l'image Quartzine..."
    
    mkdir -p "$IMAGE_DIR"
    echo "[+] Téléchargement et décompression de l'image VM..."
    curl -L "$IMAGE_URL" | gzip -d > "$IMAGE_DIR/alpine"
    
    chown -R "$SUDO_USER:$SUDO_USER" "$USER_HOME/.var/quartzine"
fi

chown -R "$REAL_USER:$REAL_USER" "$USER_HOME/.var/quartzine"

udevadm control --reload-rules
systemctl daemon-reload
systemctl enable --now quartzine.service

echo "[+] Installation de Quartzine terminée !"
