import pyudev

from detect import detect_device


def main():
    context = pyudev.Context()
    detect_device(context)



main()
