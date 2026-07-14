# Quartzine — USB Sandbox Interceptor

> Intercept before it mounts.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-yellow.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Status](https://img.shields.io/badge/status-early%20development-red)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey)

---

## Why

At my school, USB keys circulate between computers all the time, and some of them carry malware. Most people just plug the drive in and grab their file — there's no moment to think about whether it's safe. Quartzine is my attempt at removing that risk without changing anyone's habits: catch the USB key *before* the OS mounts it, and give the option to open it inside a disposable VM instead of directly on the host.

This is a solo project I'm building and iterating on as I learn. It's not a finished product yet — see [Status](#status) below for what actually works today.

---

## What it does

When a USB drive is plugged into a Linux machine, Quartzine intercepts the event **before udisks2 auto-mounts it**, and lets you choose:

- **Mount normally** → standard OS behavior, nothing changes
- **Open in a VM** → the drive is passed through to a disposable virtual machine instead of the host

---

## How it works

```
USB plugged in
    │
    ├─ udev rule blocks auto-mount, Quartzine daemon catches the event
    │
    ├─ Mount normally? ──────────────── standard OS behavior
    │
    └─ Open in VM?
          │
          ├─ QEMU/KVM VM started
          ├─ USB device passed through to the VM (not just an image mount)
          └─ Drive is only ever touched inside the VM
```

---

## Stack

| Layer | Tools |
|---|---|
| USB detection | `udev` rules, `pyudev` |
| VM orchestration | Python, QEMU/KVM |
| Config | TOML |
| Service | systemd |

---

## Requirements

- Linux x86_64 with KVM support
- Python 3.10+

---

## Installation

```
git clone https://github.com/Mathos6/Quartzine
```

or

```
git clone git@github.com:Mathos6/Quartzine.git
```

Then:

```
chmod +x Quartzine/configd/install.sh
sudo ./Quartzine/configd/install.sh
```

You'll need a VM disk image (`.qcow2`) available before the VM mode works — see the config file (`configd/config.toml`) to point Quartzine at yours.

---

## Status

Early development, built and maintained solo. This is a learning project as much as a security tool — expect rough edges.

**Working:**
- [x] udev interception (blocks auto-mount before the OS touches the drive)
- [x] USB passthrough to a QEMU/KVM VM

**In progress / known issues:**
- [ ] VM lifecycle management (snapshotting, cleanup between runs)
- [ ] Headless/systemd VM display handling
- [ ] Config loading edge cases

**Planned:**
- [ ] Host-side observation layer (eBPF/bpftrace)
- [ ] Network isolation + traffic inspection
- [ ] Report generation after a session

> [!CAUTION]
> Not ready for production use. The systemd service and VM mode are still being debugged — test on a disposable machine, not one you rely on.

---

## License

GNU General Public License v3.0 — see [LICENSE](LICENSE) for details.
