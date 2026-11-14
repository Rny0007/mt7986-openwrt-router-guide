# Attribution & Source Acknowledgements

The **OpenWrt Router Hardware Knowledge Base** is an independent, community-driven educational and research project. We gratefully acknowledge the primary open-source projects, community reverse engineers, and official repositories that make open-source networking possible:

---

## 1. Primary Upstream Projects

### OpenWrt Project
- **Role:** Upstream embedded Linux operating system, target device trees (`dts`), target makefiles, kernel patches, and build systems.
- **Website:** [openwrt.org](https://openwrt.org)
- **Source Code:** [git.openwrt.org](https://git.openwrt.org/openwrt/openwrt.git) and [github.com/openwrt/openwrt](https://github.com/openwrt/openwrt)
- **License:** GNU General Public License v2.0 (GPL-2.0).

### Linux Wireless (`mac80211` / `mt76` / `ath11k`)
- **Role:** Open-source 802.11 Wi-Fi subsystem and radio drivers for MediaTek Filogic and Qualcomm Atheros chipsets.
- **Upstream:** [wireless.wiki.kernel.org](https://wireless.wiki.kernel.org/)
- **License:** ISC / GPL-2.0 Dual License.

### U-Boot (Universal Boot Loader)
- **Role:** Open-source primary and secondary bootloaders (`BL2`, `FIP`, U-Boot proper) utilized across MediaTek Filogic, Rockchip, and Allwinner network platforms.
- **Website:** [denx.de/wiki/U-Boot](https://www.denx.de/wiki/U-Boot)
- **License:** GPL-2.0-or-later.

### AdGuard Home
- **Role:** Network-wide privacy DNS resolver and DNS-over-HTTPS (DoH) engine.
- **Website:** [adguard.com](https://adguard.com/adguard-home.html)
- **License:** GPL-3.0.

---

## 2. Hardware Research & Data Sources

All hardware specifications, memory capacities, partition layouts, and pinouts in this repository are researched from publicly accessible primary evidence:

- **Federal Communications Commission (FCC) Equipment Authorization System:** Internal teardown photography, test reports, and component silkscreen verification ([fcc.gov/oet/ea/fccid](https://www.fcc.gov/oet/ea/fccid)).
- **OpenWrt Table of Hardware (ToH) & Firmware Selector:** Community hardware wiki pages and firmware release manifests ([firmware-selector.openwrt.org](https://firmware-selector.openwrt.org)).
- **OpenWrt Developer Forums:** Technical discussions, serial UART logs, and patch submissions from community reverse engineers ([forum.openwrt.org](https://forum.openwrt.org)).
- **Manufacturer Regulatory & GPL Filings:** Publicly distributed open-source tarballs and datasheets from MediaTek, Arcadyan, GL.iNet, ASUS, FriendlyElec, and Banana Pi.

---

## 3. Original Visuals, Diagrams & Code

- All architectural vector diagrams, SVG graphics, flowchart visualizations, and UI components in this repository are **original creations** authored specifically for this project.
- No copyrighted third-party photography, manufacturer promotional assets, or proprietary interface designs are utilized.
- All code, build scripts, tests, and web interfaces are licensed under the [MIT License](LICENSE).
- All documentation, research data, and hardware schemas are licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](LICENSE-DOCS.md).

---

## 4. Trademark Notices

- "OpenWrt" is a registered trademark of the OpenWrt Project.
- "MediaTek" and "Filogic" are registered trademarks of MediaTek Inc.
- "Qualcomm" is a registered trademark of Qualcomm Incorporated.
- "Broadcom" is a registered trademark of Broadcom Inc.
- "Jio" and "JioFiber" are trademarks of Reliance Jio Infocomm Limited.
- "ASUS", "ROG", and "TUF" are registered trademarks of ASUSTeK Computer Inc.
- "GL.iNet" is a registered trademark of GL Technologies (Hong Kong) Limited.

All trademarks are cited strictly for identification, interoperability, and educational purposes. This project is independent and has not been authorized, sponsored, or endorsed by any trademark owner.
