# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 2026-11-15

### Added
- **Major Hardware Expansion (72 Devices Total across 31 Manufacturers)**: Added 24 verified device records across 8 global market batches:
  - Batch 1 (Global Consumer): Linksys WRT1900ACS, GL.iNet GL-SFT1200 Opal, Netgear R6700 v3, ASUS RT-AX86U.
  - Batch 2 (Wi-Fi 6/7 Next-Gen): Xiaomi Router 7000, TP-Link Archer BE800 v1, ASUS RT-BE96U.
  - Batch 3 (Japanese & Regional Market): Buffalo WSR-3200AX4S, Buffalo WSR-2533DHPL2.
  - Batch 4 (Travel & Mesh): GL.iNet GL-AR750S Slate, GL.iNet GL-AR300M16 Shadow, Linksys Velop WHW03 Tri-Band.
  - Batch 5 (Enterprise APs & Outdoor CPEs): Ubiquiti UniFi 6 Pro, Ubiquiti UniFi nanoHD, Comfast CF-E390AX, MikroTik cAP ac.
  - Batch 6 (Cellular 4G/5G Gateways): ZTE MF286D (LTE Cat 12), Technicolor DGA4132 TIM HUB, Huawei B535-232.
  - Batch 7 (x86 Appliances & Firewalls): Protectli Vault FW4B, Turris Omnia 2020, Orange Pi R1 Plus LTS, Qotom Q355G4.
  - Batch 8 (Managed Enterprise Switches): Zyxel GS1900-24 (Realtek RTL8382M OpenWrt DSA switch).
- **Silicon Architectures Expansion (20 Platforms Total)**: Added 5 silicon architecture profiles with block diagrams, memory buses, and driver documentation:
  - `marvell-armada-385.json` (Marvell Armada 385 / 88F6820 ARMv7 Cortex-A9)
  - `qualcomm-qca9563.json` (Qualcomm Atheros QCA9563 Dragonfly MIPS 74Kc)
  - `qualcomm-ipq5018.json` (Qualcomm IPQ5018 Maple Dual-Core ARM Cortex-A53)
  - `rockchip-rk3328.json` (Rockchip RK3328 Quad-Core ARM Cortex-A53)
  - `broadcom-bcm63138.json` (Broadcom BCM63138 Dual-Core ARM Cortex-A9 DSL/PON Gateway)
- **Search-Intent Category Landing Pages (8 Categories + Hub)**: Built dedicated, search-engine-optimized category landing pages featuring ItemList/TechArticle JSON-LD structured data, selection criteria, comparison tables, and deep dive reviews:
  - `/categories/best-openwrt-routers/` (Best Routers Overall 2024–2026)
  - `/categories/wifi-7/` (Wi-Fi 7 802.11be Upstream Status & Matrix)
  - `/categories/wifi-6/` (Wi-Fi 6 AX3000 to AX6000 Tested Sweet Spot)
  - `/categories/travel-routers/` (Portable Travel Gateways & VPN Repeaters)
  - `/categories/mesh-systems/` (802.11s Wireless Mesh & EasyMesh Hardware)
  - `/categories/multi-gig-2-5g/` (2.5G & 10G Multi-Gigabit Ethernet Routers)
  - `/categories/x86-firewalls/` (x86_64 Fanless Mini-PC OpenWrt Firewalls)
  - `/categories/cellular-4g-5g/` (4G LTE Cat 12 & 5G Cellular Gateways)
  - `/categories/` (Categories Directory Hub)
- **Explorer URL Navigation & History Persistence**:
  - Implemented `pushState` for dropdown filter selections and quick search pills.
  - Implemented `popstate` browser event listener to restore search inputs, filter states, active chips, and hardware card counts on browser Back / Forward buttons.
  - Added keyboard shortcut `/` to focus search and `Escape` to clear search or close comparison modals.

### Security
- Mandated 3.3V TTL voltage mandate and NEVER CONNECT VCC (RED WIRE) electrical warnings across all 72 disaster recovery guides.
- Implemented strict isolation: zero simulated or hypothetical flashing commands for proprietary, closed-source, or unsupported router hardware.

### Testing & Verification
- Unit test suite: 10/10 tests PASSED (`tests/run_tests.py`).
- HTML audit: 258/258 pages validated with 0 missing canonicals, 0 duplicate descriptions, and 0 H1 issues (`tests/audit_site_html.py`).
- Playwright E2E suite: 15/15 scenarios PASSED with 0 failures (`tests/test_playwright_e2e.py`).
- Lighthouse desktop audit: 100 Performance | 96 Accessibility | 100 Best Practices | 100 SEO.

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
