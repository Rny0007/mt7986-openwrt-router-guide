# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.3.0] - 2026-11-15

### Added
- **Module A: Firmware Intelligence Center**:
  - Comprehensive firmware image indexing (`factory`, `sysupgrade`, `initramfs_recovery`) across all 72 cataloged devices.
  - Direct OpenWrt Firmware Selector links, cryptographic SHA-256 checksums, prerequisite checks, upgrade/downgrade restrictions, and firmware regression logging.
- **Module B: Security & CVE Intelligence**:
  - Standalone OpenWrt vulnerability registry (`data/security/cves.json`) tracking component-level CVEs (Dnsmasq DNSpooq, FragAttacks, U-Boot ext4, mac80211, mt76, LuCI RPC, Dropbear Terrapin).
  - Integrated CVE vulnerability disclosures, CVSS scores, remediation firmware versions, attack surface hardening, and actionable workarounds into all device profiles.
- **Module C: Hardware Lifecycle & End-of-Support**:
  - Structured lifecycle telemetry tracking announcement dates, retail availability, OEM manufacturer support horizons, OpenWrt release status (`ACTIVE_MAINTENANCE`, `STABLE_SUPPORTED`, `UNSUPPORTED`), and modern replacement hardware recommendations.
- **Module D: Granular Hardware Feature Compatibility Matrix**:
  - 18 discrete subsystem support states per device profile: 2.4 GHz, 5 GHz, 6 GHz Wi-Fi radios, Ethernet switching, Multi-Gig (2.5G/10G SFP+), 802.1Q VLAN DSA, USB storage/tethering, HW NAT, HW flow offload (WED/PPE), CAKE SQM, WireGuard crypto acceleration, WPA3-SAE, 802.11s mesh, DFS radar detection, and BLE controllers.
- **Module E: OEM & Regional Model Normalization**:
  - Comprehensive ODM lineage mapping identifying original hardware manufacturers, factory model codes, rebranded consumer variants, PCB clones, and similar-model collision warnings.
- **Module F: Community Contribution & Moderation System**:
  - JSON schema for community device submissions (`data/schemas/submission.schema.json`), pending review queue, and automated moderation CLI (`scripts/moderate-submissions.py`) with duplicate detection and JSON audit trail.
- **Module G: Versioned Public Read-Only REST API & Bulk Data Exports**:
  - Versioned REST endpoints: `/api/v1/devices/index.json`, `/api/v1/devices/{id}.json`, `/api/v1/chipsets/index.json`, `/api/v1/manufacturers.json`, `/api/v1/security.json`, `/api/v1/lifecycle.json`.
  - Machine-readable bulk exports: `/api/v1/export/devices.json`, `/api/v1/export/devices.csv`, `/api/v1/export/chipsets.json`, `/api/v1/export/security.json`.
  - Full OpenAPI 3.1 schema (`/api/v1/openapi.json`) and interactive documentation portal (`/api/index.html`) with cURL, Python 3, and JavaScript implementation examples.
- **Module H: Board-Level Vector Architecture Schematics**:
  - High-resolution SVG hardware block diagrams synthesized from Linux DTS device trees and teardown schematics for all 72 router models, visualizing bus interconnects (RAM, Flash, Switch ASIC, Wi-Fi radios, UART console).
- **Module I: Technical SEO & Search Console Operations**:
  - Comprehensive operations runbook in `docs/SEO-OPS-GUIDE.md` detailing indexing monitoring, sitemap submission, Core Web Vitals optimization, and structured data validation.
- **Module J: Data Freshness, Quality Scoring & Review Queue**:
  - Catalog freshness auditor (`scripts/audit-freshness.py`) scoring metadata completeness, assigning evidence tiers (`GOLD`, `SILVER`, `BRONZE`), and detecting stale records.

### Testing & Verification
- Unit test suite: 10/10 tests PASSED (`tests/run_tests.py`).
- HTML audit: 259/259 pages validated with 0 missing canonicals, 0 duplicate descriptions, and 0 H1 issues (`tests/audit_site_html.py`).
- Playwright E2E suite: 17/17 scenarios PASSED across responsive viewports, URL pushState, REST API endpoints, and SVG schematics (`tests/test_playwright_e2e.py`).

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
