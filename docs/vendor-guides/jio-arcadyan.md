# Jio / Arcadyan Router Hardware Reference Guide: JIDU6101, JIDU6201 & Variants

This reference document synthesizes empirical hardware investigations, device tree analysis, and real-world deployment telemetry for OpenWrt on Arcadyan-built **Jio AirFiber** and **JioFiber** gateway hardware.

---

## 1. Hardware Matrix & Platform Disambiguation

> [!CAUTION]
> Do NOT assume compatibility between different Jio router model numbers based on external appearance, naming schemes, or ISP branding. Different JIDU model numbers use completely different MediaTek SoCs, flash architectures, and switch fabrics.

| Model | Marketing Name | ODM Hardware ID | SoC Silicon | CPU Architecture | Wi-Fi Radios | Switch / PHY | OpenWrt Support Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **JIDU6101** | Jio AirFiber AX6000 | Arcadyan `6j01` | **MT7986A** (Filogic 830) | Quad Cortex-A53 2.0 GHz | MT7976C 4x4 (2.4G) + 4x4 (5G) | MT7531AE (4x GbE) | **OFFICIALLY_SUPPORTED** (PR 25122, 25.12.6) |
| **JIDU6201** | JioFiber AX3000 | Arcadyan `6j02` | **MT7981B** (Filogic 820) | Dual Cortex-A53 1.3 GHz | MT7976CN 2x2 (2.4G) + 3x3 (5G) | MT7531AE (3x GbE) | **COMMUNITY_VERIFIED** (Active snapshot ports) |
| **JIDU6401** | Jio AirFiber Gateway | Unconfirmed ODM | Unverified | Unverified | Unverified | Unverified | **UNVERIFIED** (Do NOT attempt to flash JIDU6101 images) |
| **JIDU6601** | Jio AirFiber Ultra | Unconfirmed ODM | Unverified | Unverified | Unverified | Unverified | **UNVERIFIED** (Do NOT attempt to flash JIDU6101 images) |
| **JIDU6701** | Jio AirFiber 5G CPE | Unconfirmed ODM | Unverified | Unverified | Unverified | Unverified | **UNVERIFIED** (Do NOT attempt to flash JIDU6101 images) |

---

## 2. JIDU6101 (`6j01`) Detailed Hardware Architecture

The Arcadyan-manufactured JIDU6101 is one of the highest-specification consumer gateways deployed in South Asia:

```text
               +---------------------------------------------------+
               |        MediaTek MT7986A (Filogic 830 SoC)         |
               |        4x ARM Cortex-A53 Cores @ 2.0 GHz          |
               |       Hardware PPE v2 + WED v2 Flow Offload       |
               +------------------------+--------------------------+
                                        |
           +----------------------------+----------------------------+
           |                            |                            |
+----------+---------+       +----------+----------+       +---------+---------+
|   512 MB DDR4 RAM  |       |   256 MB SPI-NAND   |       |   USB 3.0 Type-A  |
|  (Samsung / Winbond|       | (ESMT / Winbond UBI)|       |   (Storage/Dongle)|
+--------------------+       +---------------------+       +-------------------+
           |                            |                            |
+----------+---------+       +----------+----------+       +---------+---------+
|   MT7976C 2.4 GHz  |       |    MT7976C 5.0 GHz  |       | MediaTek MT7531AE |
|  4x4:4 Wi-Fi 6 AX  |       |   4x4:4 Wi-Fi 6 AX  |       | 5-Port GbE Switch |
|   Up to 1148 Mbps  |       |   Up to 4804 Mbps   |       | (1x WAN, 3x LAN)  |
+--------------------+       +---------------------+       +-------------------+
```

### Key Hardware Characteristics
- **Upstream Device Profile**: `jiorouter_ax6000-jidu6101`
- **Device Tree File**: `mt7986a-jiorouter-ax6000-jidu6101.dts`
- **SPI-NAND Partition Mapping**:
  - `0x00000000 - 0x00100000`: `BL2` (ATF stage 2)
  - `0x00100000 - 0x00400000`: `u-boot-env` (Boot environment variables)
  - `0x00400000 - 0x00800000`: `factory` (Calibration & MAC addresses)
  - `0x00800000 - 0x00c00000`: `FIP` (BL31 / U-Boot payload)
  - `0x00c00000 - 0x10000000`: `ubi` (Root filesystem and kernel volume)

---

## 3. Stock Firmware Safeguards & Flashing Method

Stock Arcadyan firmware releases enforce Firmware Downgrade Protection (FDP) and encrypted cryptographic validation through an internal utility named `jcrypt`. 

### The Two-Stage Upgrade Requirement
Official OpenWrt PR 25122 fixed SPI-NAND pin pull-up/pull-down configuration registers. Direct one-step flashing from stock can soft-brick the device if old July factory images are used. The verified path uses a safe two-stage process:

1. **Unlock & Temporary Factory Stage**: A RAM-backed initramfs factory kernel is loaded into memory, booting an isolated OpenWrt session at `192.168.1.1` without modifying the permanent NAND boot chain.
2. **Permanent Sysupgrade**: Once running the temporary factory stage, the official permanent squashfs sysupgrade image (`openwrt-25.12.6-mediatek-filogic-jiorouter_ax6000-jidu6101-squashfs-sysupgrade.bin`) is flashed using `sysupgrade -n /tmp/firmware.bin`.

---

## 4. Hardware LED Telemetry Path

The JIDU6101 motherboard features three dedicated tri-color status LEDs mapped directly to Linux sysfs:

```text
Red Status LED:   /sys/class/leds/red:status/brightness   (0 = off, 1 = solid warning)
Green Status LED: /sys/class/leds/green:status/trigger    (none, default-on, heartbeat)
Blue Status LED:  /sys/class/leds/blue:status/brightness  (0 = off, 1 = backup WAN active)
```

By default in OpenWrt, the Green LED is attached to the `heartbeat` trigger, pulsing rhythmically to denote normal Linux kernel execution. During failover events, `/etc/mwan3.user` drives the Blue LED to signify that cellular backup routing is engaged.

---

## 5. Serial UART Teardown & Pinout

For development or recovery from a damaged bootloader:
- **Location**: Unpopulated 4-pin header located near the main SoC thermal shield.
- **Pinout (Pin 1 to Pin 4)**: `VCC (3.3V)`, `TX`, `RX`, `GND`
- **UART Parameters**: `115200 baud`, `8 data bits`, `no parity`, `1 stop bit`, `no flow control`.
- **Logic Level**: Strict `3.3V TTL`. Connecting a 5V TTL FTDI adapter will damage the MT7986A UART GPIO transceiver.
