# Quartzine — USB Sandbox Interceptor

> Intercept. Isolate. Observe.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-yellow.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Status](https://img.shields.io/badge/status-early%20development-red)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey)

---

## What is Quartzine?

When a USB drive is plugged into a Linux machine, Quartzine intercepts the event **before the OS mounts anything** — and asks what you want to do with it.

- **Mount normally** → standard OS behavior
- **Mount with VM** → a disposable VM receives the drive, opens it, navigates it like a real user would.

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
    └─ Analyze(mount with VM)?
          │
          ├─ Clean VM snapshot spun up
          ├─ USB passed through to VM
          ├─ VM opens and navigates the drive
          ├─ eBPF + network tap observe everything
          ├─ Report generated
          └─ VM destroyed. Nothing persists.
---

## Stack

| Layer | Tools |
|---|---|
| USB detection | `udev rules`, `pyudev` |
| VM orchestration | `Python`, `QEMU/KVM` |
| Host observation | `eBPF`, `bpftrace` |
| Network simulation | `INetSim`, `tcpdump` |

---

## Requirements

- Linux x86_64 with KVM support
- Python 3.10+


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

## License

GNU General Public License v3.0 — see [LICENSE](LICENSE) for details.
