# Router Hardware Identification Guide: SoC, Flash, Switch & Revisions

Before downloading firmware or attempting to flash any device, accurate hardware identification is mandatory. Minor OEM revisions (e.g. `v1` vs `v2`, or `A1` vs `B1`) frequently swap the underlying SoC, replace SPI-NOR flash with SPI-NAND, or switch between Gigabit PHYs.

---

## 1. Non-Destructive Software Inspection (Stock Firmware & Diagnostics)

When serial or telnet/SSH access is available on OEM firmware, extract the exact hardware identity without opening the router casing:

### Inspect Linux Kernel CPU & SoC Architecture
```sh
cat /proc/cpuinfo
```
Look for:
- `model name` / `Hardware`: Identifies ARM core (e.g. `ARMv8 Processor rev 4 (v8l)`) or MIPS core (e.g. `MIPS 1004Kc V2.15`).
- `Features`: Check for `fp`, `asimd`, `aes`, `sha1`, `sha2` indicating modern 64-bit ARM crypto acceleration.

### Inspect Total System Memory (RAM)
```sh
cat /proc/meminfo | grep MemTotal
```
Common mappings:
- `~128 MB`: ~124,000 kB (Budget entry routers)
- `~256 MB`: ~250,000 kB (Mid-tier Wi-Fi 5/6)
- `~512 MB`: ~505,000 kB (High-performance Wi-Fi 6 e.g. MT7986)
- `~1024 MB`: ~1,010,000 kB (Prosumer e.g. GL-MT6000, AX9000)

### Inspect Flash Storage Architecture
```sh
cat /proc/mtd
```
Analyze partition sizes to distinguish flash type:
- **SPI-NOR Flash (16 MB - 32 MB)**: Blocks typically `00010000` (64 KB erase size).
- **SPI-NAND Flash (128 MB - 256 MB)**: Blocks typically `00020000` (128 KB erase size) with UBI containers (`ubi` or `ubifs`).
- **eMMC / SD Card (4 GB - 32 GB)**: Listed under `/proc/partitions` as `mmcblk0` or `mmcblk0p1` rather than MTD partitions.

---

## 2. Physical Teardown & PCB Component Identification

When software inspection is unavailable or uncertain, inspect the physical circuit board:

```text
+-------------------------------------------------------------------+
|                           ROUTER PCB                              |
|                                                                   |
|   +-------------------+                     +-----------------+   |
|   |   Main SoC IC     |                     |  RAM Memory     |   |
|   |  MediaTek MT7986A |                     |  Samsung/Micron |   |
|   |   (Thermal Pad)   |                     |  DDR3/DDR4 BGA  |   |
|   +-------------------+                     +-----------------+   |
|                                                                   |
|   +-------------------+                     +-----------------+   |
|   |   RF Transceiver  |                     |  Flash Storage  |   |
|   |   MT7976C (5 GHz) |                     |  Winbond/ESMT   |   |
|   +-------------------+                     |  8-Pin SOP8 /   |   |
|                                             |  WSON8 Package  |   |
|   +-------------------+                     +-----------------+   |
|   |   Switch / PHY    |                                           |
|   |   MT7531AE        |      [o o o o] UART Header                |
|   +-------------------+      GND TX RX VCC                        |
+-------------------------------------------------------------------+
```

### Decoding Component Markings
1. **SoC Silicon**:
   - `MediaTek MT7986AV / MT7986AN`: Filogic 830 Quad-core ARM Cortex-A53 2.0 GHz.
   - `MediaTek MT7981BA / MT7981BV`: Filogic 820 Dual-core ARM Cortex-A53 1.3 GHz.
   - `MediaTek MT7621AT / DAT`: Dual-core MIPS 880 MHz with integrated Gigabit switch.
   - `Qualcomm IPQ8072A / IPQ8074`: Hawkeye Quad-core ARM Cortex-A53 2.2 GHz.
2. **Flash Storage Chips**:
   - `W25Q128...` / `MX25L128...`: 128 Mbit (16 Megabyte) SPI-NOR.
   - `W25N01GV...` / `GD5F1GQ4...`: 1 Gbit (128 Megabyte) SPI-NAND.
   - `W25N02GV...` / `F50L2G41...`: 2 Gbit (256 Megabyte) SPI-NAND.
   - `KLM8G1GETF...` / `EMMC08G...`: 8 Gigabyte eMMC BGA.

---

## 3. FCC ID Database Cross-Referencing

Every wireless router certified for sale in the United States carries an FCC ID printed on the bottom label (e.g. `FCC ID: MSQ-RTAX59U`).

Search the official FCC database (`https://fccid.io`):
- **Internal Photos**: High-resolution photography of the bare PCB without thermal shields.
- **Test Reports**: Exact RF power output, antenna gain, and frequency ranges.
- **Operational Description**: Block diagrams detailing bus interconnections (PCIe, SGMII, RGMII, SPI).
