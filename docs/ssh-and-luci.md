# Managing OpenWrt via SSH & LuCI

OpenWrt provides two primary administrative interfaces: the **LuCI Web Management Interface** and the **Dropbear SSH Command Line Shell**.

---

## 1. LuCI Web Management

LuCI is the extensible, Lua/JavaScript-driven web UI for OpenWrt.

### Enabling HTTPS (SSL/TLS)
To encrypt web traffic to the router management interface:

```sh
# [Router SSH]
opkg update
opkg install luci-ssl
/etc/init.d/uhttpd restart
```

Once installed, navigating to `http://192.168.1.1` automatically redirects to `https://192.168.1.1`. Your browser will display a self-signed certificate notice; accept it to proceed securely.

---

## 2. Dropbear SSH Service Configuration

Dropbear is a lightweight SSH server designed for embedded Linux environments.

Configuration file: `/etc/config/dropbear`

### Standard Configuration:
```uci
config dropbear
	option PasswordAuth 'on'
	option RootPasswordAuth 'on'
	option Port '22'
	option Interface 'lan'
```

### Security Hardening Options:
- **Restrict to LAN Interface**: Set `option Interface 'lan'` so Dropbear never listens on public WAN interfaces.
- **Disable Password Auth**: Set `option PasswordAuth 'off'` and `option RootPasswordAuth 'off'` after verifying that your public key in `/etc/dropbear/authorized_keys` works reliably.

Commit changes and restart Dropbear:
```sh
uci commit dropbear
/etc/init.d/dropbear restart
```

---

## 3. Essential Command-Line Diagnostics

When connected via SSH, use these commands for system monitoring and triage:

| Diagnostic Task | Command | Purpose |
| :--- | :--- | :--- |
| **System Uptime & Load** | `uptime` | Shows load averages over 1, 5, and 15 minutes. |
| **Memory Utilization** | `free -m` | Displays total, used, free, and available RAM. |
| **Process Monitor** | `top -b -n 1` | Displays active tasks sorted by CPU utilization. |
| **Flash Overlay Space** | `df -h /overlay` | Shows free disk space on the persistent rootfs overlay. |
| **Wireless Status** | `iwinfo` | Lists SSIDs, channels, HT modes, TX powers, and bitrates. |
| **Kernel Ring Buffer** | `dmesg | tail -n 50` | Displays hardware events, PHY transitions, and driver messages. |
| **System Logs** | `logread | tail -n 50` | Inspects system services, DHCP leases, and SSH authentications. |
| **Firewall Ruleset** | `nft list ruleset` | Inspects active nftables rules and flow offloading chains. |
