import subprocess

from mount_fs import mount_normally, mount_with_vm

def read_config(dev):

    with open("/home/mathieu/projects/Quartzine/config", 'r') as file:
        for line in file:
            if line.startswith("mode") and "=" in line:
                _, value = line.split("=", 1)
                value = value.strip()



    mount_with_vm(dev)
"""
    if value == "normal":
        print("monter normalement")
        mount_normally(dev.device_node)
    elif value == "vm":
        print("monter dans la vm")
        mount_with_vm(dev)
    elif value == "ask":
        subprocess.run(["notify-send", "Quartzine", "Clé USB détectée"])
        resp = subprocess.run(["zenity", "--question", "--text=Monter dans la VM?"], capture_output=True)
        resp = input("voulez-vous le monter dans la VM ?").lower()
        if resp.returncode == 0:
            print("monter dans la vm")
            mount_with_vm(dev)
        else:
            print("monter normalement")
            mount_normally(dev.device_node)
    else:
        print("Bad value at the config file")
"""




if __name__ == "__main__":
    read_config(dev)
