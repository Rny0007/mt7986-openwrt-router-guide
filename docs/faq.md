# Frequently Asked Questions (FAQ)

This document addresses common questions regarding OpenWrt compatibility, MediaTek MT7986 hardware, performance optimization, and recovery.

---

### Q1: Can I install official OpenWrt on the Jio / Arcadyan JIDU6101?
**Yes.** The JIDU6101 (Board ID: `6j01`) is officially supported in OpenWrt 25.12.6 under the target `mediatek/filogic` with profile `jiorouter_ax6000-jidu6101`. Installation can be performed via root SSH access without requiring hardware soldering or opening the enclosure.

---

### Q2: Does OpenWrt support the JIDU6201, JIDU6401, or other JIDU models?
The JIDU6201 shares the core `6j01` board layout and MediaTek MT7986A architecture with the JIDU6101 and is community verified. Other models (such as JIDU6401, 6601, and 6701) share the chipset family but require confirmation of partition maps and bootloader signature checks prior to flashing. Never flash an untested profile without full flash backups.

---

### Q3: Which OpenWrt image should I download for MediaTek MT7986?
Download images matching your exact router profile under the `mediatek/filogic` target. For the JIDU6101, use:
- **Stage 1 (Ramdisk / Factory)**: `openwrt-*-mediatek-filogic-jiorouter_ax6000-jidu6101-factory.ubi`
- **Stage 2 (Permanent Sysupgrade)**: `openwrt-25.12.6-mediatek-filogic-jiorouter_ax6000-jidu6101-squashfs-sysupgrade.bin`

---

### Q4: Are all MT7986 routers compatible with each other's firmware?
**No.** While routers may share the MediaTek MT7986A SoC, vendors use distinct Ethernet switch chips (MT7531AE vs Realtek vs dedicated SFP+ interfaces), different flash types (SPI NAND vs eMMC), and customized pin assignments. Always use device-specific images.

---

### Q5: What is the difference between MT7986 and MT7986A?
The MT7986A is the primary enterprise-tier SoC in the Filogic 830 family, featuring a quad-core 64-bit ARM Cortex-A53 CPU clocked up to 2.0 GHz with dual 2.5 Gbps SGMII interfaces. The MT7986B is a dual-core variant designed for entry-level access points.

---

### Q6: Is Filogic 830 the same as MT7986?
**Yes.** "Filogic 830" is MediaTek's commercial brand name for the MT7986 series chipset platform.

---

### Q7: How do I back up original vendor firmware before flashing?
Connect via root SSH and dump all individual MTD partitions using the `dd` command:
```sh
dd if=/dev/mtd0 of=/tmp/mtd0_fullchip.bin
```
Transfer all partition dumps to your host computer and verify checksums before flashing. See [Backup & Restore](backup-and-restore.md).

---

### Q8: How do I access the OpenWrt LuCI web interface?
Connect your computer to a LAN port via Ethernet, ensure you obtain an IP via DHCP, and navigate to `http://192.168.1.1` in your browser. The default username is `root` with no password on initial boot.

---

### Q9: How do I enable Wi-Fi 6 (802.11ax)?
Wi-Fi 6 is enabled by default in OpenWrt 25.12 when selecting `HE20`, `HE40`, `HE80`, or `HE160` modes under `/etc/config/wireless`. Ensure wireless security is configured with WPA3 SAE or WPA3/WPA2 mixed mode (`sae-compat`).

---

### Q10: How do I enable 160 MHz channel width (HE160) on 5 GHz?
In LuCI under **Network** → **Wireless** → **radio1 (5 GHz)**, set **Operating frequency** to Channel 36 and **Channel width** to **160 MHz** (`HE160`). In CLI, set `uci set wireless.radio1.htmode='HE160'`.

---

### Q11: How do I install AdGuard Home on OpenWrt?
Run `opkg update && opkg install adguardhome`. Move Dnsmasq to port 5353 (`uci set dhcp.@dnsmasq[0].port='5353'`), allowing AdGuard Home to bind port 53. Route local `.lan` queries from AdGuard Home back to `127.0.0.1:5353`. See [AdGuard Home Guide](adguard-home.md).

---

### Q12: How do I configure DNS-over-HTTPS (DoH)?
Inside the AdGuard Home web dashboard (**Settings** → **DNS Settings**), enter encrypted provider URLs such as `https://1.1.1.1/dns-query` and `https://149.112.112.112/dns-query`. AdGuard Home natively handles TLS handshakes and upstream encryption.

---

### Q13: Why was my router's status LED dark, and how was it fixed?
On the JIDU6101 reference unit, the hardware pins were fully functional, but LuCI trigger action conflicts prevented physical illumination. Aligning the triggers (`red` = `none`, `blue` = `netdev eth0`, `green` = `heartbeat`) resolved the issue immediately without custom polling daemons. See [LED Configuration](led-configuration.md).

---

### Q14: How do I recover a router that does not boot?
If the device does not acquire network connectivity, use the 3.3V UART serial debug header to interrupt U-Boot, load an official OpenWrt initramfs kernel into RAM via TFTP, and boot directly into DDR3 memory to repair flash partitions. See [Recovery & Unbrick](recovery-unbrick.md).

---

### Q15: Can I use a Wi-Fi repeater as a standalone Ethernet gateway router?
**Yes.** Simply connect your ISP modem or ONT cable to the dedicated WAN port (`eth1`), configure WAN protocol (DHCP or PPPoE), and disable the wireless repeater client station (`wwan`). This provides full-duplex gigabit routing without wireless backhaul latency.

---

### Q16: How do I eliminate packet loss and speed drops in repeater mode?
1. Ensure your local LAN subnet does not match the upstream AP subnet (change `192.168.1.1` to `192.168.31.1`).
2. Set your legal country code (`country 'IN'`) to unlock full 30 dBm transmit power.
3. Disable unassociated dormant client interfaces to stop background scanning interruptions.

---

### Q17: What is Hardware Flow Offloading and should I enable it?
Hardware Flow Offloading directs established network flows to the MediaTek MT7986 Packet Processing Engine (PPE). Enabling it (`flow_offloading_hw '1'`) allows line-rate multi-gigabit routing with negligible CPU utilization. It should always be enabled on Filogic 830 platforms.
