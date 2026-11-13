# Wi-Fi 6 (802.11ax) Configuration & Optimization

This guide explains how to configure and tune the dual-band Wi-Fi 6 subsystem on MediaTek MT7986 routers using the upstream `mt76` wireless driver.

---

## 1. Hardware Architecture Overview

MediaTek MT7986 platforms typically integrate the MT7976C RF companion transceiver:

| Radio | Physical Node | Supported Bands | Channel Widths | Antennas / Streams | Max PHY Rate |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **`radio0`** | `18000000.wifi` | 2.4 GHz (802.11b/g/n/ax) | 20 MHz, 40 MHz | 4x4 MIMO | 1148 Mbps |
| **`radio1`** | `18000000.wifi+1` | 5.0 GHz (802.11a/n/ac/ax) | 20, 40, 80, **160 MHz** | 4x4 MIMO | 4804 Mbps |

---

## 2. Setting Regulatory Domain (Country Code)

By default, an unset regulatory domain (`country '00'`) enforces restrictive worldwide defaults:
- Maximum transmit power is capped at **20 dBm** (100 mW).
- High-bandwidth DFS channels in 5 GHz may be disabled or restricted.

### Setting Regional Regulatory Domain (Example: India `IN`):
Configuring your official country code unlocks legally permitted transmit powers and frequencies:

```sh
# [Router SSH]
uci set wireless.radio0.country='IN'
uci set wireless.radio1.country='IN'
uci commit wireless
wifi reload
```

#### Verification via `iw`:
```sh
iw reg get
```
Under India (`IN`), legally compliant transmit power increases up to **30 dBm** (1000 mW), significantly improving link budget and coverage.

---

## 3. Enabling 160 MHz Channel Width on 5 GHz (HE160)

The MT7986 supports ultra-wide 160 MHz channels on 5 GHz, doubling peak throughput for Wi-Fi 6 clients (smartphones, laptops) from 1201 Mbps (at 80 MHz) to **2402 Mbps** (at 160 MHz 2x2):

```sh
# Set 5GHz radio to HE160 on non-DFS channel 36
uci set wireless.radio1.channel='36'
uci set wireless.radio1.htmode='HE160'
uci commit wireless
wifi reload
```

Verify the active channel and width:
```sh
iwinfo phy1-ap0 info
```

---

## 4. Wireless Security: WPA3 SAE / WPA2 Mixed Mode

For maximum security with legacy device compatibility:

```sh
# Configure WPA3 SAE with WPA2-PSK fallback (sae-compat)
uci set wireless.default_radio1.encryption='sae-compat'
uci set wireless.default_radio1.key='<YOUR_STRONG_WIFI_PASSWORD>'
uci commit wireless
wifi reload
```

---

## 5. Preventing Scanning Latency from Dormant Interfaces

If you previously configured multiple client station interfaces (e.g. for phone hotspots), `mac80211` periodically cycles through background scanning to discover missing APs, causing packet loss and rate drops on active links.

### Safe Practice:
Disable unused client interfaces:

```sh
uci set wireless.<interface_name>.disabled='1'
uci commit wireless
wifi reload
```
Removing dormant interfaces preserves airtime and prevents rate-control throttling.
