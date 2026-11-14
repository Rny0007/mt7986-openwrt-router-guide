# Disaster Recovery Guide: TFTP Automated Recovery & UART Serial Unbricking

When an improper firmware image is flashed or bootloader configuration is corrupted, OpenWrt routers can become unreachable over standard IP networking. This guide provides verified, safe recovery procedures to restore full functionality without damaging the hardware.

---

## 1. Hierarchy of Recovery Modes

```text
Level 1: Safe Mode (First 2 seconds of boot, failsafe network active at 192.168.1.1)
   ↓ (If kernel panics or boot loop occurs)
Level 2: Automated TFTP Client Mode (Bootloader polls static TFTP server on LAN)
   ↓ (If TFTP does not trigger)
Level 3: U-Boot Web Failsafe GUI (Hold reset button during power-on)
   ↓ (If bootloader environment or partitions are corrupt)
Level 4: Hardware UART Serial Console (Direct 3.3V TTL terminal control)
   ↓ (If flash memory is completely erased or damaged)
Level 5: Hardware SPI/NAND Flash Programmer (External CH341A / T48 SOIC clip)
```

---

## 2. Level 1: OpenWrt Failsafe Mode

If the router boots OpenWrt but the web interface (LuCI) or custom network settings prevent SSH access:

1. Disconnect all cables except an Ethernet cable between your computer and router **LAN1**.
2. Set your computer's static IP to `192.168.1.2`, netmask `255.255.255.0`, gateway `192.168.1.1`.
3. Power-cycle the router. As soon as the status LED begins flashing rapidly, press the physical **RESET** button once.
4. From your terminal:
   ```sh
   ssh -o StrictHostKeyChecking=no root@192.168.1.1
   ```
5. Once logged into the failsafe ash shell:
   ```sh
   # Revert all user configuration to clean defaults
   firstboot -y
   reboot -f
   ```

---

## 3. Level 2: Automated TFTP Bootloader Recovery

Many modern MediaTek and Qualcomm bootloaders automatically broadcast TFTP requests if the root partition cannot be mounted or if the reset button is held down during power-on.

### Standard OEM TFTP Recovery IP Defaults

| Vendor / Platform | Router IP Expected | TFTP Server IP (Your PC) | Required File Name |
| :--- | :--- | :--- | :--- |
| **MediaTek Filogic (U-Boot)** | `192.168.1.1` | `192.168.1.254` | `recovery.bin` or `openwrt.bin` |
| **TP-Link MediaTek** | `192.168.0.1` | `192.168.0.66` | `ArcherC6v3_tp_recovery.bin` |
| **Xiaomi / Redmi (miwifi)** | `192.168.31.1` | `192.168.31.100` | `test.bin` |
| **Netgear MediaTek** | `192.168.1.1` | `192.168.1.10` | `wax206.img` |

### Configuring the TFTP Server (Windows & Linux)

#### On Linux:
```sh
sudo apt install tftpd-hpa
sudo cp openwrt-*-initramfs-recovery.bin /var/lib/tftpboot/recovery.bin
sudo systemctl restart tftpd-hpa
```

#### On Windows (via Tftpd64):
1. Download official portable `Tftpd64`.
2. Configure your Ethernet adapter to the static IP required by the router (e.g. `192.168.1.254`).
3. Point Tftpd64 "Current Directory" to the folder containing your recovery kernel.
4. Power on the router while holding the RESET button for 8-10 seconds until the TFTP server log indicates file transfer.

---

## 4. Level 4: UART Serial Terminal De-Bricking

When the bootloader fails to initialize networking, physical UART serial access provides direct low-level terminal debugging.

### Wiring Safety Protocol

> [!CAUTION]
> Never connect the `VCC (3.3V or 5V)` pin from your USB-UART adapter to the router PCB. Doing so can cause cross-power contention between the router power supply and your PC's USB port, burning out the SoC. Connect ONLY: `GND`, `TX`, and `RX`.

```text
USB-UART Adapter                Router PCB Header
[ GND ] ------------------------ [ GND ]
[ RX  ] ------------------------ [ TX  ] (Crossover!)
[ TX  ] ------------------------ [ RX  ] (Crossover!)
[ VCC ] (DISCONNECTED)           [ VCC ] (DISCONNECTED)
```

### Serial Session Connection

#### Using PuTTY (Windows):
- Connection Type: `Serial`
- Serial line: `COM3` (check Windows Device Manager)
- Speed (baud): `115200` (or `1500000` for Rockchip RK3568)
- Data bits: `8`, Stop bits: `1`, Parity: `None`, Flow control: `None`

#### Using Minicom (Linux / macOS):
```sh
picocom -b 115200 -d 8 -p n -f n /dev/ttyUSB0
```

### Interrupting U-Boot & Flashing from RAM

1. Power on the router. As serial text begins streaming, immediately press `Space` or `Enter` repeatedly to drop into the U-Boot prompt:
   ```text
   MediaTek> 
   ```
2. Configure U-Boot network parameters:
   ```text
   setenv ipaddr 192.168.1.1
   setenv serverip 192.168.1.254
   ping 192.168.1.254
   ```
3. Load the recovery kernel into RAM:
   ```text
   tftpboot 0x46000000 openwrt-initramfs.bin
   bootm 0x46000000
   ```
4. The router boots directly from RAM into a live OpenWrt session. From there, execute permanent sysupgrade:
   ```sh
   sysupgrade -n /tmp/openwrt-squashfs-sysupgrade.bin
   ```
