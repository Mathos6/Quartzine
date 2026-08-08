
from var import config
from .mount_fs import mount_normally, mount_with_vm
from vm.utils import get_real_user, run_as_user

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
