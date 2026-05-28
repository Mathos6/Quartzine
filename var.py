
from enum import Enum

config = {}

with open("configd/config.toml", "r") as file:
    for line in file:
        line = line.strip()
        if line and not line.startswith("#"):
            key, value = line.split("=", 1)
            config[key.strip()] = value.strip().strip('"')

virtual_disk_size = "20G"

ram_usage = "2048"

ram_usage = "2048"

cpu_cores = "4"

class Error(Enum):
    MISSING_DEPENDENCY = 1
