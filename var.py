import os
import pwd
from enum import Enum

ROOT = os.path.dirname(os.path.abspath(__file__))


def get_real_user_var():
    """Récupère dynamiquement le nom d'utilisateur et l'UID de la session utilisateur active."""
    user = os.environ.get("SUDO_USER")
    if user and user != "root":
        try:
            return user, pwd.getpwnam(user).pw_uid
        except KeyError:
            pass

    # Si exécuté par systemd/udev, on cherche la session utilisateur dans /run/user/
    if os.path.exists("/run/user"):
        for u in os.listdir("/run/user"):
            if u.isdigit() and int(u) >= 1000:
                try:
                    uid = int(u)
                    username = pwd.getpwuid(uid).pw_name
                    return username, uid
                except KeyError:
                    pass

    # Fallback sur le premier utilisateur UID >= 1000 dans /etc/passwd
    for entry in pwd.getpwall():
        if entry.pw_uid >= 1000 and entry.pw_name != "nobody":
            return entry.pw_name, entry.pw_uid

    return "root", 0


def get_real_user_home():
    """Récupère le chemin du dossier utilisateur réel."""
    username, _ = get_real_user_var()
    if username != "root":
        return os.path.expanduser(f"~{username}")
    return os.path.expanduser("~")


config = {}

with open(os.path.join(ROOT, "configd/config.toml"), "r") as file:
    for line in file:
        line = line.strip()
        if line and not line.startswith("#"):
            key, value = line.split("=", 1)
            config[key.strip()] = value.strip().strip('"')

# Gestion du chemin d'image disque
path_to_iso = ""
if config.get("path_to_virtual_disk", "").startswith("~"):
    config["path_to_virtual_disk"] = config["path_to_virtual_disk"].replace("~", get_real_user_home(), 1)


class Error(Enum):
    MISSING_DEPENDENCY = 1


last_time = 0
last_device = None
