#!/usr/bin/env bash

DEV="$1"

#unmount if alreday mounted
umount "$DEV" 2>/dev/null


#eject key
udisksctl power-off -b "$DEV"


logger "USB bloquée: $DEV"
