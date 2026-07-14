import subprocess
import os
import time

from var import (
    config, virtual_disk_size,
    cpu_cores, ram_usage, path_to_iso,
)
import var

# device node peut être /dev/sda1
def mount_normally(device_node):
    try:
        subprocess.run(["udisksctl", "mount", "-b", device_node], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def mount_with_vm(dev):
    if not os.path.isfile(config["path_to_virtual_disk"]):
        print(f"There's no file named {config['path_to_virtual_disk']}. Please create one at this location")
        resp = input("do you want to create a disk now? (yes, no)").lower()
        if resp == "yes":
            create_virtual_disk()
            print("Disk succesfully created at", config["path_to_virtual_disk"])
        else:
            print("action aborted")
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
        virtual_disk_size
    ])

def install_vm():
    subprocess.run([
        "qemu-system-x86_64", "-enable-kvm",
        "-m", ram_usage,
        "-cdrom", path_to_iso,
        "-drive", f"file={config['path_to_virtual_disk']},format=qcow2,if=virtio",
        "-boot", "d"
    ])

#TODO: when it'll be done, add the -snapshot flag'
def run_vm_with_passthrough(dev):
    global last_time
    subprocess.run([
        "qemu-system-x86_64",
        "-enable-kvm",
        "-m", ram_usage,
        "-smp", cpu_cores,
        "-cpu", "host",
        "-device", "qemu-xhci",
        "-device", f"usb-host,vendorid=0x{dev.get('ID_VENDOR_ID')},productid=0x{dev.get('ID_MODEL_ID')}",
        "-drive", f"file={config['path_to_virtual_disk']},format=qcow2,if=virtio"

    ])

    var.last_time = time.time()
