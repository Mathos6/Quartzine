import subprocess

def mount_normally(device_node):
    subprocess.run(["udisksctl", "mount", "-b", device_node])


def mount_with_vm(dev):gi
    """
    # Création du disque virtuel
    subprocess.run([
        "qemu-img",
        "create",
        "-f",
        "qcow2", "/home/mathieu/projects/Quartzine/vm/alpine-sandbox.qcow2",
        "10G"
        ])

    # lancement de linstallation
    subprocess.run([
        "qemu-system-x86_64",
        "-enable-kvm",
        "-m", "2048",
        "-cdrom", "/home/mathieu/projects/Quartzine/alpine-extended-3.23.4-x86_64.iso",
        "-hda", "/home/mathieu/projects/Quartzine/vm/alpine-sandbox.qcow2",
        "-boot", "d"
    ])
    """
    # Lancer la vm
    subprocess.run([
        "qemu-system-x86_64",
        "-enable-kvm",
        "-m", "2048",
        "-hda", "/home/mathieu/projects/Quartzine/vm/alpine-sandbox.qcow2"

    ])



#mount_with_vm(1)
# A ajouter au lancement de la vm pour le passthrough
"""
    "-usb",
    "-device", f"usb-host,vendorid=0x{dev.get('ID_VENDOR_ID')},productid=0x{dev.get('ID_MODEL_ID')}"
"""




""""
if __name__ == "__main__":
    mount_normally(dev.device_node)
"""
