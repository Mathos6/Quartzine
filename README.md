# Quartzine — USB Sandbox Interceptor

> Intercept. Isolate. Observe.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-yellow.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Status](https://img.shields.io/badge/status-early%20development-red)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey)

---

## What is Quartzine?

When a USB drive is plugged into a Linux machine, Quartzine intercepts the event **before the OS mounts anything** — and asks what you want to do with it.

- **Mount normally** → standard OS behavior
- **Analyze** → a disposable VM receives the drive, opens it, navigates it like a real user would, while everything is observed from the host

Designed for **malware analysis labs** that handle physically untrusted media.

---

## How it works

```
USB plugged in
    │
    ├─ udev intercepts (before udisks2 mounts)
    │
    ├─ Mount normally? ──────────────── normal OS behavior
    │
    └─ Analyze?
          │
          ├─ Clean VM snapshot spun up
          ├─ USB passed through to VM
          ├─ VM opens and navigates the drive
          ├─ eBPF + network tap observe everything
          ├─ Report generated
          └─ VM destroyed. Nothing persists.
```

---

## Key properties

**Hardware-triggered** — interception happens at plug-in, not at manual file submission. No human step required.

**Deceptive environment** — the VM mimics a real user machine. Hypervisor artifacts are masked, fake activity history is present. Evasive malware finds what it expects.

**Host-side observation** — eBPF probes run from the host, invisible to anything executing inside the VM.

**Isolated network** — simulated internet via INetSim. The VM never reaches real infrastructure.

**Ephemeral by design** — every analysis starts from a clean snapshot, destroyed on completion.

**Structured reports** — network calls, filesystem changes, spawned processes, exported as JSON.

---

## Stack

| Layer | Tools |
|---|---|
| USB detection | `udev rules`, `pyudev` |
| VM orchestration | `Python`, `libvirt-python`, `QEMU/KVM` |
| Host observation | `eBPF`, `bpftrace`, `Zeek` |
| Network simulation | `INetSim`, `tcpdump` |
| Snapshots | `LVM` or `ZFS` |

---

## Requirements

- Linux x86_64 with KVM support
- Python 3.10+

```bash
pip install pyudev libvirt-python
apt install qemu-kvm libvirt-daemon bpftrace zeek inetutils
```

---

## Status

Early development. Not ready for production use.

Planned milestones:
- [ ] udev interception + user prompt
- [ ] QEMU snapshot lifecycle management
- [ ] USB passthrough to VM
- [ ] eBPF observation layer
- [ ] Network isolation + INetSim integration
- [ ] JSON report generation
- [ ] Anti-evasion VM hardening

---

## Warning

This tool is intended for **controlled lab environments only**.
Never deploy on production machines or outside a properly isolated network.

---

## License

GNU General Public License v3.0 — see [LICENSE](LICENSE) for details.

