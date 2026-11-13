# Network Topologies & Configuration

This guide explains how OpenWrt manages network interfaces on the MediaTek MT7986, comparing standalone gateway routing with Wi-Fi repeater topologies and detailing common subnet routing hazards.

---

## 1. Network Topologies Compared

```mermaid
flowchart LR
    subgraph Standalone Gateway Mode [Topology A: Dedicated Ethernet Gateway (Recommended)]
        ISP1["ISP Modem / ONT"] -->|"Ethernet WAN (eth1)"| R1["MT7986 OpenWrt Gateway"]
        R1 -->|"DSA GbE (lan1-4)"| PC1["LAN Ethernet Clients"]
        R1 -->|"Wi-Fi 6 AP (HE160)"| Mob1["Wireless Clients"]
    end

    subgraph Repeater Mode [Topology B: Wireless Repeater / WISP Client]
        UpAP["Upstream Wi-Fi AP"] -.->|"2.4GHz / 5GHz STA (wwan)"| R2["MT7986 OpenWrt Repeater"]
        R2 -->|"DSA GbE (lan1-4)"| PC2["LAN Ethernet Clients"]
        R2 -->|"Wi-Fi AP"| Mob2["Local Wireless Clients"]
    end
```

---

## 2. Dedicated Ethernet Gateway Configuration (Recommended)

In standalone gateway mode:
- **WAN Port (`eth1`)**: Connected via Ethernet to your ISP modem or ONT. Receives an IP via DHCP, static assignment, or PPPoE.
- **LAN Bridge (`br-lan`)**: Bridges physical DSA switch ports `lan1`, `lan2`, `lan3`, and `lan4` alongside local Wi-Fi AP interfaces (`phy0-ap0`, `phy1-ap0`).
- **Full Duplex Routing**: Transmit and receive paths operate independently without half-duplex wireless backhaul contention.

### Configuring PPPoE on WAN
If your ISP requires PPPoE authentication:

```sh
uci set network.wan.proto='pppoe'
uci set network.wan.username='<YOUR_PPPoE_USERNAME>'
uci set network.wan.password='<YOUR_PPPoE_PASSWORD>'
uci commit network
/etc/init.d/network restart
```

---

## 3. Wi-Fi Repeater Mode (WISP) & Subnet Conflict Hazard

When configured as a Wi-Fi repeater, the router connects to an upstream access point via a client station interface (`wwan` / `sta`) while simultaneously serving local LAN and AP clients.

### The Subnet Collision Problem:
A critical configuration pitfall occurs if the upstream router operates on the standard `192.168.1.0/24` subnet (gateway `192.168.1.1`), and the OpenWrt router's default LAN is **also** `192.168.1.0/24` (`192.168.1.1`):

```text
[Upstream AP: 192.168.1.1] 
         │
         ▼ (Repeater WAN receives: 192.168.1.21/24, Default Gateway: 192.168.1.1)
[OpenWrt Repeater]
         │
         ▼ (Local LAN configured: 192.168.1.1/24)
[Local Clients: 192.168.1.100 - 192.168.1.250]
```

#### Symptoms of Overlapping Subnets:
- Up to 60% ICMP packet loss to external internet addresses.
- ARP table collision: the kernel cannot determine whether packets destined for `192.168.1.1` belong to the local bridge (`br-lan`) or the upstream gateway (`phy0-sta0`).
- Highly erratic DNS lookups and intermittent connection drops.

### The Solution: Change Local LAN Subnet
If operating in repeater mode, change the local OpenWrt LAN subnet to a distinct address space (such as `192.168.31.0/24` or `10.10.1.0/24`):

```sh
# [Router SSH]
uci set network.lan.ipaddr='192.168.31.1'
uci commit network
/etc/init.d/network restart
```

*(After changing LAN IP, renew your computer's DHCP lease or reconnect the Ethernet cable to access the router at `192.168.31.1`)*.
