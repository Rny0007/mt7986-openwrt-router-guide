# Helper Scripts & Automation Guide

This directory documents recommended safe automation snippets and utility procedures for OpenWrt management.

> [!NOTE]
> All scripts and commands documented here are designed for execution either via local SSH or within the OpenWrt ash shell.
> Always review script logic before running commands with root privileges.

## Recommended Utility Procedures

1. **Configuration Backup Automation**:
   ```sh
   # On router: create standard configuration tarball
   sysupgrade -b /tmp/backup-$(date +%F).tar.gz
   ```

2. **Flow Offload Verification**:
   ```sh
   # Verify nftables offload chain entry
   nft list chain inet fw4 forward | grep "flow add"
   ```

3. **Status LED Verification**:
   ```sh
   # Check current trigger states
   cat /sys/class/leds/*/trigger
   ```
