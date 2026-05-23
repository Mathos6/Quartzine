
import pyudev
from read_config import read_config

def detect_device(context):

# A monitor that connects to udev for listening from changes to the \
# device list
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by("block")
    monitor.start()

    print("En attente de périphériques...")

    # device est un tuple (str, <class 'pyudev.device._device.Device'>
    for device in monitor:
        action, dev = device

        if dev.get("ID_BUS") != "usb":
            continue
        if dev.device_type != "partition":
            continue

        if action == "add":
            print(f"device_node: {dev.device_node}")
            print(f"device_type: {dev.device_type}")
            print(f"ID_BUS: {dev.get('ID_BUS')}")
            print(f"[+] Périphérique branché: {dev.device_node}")
            read_config(dev)
        elif action == "remove":
            print(f"[-] Périphérique retiré: {dev.device_node}")
        print("The type is ", type(dev))
        vendor_id = dev.get('ID_VENDOR_ID')
        product_id = dev.get('ID_MODEL_ID')





if __name__ == "__main__":
    detect_device(context)
