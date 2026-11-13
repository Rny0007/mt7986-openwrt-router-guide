# Physical Status LED Configuration & Hardware Triggers

This document explains the physical front-panel status LED architecture for MediaTek MT7986 routers, detailing the exact configuration verified on the JIDU6101 (`6j01`) reference hardware.

---

## 1. Hardware Pin Multiplexing & Driver Architecture

On the JIDU6101 reference design, the tri-color RGB status LED is driven directly by the Linux `leds-gpio` kernel driver via the MediaTek Moore pin controller (`1001f000.pinctrl-pinctrl_moore`):

| Color Channel | Sysfs Path | DT Node | Linux GPIO | Physical Pin Index | Polarity in Device Tree |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **RED** | `/sys/class/leds/red:status` | `led-0` | `gpio-524` | Pin 12 (`GPIO_7`) | `GPIO_ACTIVE_LOW` |
| **GREEN** | `/sys/class/leds/green:status` | `led-1` | `gpio-525` | Pin 13 (`GPIO_8`) | `GPIO_ACTIVE_LOW` |
| **BLUE** | `/sys/class/leds/blue:status` | `led-2` | `gpio-526` | Pin 14 (`GPIO_9`) | `GPIO_ACTIVE_LOW` |

---

## 2. Root Cause Analysis: LuCI Trigger Ordering

During initial migration, front-panel LEDs appeared dark despite successful `/sys/class/leds/` brightness writes. Diagnostic investigation confirmed:
1. The hardware pins and electrical connections were fully functional.
2. The initial inactivity was caused by **action ordering and trigger conflicts** inside LuCI's `/etc/config/system` mapping.
3. Correcting the triggers and action sequence directly inside LuCI restored visible physical blinking immediately without requiring any custom kernel patches or background polling daemons.

---

## 3. Exact Verified Working Configuration

The following table documents the exact configuration verified in LuCI and physically observed on hardware:

| LED Action Name | LED Sysfs Path | Assigned Trigger | Trigger Parameters & Modes |
| :---: | :---: | :---: | :--- |
| **`red`** | `red:status` | `none` | Default state: `0`, Interval: `1` |
| **`blue`** | `blue:status` | `netdev` | Device: `eth0`, Interval: `10`, Modes: `link_10000`, `half_duplex`, `full_duplex` |
| **`green`** | `green:status` | `heartbeat` | Interval: `10`, Inverted: `1` |

### UCI Configuration Block (`/etc/config/system`):
```uci
config led
	option name 'red'
	option sysfs 'red:status'
	option trigger 'none'
	option interval '1'
	option default '0'

config led
	option name 'blue'
	option sysfs 'blue:status'
	option trigger 'netdev'
	option interval '10'
	option dev 'eth0'
	list mode 'link_10000'
	list mode 'half_duplex'
	list mode 'full_duplex'

config led
	option name 'green'
	option sysfs 'green:status'
	option trigger 'heartbeat'
	option interval '10'
	option inverted '1'
```

---

## 4. Applying Configuration via LuCI Web Interface

1. In LuCI, navigate to **System** → **LED Configuration**.
2. If existing unverified actions exist, delete them.
3. Click **Add** to create the three entries:
   - **Entry 1**:
     - LED Name: `red`
     - LED Physical Name: `red:status`
     - Trigger: `none`
     - Default state: Unchecked (`0`)
   - **Entry 2**:
     - LED Name: `blue`
     - LED Physical Name: `blue:status`
     - Trigger: `netdev`
     - Device: `eth0`
     - Trigger modes: Check `Link On`, `Transmit`, `Receive`
   - **Entry 3**:
     - LED Name: `green`
     - LED Physical Name: `green:status`
     - Trigger: `heartbeat`
     - Invert: Checked (`1`)
4. Click **Save & Apply**.
5. Physically observe the router front panel: the status LED illuminates steadily with network activity and heartbeat pulses.
