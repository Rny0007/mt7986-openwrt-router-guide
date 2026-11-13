# Generic Configuration Examples

This directory contains sanitized, generic configuration examples for OpenWrt running on MediaTek MT7986 routers.

> [!IMPORTANT]
> These configuration files use safe generic placeholders (e.g. `<YOUR_WIFI_PASSWORD>`, `192.168.1.1`).
> Never copy these files directly to your router without adjusting interface names, switch ports, and credentials for your exact environment.

## File Index

- [`network.example`](network.example): Standard LAN/WAN configuration with switch/DSA VLAN mapping.
- [`wireless.example`](wireless.example): Dual-band 802.11ax (Wi-Fi 6) configuration with WPA3/WPA2 mixed encryption.
- [`firewall.example`](firewall.example): Standard OpenWrt fw4 (nftables) ruleset with hardware & software flow offloading.
- [`dhcp.example`](dhcp.example): Dnsmasq configuration adjusted for local resolution with external DNS forwarder (AdGuard Home).
