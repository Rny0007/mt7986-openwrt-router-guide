# Hardware Testing Guide: Safe Verification Protocol for OpenWrt Routers

This guide outlines the standard operating procedure for testing OpenWrt on physical router hardware and collecting empirical evidence for submission to the database.

---

## 1. Safety Checklist Before Power-On

> [!WARNING]
> Testing custom firmware or new device ports carries the risk of soft-bricking the router. Always verify your recovery path BEFORE modifying flash memory.

- [ ] Record the exact model number, hardware revision, and serial number from the casing label.
- [ ] Make a full backup of stock OEM firmware partitions (especially `factory` / `ART` containing wireless calibration data).
- [ ] Verify access to a functional TFTP server and Ethernet cable.
- [ ] If opening the casing, inspect for serial UART header pins and verify logic level with a multimeter (must be 3.3V or 1.8V, NEVER 5V).

---

## 2. Standard Diagnostics Collection Script

Once OpenWrt is running on your test router, run these safe read-only commands via SSH to capture hardware telemetry:

```sh
# System & Kernel Identification
uname -a
cat /etc/openwrt_release
cat /proc/cpuinfo

# Memory & Flash Subsystem
cat /proc/meminfo | grep MemTotal
cat /proc/mtd

# Wireless Subsystem
iwinfo
iw dev

# Network Switch & Physical PHYs
ip link show
dmesg | grep -E 'eth|switch|dsa|phy|ppe|wed'
```

---

## 3. Sanitizing Logs Before Submission

Before posting any dmesg capture or test log in a GitHub issue:
- Replace your WAN public IP with `203.0.113.1` (RFC 5737 TEST-NET-3).
- Replace Wi-Fi passwords with `[REDACTED_SECRET]`.
- Replace device MAC addresses with `00:00:5E:00:53:XX`.
- Strip any ISP subscriber IDs or serial numbers.
