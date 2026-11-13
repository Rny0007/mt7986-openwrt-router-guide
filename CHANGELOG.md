# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
