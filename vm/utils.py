import os
import pwd
import subprocess


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

