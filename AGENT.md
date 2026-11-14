# AGENT.md — Permanent Repository Architecture, Standards & Operating Rules

This document outlines the architectural principles, evidentiary standards, research protocols, schema definitions, and maintenance rules governing the **Global OpenWrt Router Hardware Knowledge Base** (`mt7986-openwrt-router-guide`).

---

## 1. Project Mission & Scope

The repository aims to be one of the world's most accurate, trustworthy, transparent, and contributor-friendly community resources for OpenWrt-compatible router hardware.

### Core Principles
1. **Evidence-Based Accuracy**: No AI-hallucinated hardware specs or speculative compatibility claims. Every device entry, SoC record, partition layout, and flashing guide must cite primary or independently verifiable secondary sources (OpenWrt Git, Table of Hardware, official firmware selector, device tree DTS files, FCC filings, or reproducible community hardware teardowns).
2. **Safety First**: Never publish destructive flashing instructions, unverified cross-flashing commands, or experimental bootloader overrides without explicit risk warnings and verified rollback/recovery procedures.
3. **Data Integrity & Privacy**: Never publish private keys, Wi-Fi credentials, ISP usernames/passwords, device serial numbers, personal MAC addresses, or identifying user logs. All test outputs must be generic or sanitized.
4. **Inclusive Community Ownership**: Design structured contribution channels (YAML issue templates, automated schema linting, contributor handbooks) that make it effortless for engineers, privacy advocates, and enthusiasts worldwide to verify and submit hardware profiles.

---

## 2. Directory Architecture

```text
mt7986-openwrt-router-guide/
├── .github/
│   ├── ISSUE_TEMPLATE/           # Structured YAML issue templates
│   ├── workflows/                # CI validation and link-checking workflows
│   └── PULL_REQUEST_TEMPLATE.md  # Standardized PR checklist
├── configs/                      # Sanitized reference UCI configuration files
├── data/
│   ├── schemas/                  # JSON Schemas (device, chipset, vendor)
│   ├── devices/                  # Machine-readable per-device JSON records (by vendor)
│   ├── chipsets/                 # Chipset & SoC architectural profiles
│   ├── sources/                  # Catalog of primary & secondary research sources
│   ├── index.json                # Compiled search & explorer database
│   └── validation-report.json    # Automated CI verification metrics
├── docs/                         # Structured technical knowledge base
│   ├── getting-started/          # Introductory guides & prerequisite checklists
│   ├── hardware/                 # Identification, teardown & component analysis
│   ├── installation/             # Two-stage & standard OpenWrt flashing guides
│   ├── configuration/            # DNS, DHCP, IPv6, Adblock, LED automation
│   ├── networking/               # Multi-WAN, mwan3, travelmate failover, VLAN, DSA
│   ├── wireless/                 # Wi-Fi 6/7 (HE160, DFS, WPA3-SAE, mesh)
│   ├── security/                 # Firewall hardening, flow offload, DoH/DoT
│   ├── performance/              # WED offloading, SQM/CAKE, benchmarks
│   ├── recovery/                 # TFTP recovery, UART serial console, de-bricking
│   ├── troubleshooting/          # DNS, wireless roaming, link negotiation
│   ├── chipset-guides/           # Deep-dives by SoC platform (MediaTek, Qualcomm, etc.)
│   └── vendor-guides/            # OEM quirks, bootloader locks & recovery modes
├── explorer/                     # Lightweight, static browser-based device explorer
├── images/                       # Diagrams, schematics, and UI illustrations
├── scripts/                      # Safe diagnostics, verification & index generator tools
├── tests/                        # Automated test suite (Python/pytest)
├── AGENT.md                      # Permanent architecture & operating rules (this file)
├── CHANGELOG.md                  # Semantic release notes & milestone tracking
├── CITATION.cff                  # Academic & community citation metadata
├── CODE_OF_CONDUCT.md            # Community participation standards
├── CONTRIBUTING.md               # Contribution workflow & guidelines
├── FIRST-TIME-CONTRIBUTORS.md    # Beginner onboarding & quick-start tasks
├── GOVERNANCE.md                 # Project governance & maintainer responsibilities
├── LICENSE                       # MIT License (Code & Scripts)
├── LICENSE-DOCS.md               # CC BY 4.0 License (Documentation & Schemas)
├── llms.txt                      # Standardized AI agent context guide
├── NOTICE.md                     # Legal notices & open-source acknowledgements
├── PROGRESS.md                   # Real-time task progress tracking
├── README.md                     # Repository landing page & global index
├── RESEARCH-METHODOLOGY.md       # Hardware verification & evidentiary rules
├── ROADMAP.md                    # Strategic development roadmap
├── SECURITY.md                   # Vulnerability disclosure policy
└── SUPPORT.md                    # Community support channels & FAQ pointers
```

---

## 3. Evidence Classification & Hardware Status Taxonomy

Every device record in `data/devices/` MUST carry a verified `support_status` label adhering strictly to this taxonomy:

| Status Label | Definition | Required Evidence |
| :--- | :--- | :--- |
| `OFFICIALLY_SUPPORTED` | Device is formally integrated into upstream OpenWrt Git master or stable release branches. | Upstream device tree (`.dts`), Git commit SHA, or official Firmware Selector URL. |
| `COMMUNITY_VERIFIED` | Device runs OpenWrt via functional community build, fork, or patch with multiple independent user verifications. | Forum thread, GitHub pull request, boot log, and photos/dmesg confirmation. |
| `PARTIALLY_VERIFIED` | Device boots OpenWrt, but one or more major subsystems (Wi-Fi, 2.5G PHY, hardware offload) are incomplete or unstable. | Detailed issue tracker link with exact broken subsystems documented. |
| `EXPERIMENTAL` | Early-stage port in progress; bootloader unlock or serial kernel boot achieved, but not safe for production. | Serial boot log, pull request, or active developer branch. |
| `UNSUPPORTED` | Hardware cannot run OpenWrt due to closed bootloader, locked cryptographic signature, unsupported architecture, or missing PHY drivers. | Technical explanation citing SoC constraints or secure boot barriers. |
| `UNKNOWN` | Hardware details exist in public records, but OpenWrt feasibility has not yet been audited. | Basic FCC/teardown citation only; no compatibility assertions made. |

> [!IMPORTANT]
> Never elevate a device's status from `EXPERIMENTAL` or `COMMUNITY_VERIFIED` to `OFFICIALLY_SUPPORTED` unless upstream commit evidence exists in OpenWrt's official Git repository (`git.openwrt.org` or `github.com/openwrt/openwrt`).

---

## 4. Hardware Research Hierarchy of Sources

When researching and verifying device profiles, data MUST be gathered in this strict order of precedence:

1. **Official OpenWrt Upstream Tree**: Device tree source (`target/linux/<target>/dts/*.dts`), image Makefile definitions, and official release manifests.
2. **Official OpenWrt Table of Hardware (ToH)** and Firmware Selector API (`https://firmware-selector.openwrt.org`).
3. **OpenWrt Official Developer Mailing Lists & Forum Threads**: Developer patch submissions, reviewed pull requests, and verified user tests.
4. **FCC ID Filings & Internal Teardowns**: Board photography, component markings, flash/RAM part numbers, and RF front-end module (FEM) IDs.
5. **OEM GPL Source Releases & Technical Documentation**: Kernel tarballs, U-Boot configurations, and hardware revision errata.
6. **Reproducible Community Teardowns & Investigations**: Verified blogs, independent reverse engineering repositories, and UART boot captures.

*Any field that cannot be corroborated through at least one primary source must be marked `null`, `"UNKNOWN"`, or `"UNVERIFIED"`. Never invent clock speeds, RAM capacities, or flash partition sizes.*

---

## 5. Privacy, Secrets & Sanitization Protocol

No commit may contain:
- Wi-Fi pre-shared keys (WPA2/WPA3 passwords)
- SSH private keys (`id_rsa`, `id_ed25519`, Dropbear host keys)
- ISP PPPoE or static WAN credentials
- Public IPv4 addresses or identifiable IPv6 global prefixes
- Hardware MAC addresses of personal client devices (replace with `XX:XX:XX:XX:XX:XX` or RFC 7042 documentation prefixes `00:00:5E:00:53:xx`)
- Physical device serial numbers or IMEI/EID identifiers

---

## 6. Automation & CI Integrity

1. All device records in `data/devices/` must validate without errors against `data/schemas/device.schema.json`.
2. All chipset records in `data/chipsets/` must validate without errors against `data/schemas/chipset.schema.json`.
3. `data/index.json` must be regenerated or validated via `scripts/build-index.py` on every data update.
4. Automated tests (`tests/test_devices.py`) enforce uniqueness of device IDs, validity of source URLs, and non-empty mandatory hardware fields.
5. Third-party GitHub Actions must be pinned to full immutable commit SHAs for supply chain security.
