#!/usr/bin/env python3

import os
import shutil
import sys
import socket
import psutil

def check_reboot():
    return os.path.exists("/run/reboot-required")

def check_disk_full(disk, min_gb, min_percent):
    """Returns True if there isnt enough disk space. otherwise False."""
    du = shutil.disk_usage(disk)
    #calculate the percentage of free space
    percent_free = 100 * du.free / du.total
    #calculate how many free gigabytes
    gigabytes_free = du.free / 2**30
    if gigabytes_free < min_gb or percent_free < min_percent:
        return True
    return False


def check_root_full():
    """Returns True if the root partition is full. False otherwise."""
    return check_root_full(disk="/", min_gb=2, min_percent=10)

def check_no_network():
    """Returns True if it fails to resolve Google's url. Otherwise False. """
    try:
        socket.gethostbyname("www.google.com")
        return False
    except:
        return True

def main():
    checks=[
        (check_reboot, "Pending Reboot"),
        (check_root_full, "Root Partition Full"),
        (check_no_network, "No Working Network"),
    ]
    everything_ok = True
    for check, msg in checks:
        if check():
            print(msg)
            everything_ok = False

    if not everything_ok:
        sys.exit(1)

    print("Everything Ok.")
    sys.exit(0)
main()
