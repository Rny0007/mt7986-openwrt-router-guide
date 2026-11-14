# Research Methodology: Evidentiary Standards for Router Hardware Records

This document defines how hardware research is conducted, validated, and documented in the Global OpenWrt Router Hardware Knowledge Base.

---

## 1. Primary vs. Secondary Sources

| Tier | Source Category | Examples | Trust Level |
| :--- | :--- | :--- | :--- |
| **Tier 1 (Canonical)** | Official OpenWrt Git Source Tree | `git.openwrt.org`, `target/linux/*/dts/*.dts`, upstream commits | Authoritative |
| **Tier 1 (Canonical)** | Official OpenWrt Firmware Selector | `firmware-selector.openwrt.org` API manifests | Authoritative |
| **Tier 2 (Official Regulatory)** | FCC Certification Filings | `fccid.io` internal teardown photos, RF exposure reports | Authoritative (for hardware) |
| **Tier 2 (OEM Technical)** | Manufacturer GPL Code / Datasheets | MediaTek Filogic product briefs, Broadcom datasheets | Highly Verifiable |
| **Tier 3 (Community)** | OpenWrt Official Forums & Mailing Lists | Porting discussions, boot logs, dmesg captures | Verifiable |
| **Tier 4 (Secondary)** | Independent Tech Blogs & Teardowns | Reverse engineering writeups, YouTube teardowns | Requires Corroboration |

---

## 2. The Multi-Source Corroboration Rule

No device profile may be submitted based on marketing claims alone. Manufacturers frequently change internal revisions (e.g. replacing MediaTek with Realtek) while maintaining the identical commercial model name.

To establish `OFFICIALLY_SUPPORTED`:
1. The OpenWrt target and profile MUST exist in upstream Git master or a stable release branch.
2. The specific hardware revision MUST match the device tree source file (`.dts`).

To establish `COMMUNITY_VERIFIED`:
1. At least two independent contributors must provide reproducible boot logs or dmesg output confirming functional operation.
