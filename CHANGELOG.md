# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-11-13

### Added
- Comprehensive DNS troubleshooting guide (`docs/DNS-TROUBLESHOOTING.md`) documenting the Apple iOS/iPadOS Automatic DNS failure under split-DNS architectures (AdGuard Home on port 53 + Dnsmasq on port 5353).
- Wire-level empirical verification capturing pre-fix and post-fix DHCP INFORM packets proving DHCP Option 6 delivery.
- Updated `configs/dhcp.example` with explicit DHCP Option 6 (`6,192.168.10.1`) and Option 3 declarations alongside IPv6 RDNSS suppression (`ra_dns '0'`, `dns_service '0'`).

### Fixed
- Documented Dnsmasq port 5353 relocation behavior where DHCP Option 6 (DNS server) is omitted by default, stranding Apple clients adhering strictly to RFC 2131.
- Documented `odhcpd` dead IPv6 DNS announcement resolution when WAN lacks native IPv6 routing.

## [1.0.0] - 2026-11-13

### Added
- Complete architecture and installation guide for MediaTek MT7986 (Filogic 830) routers.
- Verified hardware reference implementation for the Arcadyan/Jio JIDU6101 (`6j01`) running official OpenWrt 25.12.6.
- Comprehensive MT7986 device compatibility matrix covering JIDU family and broader ecosystem (GL.iNet, Banana Pi, Acer, Asus, Mercusys).
- Step-by-step guides for LuCI, Dropbear SSH key authentication, and network topology transitions.
- Lightweight privacy stack documentation: AdGuard Home DNS integration with local Dnsmasq forwarding and encrypted Upstream DNS-over-HTTPS (DoH).
- Hardware and software Flow Offloading implementation details.
- Verified front-panel status LED configuration documentation utilizing native OpenWrt `leds-gpio` triggers.
- Multi-tier recovery hierarchy including software rollback, HTTP failsafe, U-Boot serial console TFTP recovery, and SPI-NAND hardware programmer steps.
- Sanitized UCI configuration examples for network, wireless, firewall, and DHCP.
- AI assistant integration guide and machine-readable `llms.txt`.
