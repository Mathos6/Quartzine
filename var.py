import os

from enum import Enum

ROOT = os.path.dirname(os.path.abspath(__file__))

config = {}

with open(os.path.join(ROOT, "configd/config.toml"), "r") as file:
    for line in file:
        line = line.strip()
        if line and not line.startswith("#"):
            key, value = line.split("=", 1)
            config[key.strip()] = value.strip().strip('"')

            
# L'utilisateur pourrait le specifier s'il veut sa propre distro
# Pas encore intégré
path_to_iso = ""

class Error(Enum):
    MISSING_DEPENDENCY = 1



last_time = 0
last_device = None
