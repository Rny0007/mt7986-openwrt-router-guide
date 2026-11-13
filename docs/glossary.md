# Technical Glossary

This glossary defines key networking, embedded Linux, hardware, and OpenWrt terminology used throughout this documentation.

---

### AdGuard Home
An open-source, network-wide ad-blocking and privacy software application that acts as a local DNS forwarding and sinkholing server.

### ARM Cortex-A53
A 64-bit multi-core processor core developed by ARM implementing the ARMv8-A architecture. The MediaTek MT7986 utilizes four Cortex-A53 cores clocked up to 2.0 GHz.

### Device Tree (DTS / DTB)
A standardized data structure used by the Linux kernel to describe hardware components (GPIOs, pin multiplexers, clocks, interrupt lines, PHYs, and memory-mapped peripherals) without hardcoding values in driver binaries.

### Distributed Switch Architecture (DSA)
A Linux kernel subsystem treating individual physical switch ports on embedded hardware (e.g. `lan1`–`lan4`) as independent network interfaces managed by the operating system rather than opaque hardware bridges.

### DNSSEC (DNS Security Extensions)
A suite of cryptographic extensions to the Domain Name System authenticating DNS response integrity and origin authenticity, protecting clients against forged responses.

### DNS-over-HTTPS (DoH)
A network protocol for performing domain lookups via the encrypted HTTPS protocol (RFC 8484) on port 443, preventing third-party transit interception and logging.

### Filogic 830
MediaTek's brand name for its MT7986 Wi-Fi 6 router SoC family.

### FIT (Flattened Image Tree)
A flexible firmware image format used by U-Boot encapsulating kernel, ramdisk, device tree blobs, and cryptographic RSA/SHA signatures into a single image.

### Flow Offloading (Hardware / Software)
A Linux firewall feature that bypasses standard per-packet routing table traversals for established streams, handing packets off directly to network drivers or hardware silicon engines (PPE).

### Initramfs
An initial ramdisk root filesystem packed into the Linux kernel binary and loaded directly into RAM, allowing recovery without mounting flash storage.

### LuCI
The Lua- and JavaScript-based web management interface standard in official OpenWrt installations.

### MediaTek MT7986A
The flagship quad-core 64-bit Wi-Fi 6 router SoC powering enterprise and consumer AX6000 routers.

### OpenWrt
An open-source Linux operating system designed for embedded wireless routers, gateways, and network appliances.

### Packet Processing Engine (PPE)
A dedicated silicon block inside MediaTek network processors that performs line-rate hardware NAT, bridging, and flow routing.

### SPI-NAND Flash
High-capacity serial flash storage communicating over a Serial Peripheral Interface (SPI), standard in modern 256MB+ routers.

### Sysupgrade
OpenWrt's native firmware upgrade utility that validates checksums, formats flash volumes, and seamlessly transitions kernel and root filesystems.

### UBI / UBIFS (Unsorted Block Images)
A wear-leveling flash management subsystem and fault-tolerant filesystem specifically designed for raw flash memory chips (NAND/NOR).

### WISP / Repeater Mode
Wireless Internet Service Provider mode, where a router connects wirelessly to an upstream access point as a client while simultaneously serving local network devices.
