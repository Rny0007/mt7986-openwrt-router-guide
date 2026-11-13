# Troubleshooting Guide

This guide provides diagnostic steps and verified resolutions for common issues encountered during OpenWrt installation, configuration, and operation on MediaTek MT7986 hardware.

---

## 1. Quick Triage Diagnostic Table

| Symptom | Possible Cause | Diagnostic Command / Check | Safe Resolution |
| :--- | :--- | :--- | :--- |
| **LuCI Web UI not loading** | `uhttpd` server stopped or crashed | `ps | grep uhttpd` via SSH | Run `/etc/init.d/uhttpd restart` or install `opkg install luci`. |
| **SSH Connection Refused** | Dropbear service not bound to port 22 | `netstat -tulpn | grep 22` | Check `/etc/config/dropbear` to verify `Port '22'` and `Interface 'lan'`. |
| **High Packet Loss / Spikes (60%)** | Overlapping LAN and WAN subnets (both `192.168.1.0/24`) | `ip route; ip addr` | Change local LAN IP to `192.168.31.1` via `uci set network.lan.ipaddr='192.168.31.1'`. |
| **Wi-Fi Repeater Bitrate Capped at 1 Mbps** | Mac80211 scanning dormant SSIDs or country unset | `iw dev phy0-sta0 station dump` | Set country code (`country 'IN'`) and disable unused STA interfaces (`option disabled '1'`). |
| **Front-Panel Status LED Dark** | Conflicting or improperly ordered LuCI LED triggers | `cat /etc/config/system | grep -A 10 'config led'` | Re-align triggers: `red` -> `none`, `blue` -> `netdev eth0`, `green` -> `heartbeat`. |
| **DNS Not Resolving External Domains** | Dnsmasq and AdGuard Home port conflict on port 53 | `netstat -tulpn | grep :53` | Re-align Dnsmasq to port 5353 (`uci set dhcp.@dnsmasq[0].port='5353'`). |
| **Local Hostnames (*.lan) Not Resolving** | AdGuard Home not forwarding `.lan` to Dnsmasq | `nslookup openwrt.lan 127.0.0.1` | Add upstream routing rule in AdGuard: `[/lan/]127.0.0.1:5353`. |
| **5 GHz Wi-Fi Width Stuck at 80 MHz** | Missing `HE160` configuration or regulatory limit | `iwinfo phy1-ap0 info` | Set `option htmode 'HE160'` on `radio1` with compliant country code. |
| **Wired Speed Limited to 94 Mbps** | Client PC has Fast Ethernet (100Base-TX) NIC | Check client NIC link speed in OS | Verify using a Gigabit or 2.5 Gbps Ethernet adapter and Cat6 cable. |
| **Apple Devices (iPhone/iPad) Fail with Automatic DNS** | Dnsmasq on port 5353 omitted DHCP Option 6; dead IPv6 RDNSS broadcast | Inspect `/etc/config/dhcp` for `dhcp_option '6,...'` | Add `list dhcp_option '6,<router-ip>'` and set `ra_dns '0'`, `dns_service '0'`. See [DNS Troubleshooting Guide](DNS-TROUBLESHOOTING.md). |

---

## 2. Detailed Diagnostic Walkthroughs

### Issue A: Overlapping Subnet Routing Failure
If operating in wireless repeater mode, verify your routing table:
```sh
ip route
```
If you observe `default via 192.168.1.1` on the wireless station interface while `br-lan` is also assigned `192.168.1.1`, the Linux kernel experiences ARP flux and non-deterministic gateway routing. Change `network.lan.ipaddr` to a different class C subnet (e.g. `192.168.31.1`) to isolate LAN and WAN routing completely.

### Issue B: Status LED Visibility Troubleshooting
If the front-panel status LED does not illuminate:
1. Verify device tree claims pins in debugfs:
   ```sh
   cat /sys/kernel/debug/gpio | grep -E '(524|525|526)'
   ```
2. Verify pin state: `gpio-524`, `525`, `526` must be claimed by `leds-gpio`.
3. Check trigger configuration in `/etc/config/system`. Ensure that conflicting custom trigger scripts are removed and native `netdev` / `heartbeat` triggers are assigned.

### Issue C: Apple Devices Fail with Automatic DNS (AdGuard Home Setup)
When AdGuard Home runs on port 53 and Dnsmasq is moved to port 5353:
1. Dnsmasq automatically suppresses DHCP Option 6 (DNS server) because it is no longer bound to standard port 53.
2. Windows and Android silently tolerate this via secondary DNS fallbacks or Private DNS, but Apple iOS/iPadOS strictly fails captive portal checks (`captive.apple.com`), reporting "No Internet Connection".
3. Furthermore, if WAN has no native IPv6 connectivity, `odhcpd`'s default IPv6 RDNSS advertisement misleads Apple clients into attempting queries across an unroutable IPv6 path.

**Permanent Resolution:**
```sh
# [Router SSH]
uci add_list dhcp.lan.dhcp_option='6,192.168.10.1'
uci add_list dhcp.lan.dhcp_option='3,192.168.10.1'
uci set dhcp.lan.ra_dns='0'
uci set dhcp.lan.dns_service='0'
uci -q delete dhcp.lan.ra_flags
uci commit dhcp
/etc/init.d/dnsmasq restart
/etc/init.d/odhcpd restart
```
Read the full forensic investigation, raw wire DHCP INFORM packet analysis, and verification benchmarks in the dedicated [DNS Troubleshooting Guide](DNS-TROUBLESHOOTING.md).
