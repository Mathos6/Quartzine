
from enum import Enum


path_to_virtual_disk = "/home/mathieu/projects/Quartzine/vm/vm.qcow2"

virtual_disk_size = "20G"

ram_usage = "2048"

path_to_iso = "/home/mathieu/Bureau/alpine.iso"

ram_usage = "2048"

cpu_cores = "4"

path_to_config_file = "/home/mathieu/projects/Quartzine/config"


class Error(Enum):
    MISSING_DEPENDENCY = 1
