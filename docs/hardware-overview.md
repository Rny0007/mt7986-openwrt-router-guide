# MediaTek MT7986 (Filogic 830) Hardware Architecture

This document details the hardware architecture, internal bus topology, chipsets, and peripheral interfaces found on the MediaTek MT7986 platform, using the JIDU6101 (`6j01`) reference design as a primary technical case study.

---

## 1. System-on-Chip (SoC) Overview

The MediaTek MT7986A is an enterprise-grade network processor featuring:

- **Processor Cores**: Quad-core ARM Cortex-A53 running up to 2.0 GHz.
- **ISA**: ARMv8-A (64-bit `aarch64`).
- **L1 Cache**: 32 KB I-Cache + 32 KB D-Cache per core.
- **L2 Cache**: 512 KB unified cache.
- **Hardware Acceleration Engine**:
  - **PPE (Packet Processing Engine)**: Hardware NAT, flow offloading, and QoS packet classification capable of handling multi-gigabit line-rate routing without CPU intervention.
  - **Security Cryptographic Engine**: Hardware AES, SHA, and HMAC acceleration (utilized by WireGuard and IPsec).

---

## 2. Memory and Flash Subsystems

### System RAM
- **Capacity**: 512 MB DDR3 / DDR4 SDRAM.
- **Bus Width**: 16-bit / 32-bit with ECC support.
- **Kernel Mapping**: Mapped from `0x40000000` to `0x60000000`.

### Flash Storage
- **Type**: 256 MB SPI NAND Flash.
- **Chip Identifier**: Typically Winbond `W25N02KV` or Macronix `MX35LF2GE4AB`.
- **Interface**: High-speed SPI (`10015000.spi`).
- **NAND Geometry**:
  - Total Size: 268,435,456 bytes (256 MiB).
  - Block Size (Erase Size): 131,072 bytes (128 KiB).
  - Page Size (Write Size): 2,048 bytes (2 KiB).
  - OOB (Out-of-Band) Spare Area: 64 / 128 bytes per page for ECC parity.

---

## 3. Ethernet & Switch Architecture

The MT7986A integrates two multi-rate Ethernet MACs connected via HSGMII / SGMII at up to 2.5 Gbps:

```text
+--------------------------------------------------------------+
|                    MediaTek MT7986A SoC                      |
|                                                              |
|   +-----------------------+      +-----------------------+   |
|   |   GMAC1 (HSGMII)      |      |   GMAC2 (HSGMII)      |   |
|   |   2500 Mbps Bus       |      |   2500 Mbps Bus       |   |
|   +-----------+-----------+      +-----------+-----------+   |
+---------------|------------------------------|---------------+
                |                              |
                v                              v
    +-----------------------+      +-----------------------+
    |   MT7531AE Switch     |      |   External 2.5G PHY   |
    |   (LAN 1 - 4 GbE)     |      |   (WAN Port / eth1)   |
    +-----------------------+      +-----------------------+
```

### MediaTek MT7531AE Switch
- Connected to GMAC1 over internal HSGMII at 2.5 Gbps (`eth0`).
- Implemented in Linux as a **DSA (Distributed Switch Architecture)** device:
  - `lan1` (GbE)
  - `lan2` (GbE)
  - `lan3` (GbE)
  - `lan4` (GbE)
- All LAN switch ports are dynamically bridged under `br-lan`.

---

## 4. Wireless RF Subsystem (MT7976C)

Wireless capability is delivered by the MediaTek MT7976C companion RF transceiver chip communicating via dedicated high-speed AXI / PCIe buses (`18000000.wifi`):

- **2.4 GHz Radio (`phy0`)**:
  - 4x4 MIMO 802.11ax / 802.11n.
  - Channel width: 20 MHz / 40 MHz (HT20, HT40, HE20, HE40).
  - Maximum theoretical PHY rate: 1148 Mbps (at 40 MHz, MCS 11, 4 streams).
- **5.0 GHz Radio (`phy1`)**:
  - 4x4 MIMO 802.11ax / 802.11ac.
  - Channel width: 20 MHz, 40 MHz, 80 MHz, and full **160 MHz** (HE160).
  - Maximum theoretical PHY rate: 4804 Mbps (at 160 MHz, MCS 11, 4 streams).
- **Aggregate Rating**: AX6000 Wi-Fi 6.

---

## 5. Pin Multiplexing (Pinctrl) & GPIO Assignments

The MediaTek MT7986 Moore pin controller (`1001f000.pinctrl-pinctrl_moore`) exposes 101 GPIO lines (`gpiochip0`, offsets 512–612 in modern kernels):

### Verified Front-Panel Status LED Mappings (JIDU6101 / `6j01`):
| Color Channel | Device Tree Node | Hardware Pin Index | Linux GPIO | Physical Polarity | Trigger Driver |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **RED** | `led-0` | Pin 12 (`GPIO_7`) | `gpio-524` | `GPIO_ACTIVE_LOW` (0V = ON) | `leds-gpio` |
| **GREEN** | `led-1` | Pin 13 (`GPIO_8`) | `gpio-525` | `GPIO_ACTIVE_LOW` (0V = ON) | `leds-gpio` |
| **BLUE** | `led-2` | Pin 14 (`GPIO_9`) | `gpio-526` | `GPIO_ACTIVE_LOW` (0V = ON) | `leds-gpio` |

### Dedicated PHY LEDs:
- 2.4 GHz Activity: Pin 1 (`WF2G_LED`) driven directly by `18000000.wifi` (`mt76-phy0`).
- 5.0 GHz Activity: Pin 2 (`WF5G_LED`) driven directly by `18000000.wifi` (`mt76-phy1`).

---

## 6. Serial Debug Header (UART)

For low-level bootloader access and serial unbricking:
- **Voltage Level**: **3.3V TTL** (Never connect a 5V RS-232 adapter).
- **Baud Rate**: `115200`
- **Data Bits**: `8`
- **Parity**: `None`
- **Stop Bits**: `1`
- **Flow Control**: `None`
- **Header Pinout**: Typically labeled `TX`, `RX`, `GND` adjacent to the MT7986 shielding can.
