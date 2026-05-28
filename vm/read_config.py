import subprocess
from var import config

from .mount_fs import mount_normally, mount_with_vm

def read_config(dev):
    mode = config["mode"]
    if mode == "normal":
        print("monter normalement")
        mount_normally(dev.device_node)
    elif mode == "vm":
        print("monter dans la vm")
        mount_with_vm(dev)
    elif mode == "ask":
        subprocess.run(["notify-send", "Quartzine", "Clé USB détectée"])
        resp = subprocess.run(["zenity", "--question", "--text=Monter dans la VM?"], capture_output=True)
        if resp.returncode == 0:
            print("monter dans la vm")
            mount_with_vm(dev)
        else:
            print("monter normalement")
            mount_normally(dev.device_node)
    else:
        print("Bad value at the config file")

