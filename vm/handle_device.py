import subprocess
import pwd
from var import config
import os
from .mount_fs import mount_normally, mount_with_vm


def get_real_user():
    user = os.environ.get("SUDO_USER")
    if not user:
        # Si exécuté par systemd/udev sans SUDO_USER, trouver le propriétaire de /dev/tty1 ou /run/user/
        for u in os.listdir("/run/user"):
            if u.isdigit() and int(u) >= 1000:
                try:
                    return pwd.getpwuid(int(u)).pw_name, int(u)
                except KeyError:
                    pass
        user = "1000" # fallback
    uid = pwd.getpwnam(user).pw_uid
    return user, uid


def run_as_user(user, uid, command):
    """Exécute une commande GUI/Notification dans le contexte de l'utilisateur."""
    xdg_runtime_dir = f"/run/user/{uid}"
    dbus_addr = f"unix:path={xdg_runtime_dir}/bus"

    # Détection dynamique du socket Wayland
    wayland_display = None
    if os.path.exists(xdg_runtime_dir):
        for item in os.listdir(xdg_runtime_dir):
            if item.startswith("wayland-"):
                wayland_display = item
                break

    # On prépare la commande avec TOUTES les variables d'environnement graphiques nécessaires
    cmd = [
        "sudo", "-u", user,
        f"XDG_RUNTIME_DIR={xdg_runtime_dir}",
        f"DBUS_SESSION_BUS_ADDRESS={dbus_addr}",
        f"XAUTHORITY=/home/{user}/.Xauthority"  # Pour l'autorisation XWayland/X11
    ]
    
    if wayland_display:
        cmd.append(f"WAYLAND_DISPLAY={wayland_display}")
    
    cmd.append("DISPLAY=:0") # Fallback si besoin

    cmd.extend(command)
    return subprocess.run(cmd, capture_output=True, text=True)

def handle_device(dev):
    mode = config["mode"]
    user, uid = get_real_user()

    if mode == "normal":
        print("monter normalement")
        mount_normally(dev.device_node)
    elif mode == "vm":
        print("monter dans la vm")
        mount_with_vm(dev)
    elif mode == "ask":
        run_as_user(user, uid, ["notify-send", "Quartzine", "Clé USB détectée"])
        resp = run_as_user(user, uid, ["zenity", "--question", "--text=Monter la clé USB dans la VM ?"])
        print(f"[DEBUG] Zenity returncode: {resp.returncode}")
        print(f"[DEBUG] Zenity stderr: {resp.stderr}")
        
        if resp.returncode == 0:
            print("[+] Choix : Monter dans la VM")
            mount_with_vm(dev)
        else:
            print("[+] Choix : Monter normalement")
            mount_normally(dev.device_node)
    else:
        print("Bad value at the config file")
