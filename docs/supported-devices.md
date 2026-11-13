# Supported Devices Compatibility Matrix

This matrix categorizes hardware compatibility for MediaTek MT7986 / MT7986A (Filogic 830) routers across official OpenWrt releases and community test beds.

> [!IMPORTANT]
> Never assume firmware images are cross-compatible between different router models, even if they share the same MT7986 SoC. Board layouts, pin muxing, switch chips (MT7531 vs Realtek vs direct PHYs), and flash partition tables differ significantly.

---

## 1. JIDU Device Family (Arcadyan / Jio Platforms)

| Device Model | Board ID | SoC | RAM / Flash | OpenWrt Profile | Official Status | Verified Release | Notes / Differences |
| :--- | :---: | :---: | :---: | :--- | :---: | :---: | :--- |
| **JIDU6101** | `6j01` | MT7986A | 512 MB / 256 MB SPI-NAND | `jiorouter_ax6000-jidu6101` | **Officially Supported** | OpenWrt 25.12.6 | **Primary Reference Model**. Dual-slot UBI layout on `mtd5`/`mtd6`, MT7531AE switch, MT7976C Wi-Fi. Verified working. |
| **JIDU6201** | `6j01` | MT7986A | 512 MB / 256 MB SPI-NAND | `jiorouter_ax6000-jidu6101` | **Community Verified** | OpenWrt 25.12.x | Hardware shares `6j01` PCB layout with JIDU6101; antenna configuration variants. |
| **JIDU6401** | `6j01` | MT7986A | 512 MB / 256 MB SPI-NAND | `jidu6j01` (generic) | *Unverified — Please Confirm* | — | Enterprise/outdoor housing revision. Confirm bootloader and signature locks before flashing. |
| **JIDU6601** | `6j01` | MT7986A | 512 MB / 256 MB SPI-NAND | `jidu6j01` (generic) | *Unverified — Please Confirm* | — | Requires verification of UART headers and SPI NAND partition table. |
| **JIDU6701** | `6j01` | MT7986A | 512 MB / 256 MB SPI-NAND | `jidu6j01` (generic) | *Unverified — Please Confirm* | — | Upgraded memory variant reported in field; requires flash dump audit. |

---

## 2. Broader MT7986 Router Ecosystem

| Manufacturer & Model | SoC | Ethernet Configuration | Wireless Specification | OpenWrt Profile | Official Support Status | Source Reference |
| :--- | :---: | :--- | :--- | :--- | :---: | :--- |
| **GL.iNet GL-MT6000 (Flint 2)** | MT7986A | 2x 2.5 GbE + 4x 1 GbE | 4x4 2.4GHz + 4x4 5GHz (AX6000) | `glinet_gl-mt6000` | **Officially Supported** | OpenWrt ToH / Stable |
| **Banana Pi BPI-R3** | MT7986A | 2x 2.5G SFP + 5x GbE | 4x4 2.4GHz + 4x4 5GHz (AX6000) | `bananapi_bpi-r3` | **Officially Supported** | OpenWrt ToH / Stable |
| **Acer Predator Connect W6** | MT7986A | 1x 2.5 GbE + 4x 1 GbE | Tri-Band AX7800 (MT7976 + MT7979) | `acer_predator-w6` | **Community Supported** | Upstream Pull Request |
| **Asus TUF Gaming AX4200** | MT7986A | 1x 2.5 GbE + 4x 1 GbE | 2x2 2.4GHz + 3x3 5GHz (AX4200) | `asus_tuf-ax4200` | **Officially Supported** | OpenWrt ToH / Stable |
| **Mercusys MR90X (v1)** | MT7986A | 1x 2.5 GbE + 3x 1 GbE | 4x4 2.4GHz + 4x4 5GHz (AX6000) | `mercusys_mr90x-v1` | **Officially Supported** | OpenWrt ToH / Stable |
| **ZyXEL NWA50AX Pro** | MT7986A | 1x 2.5 GbE PoE | 2x2 2.4GHz + 3x3 5GHz | `zyxel_nwa50ax-pro` | **Officially Supported** | OpenWrt ToH / Stable |

---

## 3. Official Source Links

- OpenWrt Target Source: [`target/linux/mediatek/filogic/`](https://git.openwrt.org/?p=openwrt/openwrt.git;a=tree;f=target/linux/mediatek/filogic)
- OpenWrt Table of Hardware (ToH): [OpenWrt ToH MediaTek MT7986](https://openwrt.org/toh/views/toh_extended_all?dataflt%5BSoC*%7E%5D=MT7986)
- Official Firmware Selector: [firmware-selector.openwrt.org](https://firmware-selector.openwrt.org)
