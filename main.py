import pyudev, shutil, sys

from detect import detect_device
from var import Error

def main():
    errors = list()
    if shutil.which('qemu-system-x86_64') is None:
        errors.append("Error: qemu-system-x86_64 is not installed")
    if shutil.which('qemu-img') is None:
        errors.append("Error: qemu-img is not installed")
    if shutil.which('udisksctl') is None:
        errors.append("Error: udisksctl is not installed")
    if shutil.which('notify-send') is None:
        errors.append("Error: notify-send is not installed")
    if shutil.which('zenity') is None:
        errors.append("Error: zenity is not installed")

    if errors:
        for error in errors:
            print(error)
        sys.exit(Error.MISSING_DEPENDENCY.value)

    context = pyudev.Context()
    detect_device(context)



main()
