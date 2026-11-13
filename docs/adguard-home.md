# AdGuard Home DNS & Privacy Architecture

This guide explains how to install, configure, and operate **AdGuard Home** directly on OpenWrt running on MediaTek MT7986 hardware.

---

## 1. Architectural Overview: Port 53 Re-alignment

In standard OpenWrt, **Dnsmasq** handles both local DHCP leases and DNS resolution on port 53. To implement network-wide ad-blocking and encrypted upstream DNS with AdGuard Home, we re-align the DNS pipeline:

```mermaid
flowchart TD
    Client["LAN / Wi-Fi Client"] -->|"DNS Query (UDP/TCP 53)"| AGH["AdGuard Home (Port 53)"]
    AGH -->|"Check Local Domain *.lan"| Dnsmasq["Dnsmasq (Port 5353)"]
    Dnsmasq -->|"Resolve Hostname / DHCP Lease"| AGH
    AGH -->|"Blocked Ad/Tracker"| Blackhole["0.0.0.0 / :: (Sinkhole)"]
    AGH -->|"Legitimate External Domain"| DoH["Encrypted Upstream DNS-over-HTTPS (1.1.1.1 / Quad9)"]
```

### The Conflict & Solution:
1. Two services cannot bind to port 53 simultaneously.
2. Dnsmasq is moved to alternate port **5353** (`option port '5353'`), where it continues handling DHCP IP allocation and local `.lan` hostname resolution.
3. AdGuard Home binds to **`0.0.0.0:53`**, serving as the primary network resolver.
4. AdGuard Home forwards local domain queries (`[/lan/]127.0.0.1:5353`) to Dnsmasq, maintaining local device name resolution seamlessly.

---

## 2. Step-by-Step Installation & Configuration

### Step 2.1: Re-align Dnsmasq to Port 5353
```sh
# [Router SSH]
uci set dhcp.@dnsmasq[0].port='5353'
uci commit dhcp
/etc/init.d/dnsmasq restart
```

### Step 2.2: Install AdGuard Home
```sh
# [Router SSH]
opkg update
opkg install adguardhome
```

### Step 2.3: Initial Setup Wizard
1. Open your web browser to:
   `http://192.168.1.1:3000` (initial wizard port).
2. Configure Administration Web Interface on port `8080`.
3. Configure DNS Server to listen on **All Interfaces** on port `53`.
4. Set an administrative username and strong password.

---

## 3. Configuring Upstream DNS & Local Domain Forwarding

Inside the AdGuard Home Web Interface (**Settings** → **DNS Settings**):

### Upstream DNS Servers:
Add privacy-respecting, encrypted DNS-over-HTTPS (DoH) providers:
```text
https://1.1.1.1/dns-query
https://1.0.0.1/dns-query
https://149.112.112.112/dns-query
```

### Private Reverse DNS & Local Domain Resolution:
Under **Private reverse DNS servers**, enter:
```text
127.0.0.1:5353
```
Under **Upstream DNS servers**, add local routing rules:
```text
[/lan/]127.0.0.1:5353
[/168.192.in-addr.arpa/]127.0.0.1:5353
```
This ensures local router hostnames (e.g. `openwrt.lan`) resolve instantly without leaking internal queries to the internet.

### Enable DNSSEC:
Check **Enable DNSSEC** to authenticate responses cryptographically and protect against DNS cache poisoning.

---

## 4. Recommended Filter Blocklists

Under **Filters** → **DNS Blocklists**, enable high-quality community curated lists:
- **AdGuard DNS Filter**: Standard comprehensive blocking list.
- **HaGeZi's DNS Blocklists (Pro)**: High-efficiency, zero-false-positive list optimized for home networks.

---

## 5. Verification

From your host computer:

```sh
# 1. Test local hostname resolution
nslookup openwrt.lan 192.168.1.1

# 2. Test ad domain blocking (should return 0.0.0.0)
nslookup doubleclick.net 192.168.1.1

# 3. Test external domain resolution
nslookup google.com 192.168.1.1
```
All queries should resolve in less than 25 ms, with blocked ad domains sinkholed in under 1 ms.
