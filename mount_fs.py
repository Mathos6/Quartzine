import subprocess
import os

from var import path_to_virtual_disk, virtual_disk_size

# device node peut être /dev/sda1
def mount_normally(device_node):
    subprocess.run(["udisksctl", "mount", "-b", device_node])


def mount_with_vm(dev):

    if not os.path.isfile(path_to_virtual_disk):
        print(f"There's no file named {path_to_virtual_disk}")
        return

    """
    # Création du disque virtuel
    subprocess.run([
        "qemu-img", "create",
        "-f", "qcow2",
        path_to_virtual_disk,
        virtual_disk_size
        ])

    # lancement de linstallation
    subprocess.run([
        "qemu-system-x86_64", "-enable-kvm",
        "-m", ram_usage,
        "-cdrom", path_to_iso,
        "-drive", f"file={path_to_virtual_disk},format=qcow2,if=virtio"
        "-boot", "d"
    ])

    """
    # Lancer la vm
    subprocess.run([
        "qemu-system-x86_64",
        "-enable-kvm",
        "-m", "2048",
        "-drive", f"file={path_to_virtual_disk},if=virtio"

    ])



mount_with_vm(1)
# A ajouter au lancement de la vm pour le passthrough
"""
    "-usb",
    "-device", f"usb-host,vendorid=0x{dev.get('ID_VENDOR_ID')},productid=0x{dev.get('ID_MODEL_ID')}"
"""




""""
if __name__ == "__main__":
    mount_normally(dev.device_node)
"""
