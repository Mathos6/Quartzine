 
import subprocess
import os
import time

from var import config
import var
from vm.utils import get_real_user, run_as_user



# device node peut être /dev/sda1
def mount_normally(device_node):
    try:
        subprocess.run(["udisksctl", "mount", "-b", device_node], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def mount_with_vm(dev):
    if not os.path.isfile(config["path_to_virtual_disk"]):
        print(f"There's no file named {config['path_to_virtual_disk']}. Please create one at this location")
        user, uid = get_real_user()
        resp = run_as_user(
            user, 
            uid, 
            [
                "zenity", 
                "--question",
                "--title=Quartzine",
                "--text=L'image disque n'existe pas. Voulez-vous la créer maintenant ?"
            ]
        )
        
        if resp.returncode == 0:
            create_virtual_disk()
            print("Disk successfully created at", config["path_to_virtual_disk"])
        else:
            print("Action aborted")
            return
            
    print("Checking virtual disk...")
    result = subprocess.run(
        ["virt-inspector", "-a", config["path_to_virtual_disk"]],
        capture_output=True,
        text=True
    ).stdout
    if "<name>" not in result:
        print("You are about to install the OS in the virtual disk. ")
        install_vm()
        print("Installation succesfully completed")

    print("Time to run it")
    run_vm_with_passthrough(dev)





def create_virtual_disk():
    subprocess.run([
        "qemu-img", "create",
        "-f", "qcow2",
        config["path_to_virtual_disk"],
        config["virtual_disk_size"]
    ])

def install_vm():
    user, uid = get_real_user()
    
    cmd = [
        "qemu-system-x86_64", 
        "-enable-kvm",
        "-m", config["ram_usage"],
        "-cdrom", config["path_to_iso"],
        "-drive", f"file={config['path_to_virtual_disk']},format=qcow2,if=virtio",
        "-boot", "d"
    ]
    
    run_as_user(user, uid, cmd)

#TODO: when it'll be done, add the -snapshot flag'
def run_vm_with_passthrough(dev):
    global last_time
    user, uid = get_real_user()
    cmd = [
        "qemu-system-x86_64",
        "-enable-kvm",
        "-snapshot",
        "-m", config["ram_usage"],
        "-smp", config["cpu_cores"],
        "-cpu", "host",
        "-device", "qemu-xhci",
        "-device", f"usb-host,vendorid=0x{dev.get('ID_VENDOR_ID')},productid=0x{dev.get('ID_MODEL_ID')}",
        "-drive", f"file={config['path_to_virtual_disk']},format=qcow2,if=virtio"
    ]
    run_as_user(user, uid, cmd)
    var.last_time = time.time()
