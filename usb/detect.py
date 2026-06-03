
import pyudev, time, subprocess
from vm.read_config import read_config
from var import config
import var

project_root = config["project_root"]

def detect_device(context):

# A monitor that connects to udev for listening from changes to the \
# device list
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by("block")
    monitor.start()

    print("En attente de périphériques...")

    # device est un tuple (str, <class 'pyudev.device._device.Device'>
    devices = list()
    for device in monitor:
        action, dev = device

        if dev.get("ID_BUS") != "usb":
            continue
        if dev.device_type != "partition":
            continue

        if action == "add":
            print(f"[+] Périphérique branché: {dev.device_node}")
            if recently_mounted(dev):
                block_usb(dev)
                continue
            else:
                read_config(dev)


def recently_mounted(dev) -> bool :
    if dev.get("ID_SERIAL") == var.last_device and time.time() - var.last_time < 10:
        var.last_time = time.time()
        return True

    var.last_device = dev.get("ID_SERIAL")
    var.last_time = time.time()
    return False


def block_usb(dev):
    subprocess.run(["/bin/bash", f"{project_root}/usb/block.sh", f"{dev.device_node}"])
