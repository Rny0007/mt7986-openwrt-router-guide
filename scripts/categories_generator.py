#!/usr/bin/env python3
"""
scripts/categories_generator.py
Generates the 8 search-intent category landing pages and the categories directory hub
for the Global OpenWrt Router Hardware Knowledge Base.
"""

import os
import json

CATEGORIES_META = [
    {
        "slug": "best-openwrt-routers",
        "title": "Best OpenWrt Routers (2024–2026 Curated Hardware Guide)",
        "nav_title": "Best Routers Overall",
        "description": "Comprehensive, evidence-based recommendations for the best OpenWrt routers across Wi-Fi 6, 2.5G multi-gigabit, portable travel, budget, and x86 firewalls.",
        "icon": "🏆",
        "badge": "Curated Top Picks",
        "intro_lead": "Selecting the right router for OpenWrt requires looking beyond retail marketing and examining silicon architecture, wireless driver upstream support, flash capacity, and bootloader accessibility.",
        "criteria": [
            "Official or verified stable OpenWrt community support without proprietary binary blobs.",
            "Modern SoC with hardware crypto (AES/ARMv8 CE) for high-speed WireGuard and OpenVPN.",
            "Adequate flash memory (minimum 128 MB NAND/SPI, preferably 512 MB+) for packages and future upgrades.",
            "Sufficient RAM (minimum 512 MB, recommended 1 GB+) for CAKE SQM, DNS filtering, and Docker/containers.",
            "Open-source wireless driver support (mac80211, mt7915, ath11k) with full DFS and WPA3 compatibility."
        ],
        "device_ids": [
            "jidu6101",
            "gl-inet-gl-mt6000",
            "gl-inet-gl-mt3000",
            "linksys-e8450",
            "turris-omnia",
            "protectli-vault-fw4b",
            "ubiquiti-unifi-6-pro"
        ],
        "highlights": [
            {
                "id": "jidu6101",
                "role": "Best Enterprise Value & Dual 2.5G",
                "verdict": "Unbeatable enterprise-grade MediaTek Filogic 830 hardware with dual 2.5GbE PHYs and 1GB RAM, available at exceptional surplus value."
            },
            {
                "id": "gl-inet-gl-mt6000",
                "role": "Best Flagship Home Router",
                "verdict": "The premier turnkey OpenWrt Wi-Fi 6 router on the market with dual 2.5G ports, quad-core MediaTek Filogic 830, and 1GB DDR4."
            },
            {
                "id": "gl-inet-gl-mt3000",
                "role": "Best Portable & Travel Gateway",
                "verdict": "Ultra-compact pocket router featuring 2.5GbE WAN, MediaTek Wi-Fi 6, captive portal repeater mode, and hardware toggle switch."
            },
            {
                "id": "linksys-e8450",
                "role": "Best Budget Open-Source Wi-Fi 6",
                "verdict": "Proven MediaTek MT7622 architecture with native upstream support and unbrickable recovery via U-Boot TFTP."
            },
            {
                "id": "turris-omnia",
                "role": "Best Open-Hardware & Modular Platform",
                "verdict": "Czech-engineered modular ARM router with SFP cage, dual mini-PCIe slots, hardware crypto, and dedicated recovery modes."
            },
            {
                "id": "protectli-vault-fw4b",
                "role": "Best x86_64 Dedicated Firewall",
                "verdict": "Fanless Intel Celeron appliance with 4 discrete Intel I211-AT gigabit NICs, Coreboot open BIOS, and unlimited package capability."
            }
        ]
    },
    {
        "slug": "wifi-7",
        "title": "Best OpenWrt Wi-Fi 7 Routers: Upstream Status & Hardware Matrix",
        "nav_title": "Wi-Fi 7 (802.11be)",
        "description": "Technical analysis of Wi-Fi 7 (802.11be) router hardware, upstream Linux mac80211/ath12k/mt7996 driver status, and community ports.",
        "icon": "⚡",
        "badge": "Emerging Technology",
        "intro_lead": "Wi-Fi 7 (802.11be) brings Multi-Link Operation (MLO), 320 MHz channel width, and 4096-QAM modulation. Upstream OpenWrt support is currently transitioning from experimental development trees into production snapshots.",
        "criteria": [
            "Silicon vendor Linux driver release strategy: Qualcomm ath12k vs MediaTek mt7996 open drivers.",
            "Hardware revision stability: early v1 Wi-Fi 7 routers frequently change RF frontend chipsets.",
            "Thermal design and cooling: Wi-Fi 7 silicon runs significantly hotter than Wi-Fi 6.",
            "Multi-gigabit wired interconnects: Wi-Fi 7 requires at least 2.5GbE or 10GbE backhaul to prevent wired bottlenecks.",
            "Upstream kernel requirement: OpenWrt with Linux 6.6+ LTS kernel is required for mac80211 802.11be features."
        ],
        "device_ids": [
            "xiaomi-router-7000",
            "tp-link-archer-be800-v1",
            "asus-rt-be96u"
        ],
        "highlights": [
            {
                "id": "xiaomi-router-7000",
                "role": "Most Advanced Community Wi-Fi 7 Port",
                "verdict": "Qualcomm IPQ9554 quad-core architecture with 1GB RAM and quad 2.5GbE ports. Active community OpenWrt builds available via ath12k."
            },
            {
                "id": "tp-link-archer-be800-v1",
                "role": "Flagship 10G Multi-Gig Hardware",
                "verdict": "Qualcomm IPQ9574 platform with dual 10GbE and quad 2.5GbE ports. Bootloader access validated; awaiting upstream device profile."
            },
            {
                "id": "asus-rt-be96u",
                "role": "Proprietary Architecture Warning",
                "verdict": "High-end Broadcom BCM4916 hardware blocked from open-source Wi-Fi due to closed Broadcom wireless drivers."
            }
        ]
    },
    {
        "slug": "wifi-6",
        "title": "Best OpenWrt Wi-Fi 6 Routers: Tested AX3000 to AX6000 Hardware",
        "nav_title": "Wi-Fi 6 (802.11ax)",
        "description": "Curated comparison of top Wi-Fi 6 (802.11ax) routers running upstream OpenWrt. Evaluated for gigabit throughput, SQM QoS, and open-source mt7915/ath11k drivers.",
        "icon": "📶",
        "badge": "Production Sweet Spot",
        "intro_lead": "Wi-Fi 6 (802.11ax) represents the current mature standard for OpenWrt deployments. MediaTek Filogic and Qualcomm IPQ platforms offer 100% open-source wireless drivers with full hardware offload.",
        "criteria": [
            "Fully open-source mac80211 kernel wireless drivers (MediaTek mt7915/mt7986 or Qualcomm ath11k).",
            "True multi-gigabit routing capacity: MediaTek Filogic 830 / 820 or Qualcomm IPQ807x / IPQ60xx.",
            "WPA3-Personal, WPA3-Enterprise, and 802.11w Protected Management Frames support.",
            "Target Wake Time (TWT) and BSS Coloring support for dense client deployments.",
            "Flashing safety: factory firmware vulnerability or unlocked U-Boot bootloader."
        ],
        "device_ids": [
            "jidu6101",
            "gl-inet-gl-mt6000",
            "linksys-e8450",
            "belkin-rt1800",
            "xiaomi-ax3000t",
            "buffalo-wsr-3200ax4s",
            "ubiquiti-unifi-6-pro"
        ],
        "highlights": [
            {
                "id": "jidu6101",
                "role": "Best Value AX6000 Enterprise Router",
                "verdict": "MediaTek MT7986A Filogic 830 with 4x4 MU-MIMO dual-band wireless, 1GB DDR4, dual 2.5G ports, and verified failover configuration."
            },
            {
                "id": "gl-inet-gl-mt6000",
                "role": "Best Retail AX6000 Router",
                "verdict": "Turnkey consumer router with dual 2.5GbE, 8GB eMMC flash, 1GB RAM, and comprehensive open-source driver ecosystem."
            },
            {
                "id": "linksys-e8450",
                "role": "Best AX3200 Budget Workhorse",
                "verdict": "Stable dual-band AX3200 router with 512MB RAM, internal antennas, and pristine upstream OpenWrt integration."
            },
            {
                "id": "xiaomi-ax3000t",
                "role": "Best Ultra-Budget AX3000 Node",
                "verdict": "MediaTek Filogic 820 dual-core platform offering 160 MHz channel width and Wi-Fi 6 speeds under $40 USD."
            },
            {
                "id": "ubiquiti-unifi-6-pro",
                "role": "Best Enterprise Ceiling AP",
                "verdict": "Qualcomm IPQ5018 dual-band access point with 48V PoE 802.3at power input and professional RF engineering."
            }
        ]
    },
    {
        "slug": "travel-routers",
        "title": "Best OpenWrt Travel Routers: Portable Gateways for Secure Wi-Fi",
        "nav_title": "Travel & Pocket Gateways",
        "description": "Top portable OpenWrt travel routers for hotel captive portal bypass, encrypted WireGuard VPN tunnels, cellular USB tethering, and Wi-Fi repeating.",
        "icon": "✈️",
        "badge": "Mobile Privacy",
        "intro_lead": "Public Wi-Fi at airports, hotels, and cafes exposes traffic to snooping and requires tedious captive portal authentication on every single device. A portable OpenWrt travel router creates a personal, encrypted bubble for all your devices.",
        "criteria": [
            "Compact physical form factor and low power consumption (USB-C 5V/3A input).",
            "Dual-band Wi-Fi with independent radios to repeat upstream public Wi-Fi while broadcasting private LAN SSID simultaneously without halving bandwidth.",
            "Hardware VPN toggle switch to instantly engage WireGuard or OpenVPN tunnels.",
            "USB 3.0 or 2.0 port for 4G/5G smartphone USB tethering.",
            "Extensible storage (MicroSD card or external USB drive) for local file sharing and offline media streaming."
        ],
        "device_ids": [
            "gl-inet-gl-mt3000",
            "gl-inet-gl-axt1800",
            "gl-inet-gl-ar750s",
            "gl-inet-gl-ar300m16",
            "gl-inet-gl-sft1200"
        ],
        "highlights": [
            {
                "id": "gl-inet-gl-mt3000",
                "role": "Best Overall Travel Router (Beryl AX)",
                "verdict": "MediaTek Filogic 820 Wi-Fi 6, 2.5GbE WAN, 512MB RAM, USB 3.0, and foldable antennas make it the definitive modern travel companion."
            },
            {
                "id": "gl-inet-gl-axt1800",
                "role": "Best High-Throughput Travel Router (Slate AX)",
                "verdict": "Qualcomm IPQ6000 quad-core processor with active fan cooling, 3x gigabit ports, and up to 550 Mbps WireGuard VPN client speeds."
            },
            {
                "id": "gl-inet-gl-ar750s",
                "role": "Best Proven Legacy Travel Router (Slate)",
                "verdict": "Qualcomm QCA9563 dual-band AC750 router with MicroSD slot and extremely low power draw."
            },
            {
                "id": "gl-inet-gl-ar300m16",
                "role": "Best Micro Pocket Node (Shadow)",
                "verdict": "Matchbox-sized single-band 2.4GHz router powered by 5V USB, perfect as a lightweight network probe or dedicated VPN bridge."
            }
        ]
    },
    {
        "slug": "mesh-systems",
        "title": "Best OpenWrt Mesh Wi-Fi Systems: 802.11s & EasyMesh Hardware",
        "nav_title": "Mesh & Whole-Home Wi-Fi",
        "description": "Evidence-based hardware guide for building reliable, whole-home OpenWrt mesh networks. Covers 802.11s wireless mesh, 802.11k/v/r fast roaming, and wired backhaul.",
        "icon": "🕸️",
        "badge": "Whole-Home Coverage",
        "intro_lead": "Proprietary mesh systems lock users into vendor cloud ecosystems and black-box telemetry. With OpenWrt, you can build enterprise-grade mesh networks using standard 802.11s wireless mesh, Batman-adv, or DAWN/usteer roaming daemons.",
        "criteria": [
            "Support for IEEE 802.11s wireless mesh networking with wpad-mesh-openssl.",
            "Fast BSS Transition (802.11r), Radio Resource Management (802.11k), and Wireless Network Management (802.11v) for sub-50ms client roaming.",
            "Tri-band hardware architecture (dedicated 5 GHz backhaul radio) for environments without Ethernet cabling.",
            "Support for DAWN (Decentralized Autonomous Wireless Networking) or usteer for intelligent 802.11v band steering.",
            "Identical RF capabilities across nodes to avoid asymmetric link degradation."
        ],
        "device_ids": [
            "linksys-velop-whw03",
            "linksys-e8450",
            "belkin-rt1800",
            "xiaomi-ax3000t",
            "gl-inet-gl-mt6000",
            "comfast-cf-e390ax",
            "ubiquiti-unifi-nanohd"
        ],
        "highlights": [
            {
                "id": "linksys-velop-whw03",
                "role": "Best Tri-Band Wireless Mesh Node",
                "verdict": "Qualcomm IPQ4019 platform with two discrete 5GHz radios: one dedicated for 802.11s backhaul and one for client access."
            },
            {
                "id": "linksys-e8450",
                "role": "Best Dual-Band Wi-Fi 6 Mesh Workhorse",
                "verdict": "Exceptional radio range and mt76 driver stability. Combines seamlessly with wired gigabit backhaul across multiple floors."
            },
            {
                "id": "xiaomi-ax3000t",
                "role": "Best Budget Multi-Node Wi-Fi 6 Mesh",
                "verdict": "At low cost per unit, 3 or 4 AX3000T units create an affordable, high-speed 160 MHz whole-home mesh network."
            },
            {
                "id": "comfast-cf-e390ax",
                "role": "Best Commercial Ceiling-Mount Mesh AP",
                "verdict": "Industrial ceiling access point with 48V PoE, high-gain antennas, and dual-band Wi-Fi 6 for commercial hospitality installations."
            }
        ]
    },
    {
        "slug": "multi-gig-2-5g",
        "title": "Best OpenWrt Routers with 2.5G & 10G Ethernet Ports",
        "nav_title": "Multi-Gigabit (2.5G & 10G)",
        "description": "Curated list of OpenWrt routers equipped with 2.5GbE and 10GbE multi-gigabit Ethernet interfaces. Optimized for multi-gig fiber and NAS networking.",
        "icon": "🚀",
        "badge": "High Throughput",
        "intro_lead": "With ISPs deploying 1.2 Gbps to 5 Gbps fiber connections, traditional gigabit Ethernet ports become an instant bottleneck. These routers feature 2.5GbE or 10GbE multi-gigabit interfaces capable of delivering full line-rate speeds with OpenWrt.",
        "criteria": [
            "Dedicated 2.5GBASE-T or 10GBASE-T / SFP+ PHY interfaces with proper Linux driver support (e.g. Maxlinear GPY211, Aquantia, Realtek).",
            "SoC internal bus interconnect with sufficient bandwidth to avoid bottlenecking between switch fabric and CPU cores.",
            "Hardware Network Acceleration (MediaTek WED / PPE or Qualcomm NSS) support in OpenWrt.",
            "Fast packet processing power for CAKE SQM at 1 Gbps to 2.5 Gbps line rates.",
            "Multiple multi-gig ports to support both high-speed WAN input and high-speed LAN/NAS output simultaneously."
        ],
        "device_ids": [
            "jidu6101",
            "gl-inet-gl-mt6000",
            "xiaomi-router-7000",
            "tp-link-archer-be800-v1",
            "protectli-vault-fw4b",
            "qotom-q355g4"
        ],
        "highlights": [
            {
                "id": "jidu6101",
                "role": "Best Dual 2.5G Enterprise Value",
                "verdict": "Features two discrete 2.5GbE ports driven by Maxlinear GPY211 PHYs coupled with MediaTek Filogic 830 hardware flow offloading."
            },
            {
                "id": "gl-inet-gl-mt6000",
                "role": "Best Dual 2.5G + 4x 1G Flexible Router",
                "verdict": "Offers 2x 2.5GbE plus 4x 1GbE ports with software assignable WAN/LAN and dual-WAN load balancing."
            },
            {
                "id": "xiaomi-router-7000",
                "role": "Best Quad 2.5G Switch Configuration",
                "verdict": "Equipped with 4 full-speed 2.5GbE ports powered by Qualcomm IPQ9554 silicon, making it an ideal core router and switch combo."
            },
            {
                "id": "tp-link-archer-be800-v1",
                "role": "Ultimate 10G Multi-Gig Platform",
                "verdict": "Features 2x 10GbE (1x RJ45, 1x SFP+ combo) plus 4x 2.5GbE ports for unmatched routing headroom."
            }
        ]
    },
    {
        "slug": "x86-firewalls",
        "title": "Best x86 Mini-PC Hardware for OpenWrt Firewalls & Routers",
        "nav_title": "x86 Mini-PC Firewalls",
        "description": "Top x86_64 mini-PCs, fanless appliances, and single-board computers for OpenWrt. Evaluated for multi-gigabit routing, Suricata IDS/IPS, and CAKE SQM.",
        "icon": "🛡️",
        "badge": "Maximum Performance",
        "intro_lead": "For demanding network environments requiring full-table BGP, deep packet inspection (Suricata/Snort), or line-rate CAKE SQM over multi-gigabit fiber, dedicated x86_64 appliances running OpenWrt offer unmatched compute capacity.",
        "criteria": [
            "Intel Ethernet NICs (I211, I225-V, I226-V, or X520/X540/X710) with robust Linux driver support and multiple hardware queues.",
            "Intel AES-NI instruction set hardware acceleration for wire-speed WireGuard and IPsec VPN cryptographic throughput.",
            "Fanless, solid-state aluminum chassis for silent 24/7 reliability in home or enterprise rack environments.",
            "Open source BIOS / Coreboot firmware support without proprietary hardware lockouts.",
            "Standard UEFI boot support enabling seamless installation to internal M.2 NVMe, SATA SSD, or eMMC storage."
        ],
        "device_ids": [
            "protectli-vault-fw4b",
            "qotom-q355g4",
            "turris-omnia",
            "orange-pi-r1-plus-lts"
        ],
        "highlights": [
            {
                "id": "protectli-vault-fw4b",
                "role": "Best Dedicated Open-Source Firewall",
                "verdict": "Intel Celeron J3160 fanless appliance with 4 discrete Intel I211-AT gigabit controllers, optional Coreboot BIOS, and 4G LTE mPCIe slot."
            },
            {
                "id": "qotom-q355g4",
                "role": "Best High-Compute Core i5 Appliance",
                "verdict": "Intel Core i5-5200U dual-core with 4 threads, 4x Intel NICs, and heavy CPU headroom for complex IDS/IPS rulesets and containers."
            },
            {
                "id": "turris-omnia",
                "role": "Best High-Reliability ARM Network Computer",
                "verdict": "Modular ARM alternative to x86 featuring SFP WAN cage, 3x mPCIe slots, SIM card slot, and automatic open-source firmware updates."
            },
            {
                "id": "orange-pi-r1-plus-lts",
                "role": "Best Micro Dual-Gigabit Travel Appliance",
                "verdict": "Compact Rockchip RK3328 board with dual gigabit Ethernet ports, perfect as an ultra-compact low-power dedicated firewall."
            }
        ]
    },
    {
        "slug": "cellular-4g-5g",
        "title": "Best 4G / 5G Cellular OpenWrt Routers & Mobile Gateways",
        "nav_title": "4G / 5G Cellular Gateways",
        "description": "Authoritative hardware guide for 4G/LTE Cat 12 and 5G NR mobile broadband routers supported by OpenWrt. Features dual-SIM redundancy and multi-WAN failover.",
        "icon": "📡",
        "badge": "Mobile Broadband",
        "intro_lead": "For remote installations, maritime deployments, RVs, and enterprise multi-WAN failover, cellular OpenWrt routers provide carrier-independent mobile broadband without vendor cloud lock-in or subscription fees.",
        "criteria": [
            "Integrated Qualcomm or Quectel LTE Cat 12+ or 5G NR modem with Carrier Aggregation (CA) support.",
            "Driver support for QMI, MBIM, or ModemManager / RNDIS in OpenWrt.",
            "External SMA antenna connectors for external directional or MIMO cellular antennas.",
            "Multi-WAN failover support (mwan3) for seamless zero-downtime switching between fixed-line and cellular uplinks.",
            "Dual-SIM slot redundancy for automatic switching between different telecom providers."
        ],
        "device_ids": [
            "zte-mf286d",
            "huawei-b535-232",
            "jidu6101",
            "gl-inet-gl-mt3000"
        ],
        "highlights": [
            {
                "id": "zte-mf286d",
                "role": "Best Native LTE Cat 12 OpenWrt Gateway",
                "verdict": "Qualcomm IPQ4019 Wi-Fi SoC paired with an integrated Qualcomm Snapdragon X12 LTE-A modem supporting 3-carrier aggregation up to 600 Mbps."
            },
            {
                "id": "huawei-b535-232",
                "role": "Proprietary Chipset Architecture Analysis",
                "verdict": "HiSilicon Balong 711 modem hardware is locked to vendor firmware. Serves as a vital reference on why open modem platforms are mandatory."
            },
            {
                "id": "jidu6101",
                "role": "Best Real-World Dual-WAN Cellular Failover Hub",
                "verdict": "Demonstrated reference platform for mwan3 automatic failover pairing primary fixed-line fiber with Samsung Galaxy S25 / 5G hotspot backup."
            },
            {
                "id": "gl-inet-gl-mt3000",
                "role": "Best USB 4G/5G Tethering & Repeater Node",
                "verdict": "Supports instant plug-and-play USB cellular modem and smartphone tethering with automated fallback routing."
            }
        ]
    }
]

def render_comparison_table(devices_dict, device_ids):
    rows = []
    for dev_id in device_ids:
        d = devices_dict.get(dev_id)
        if not d:
            continue
        mfg = d.get("manufacturer", "")
        model = d.get("model", "")
        status = d.get("openwrt", {}).get("support_status", "UNKNOWN")
        soc = d.get("soc", {}).get("model", "N/A")
        ram_mb = d.get("ram", {}).get("capacity_mb", "N/A")
        flash_mb = d.get("flash", {}).get("capacity_mb", "N/A")
        
        # Wi-Fi summary
        wifi = d.get("wifi") or d.get("wireless") or []
        wifi_summary = []
        for w in wifi:
            gen = w.get("generation", "Wi-Fi")
            band = w.get("band", "")
            wifi_summary.append(f"{gen} ({band})")
        wifi_str = ", ".join(wifi_summary) if wifi_summary else "No Wi-Fi (Wired Only)"

        # Ethernet summary
        ports = d.get("ethernet_ports") or d.get("ethernet", {}).get("ports") or []
        speeds = set()
        for p in ports:
            spd = p.get("speed_mbps")
            if spd:
                speeds.add(f"{spd}M" if spd < 1000 else f"{spd//1000}G" if spd % 1000 == 0 else f"{spd/1000:.1f}G")
        speeds_str = "/".join(sorted(speeds, reverse=True)) if speeds else "N/A"
        port_count = len(ports)
        eth_str = f"{port_count} ports ({speeds_str})" if port_count > 0 else "N/A"

        status_badge = f'<span class="badge-status status-{status.lower().replace("_", "-")}">{status.replace("_", " ")}</span>'

        rows.append(f"""
        <tr>
          <td>
            <strong><a href="../../devices/{dev_id}/index.html">{mfg} {model}</a></strong>
            <div style="font-size: 0.78rem; color: var(--text-dim); margin-top: 0.2rem;">ID: <code>{dev_id}</code></div>
          </td>
          <td>{status_badge}</td>
          <td><code>{soc}</code></td>
          <td>{ram_mb} MB / {flash_mb} MB</td>
          <td style="font-size: 0.85rem;">{wifi_str}</td>
          <td>{eth_str}</td>
          <td>
            <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
              <a href="../../devices/{dev_id}/index.html" class="btn btn-sm btn-outline">Profile</a>
              <a href="../../guides/install/{dev_id}/index.html" class="btn btn-sm btn-primary">Install</a>
            </div>
          </td>
        </tr>
        """)

    return f"""
    <div class="table-responsive card" style="margin-bottom: 2.5rem; padding: 0.5rem;">
      <table class="data-table" style="width: 100%; border-collapse: collapse;">
        <thead>
          <tr>
            <th>Device Model</th>
            <th>Support Status</th>
            <th>SoC Silicon</th>
            <th>RAM / Flash</th>
            <th>Wireless Radio</th>
            <th>Ethernet</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {"".join(rows)}
        </tbody>
      </table>
    </div>
    """

def generate_category_page(cat, devices_dict, bw_module):
    slug = cat["slug"]
    title = cat["title"]
    desc = cat["description"]
    canonical_path = f"categories/{slug}/"

    # Breadcrumb JSON-LD
    json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": f"{bw_module.BASE_URL}/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Buying Guides & Categories",
                        "item": f"{bw_module.BASE_URL}/categories/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": cat["nav_title"],
                        "item": f"{bw_module.BASE_URL}/{canonical_path}"
                    }
                ]
            },
            {
                "@type": "TechArticle",
                "headline": title,
                "description": desc,
                "url": f"{bw_module.BASE_URL}/{canonical_path}",
                "inLanguage": "en",
                "author": {
                    "@type": "Organization",
                    "name": "Global OpenWrt Router Hardware Knowledge Base"
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "Global OpenWrt Router Hardware Knowledge Base"
                }
            },
            {
                "@type": "ItemList",
                "name": title,
                "description": desc,
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": idx + 1,
                        "name": f"{devices_dict[did]['manufacturer']} {devices_dict[did]['model']}" if did in devices_dict else did,
                        "url": f"{bw_module.BASE_URL}/devices/{did}/"
                    }
                    for idx, did in enumerate(cat["device_ids"]) if did in devices_dict
                ]
            }
        ]
    }

    # Navigation category pills
    pills_html = []
    for c in CATEGORIES_META:
        active_cls = ' class="category-pill active"' if c["slug"] == slug else ' class="category-pill"'
        pills_html.append(f'<a href="../{c["slug"]}/index.html"{active_cls}>{c["icon"]} {c["nav_title"]}</a>')
    category_nav = f"""
    <div class="category-pills-bar" style="display: flex; gap: 0.6rem; overflow-x: auto; padding: 0.75rem 0 1.5rem 0; margin-bottom: 2rem;">
      <a href="../index.html" class="category-pill">📁 All Guides</a>
      {"".join(pills_html)}
    </div>
    """

    # Criteria list
    criteria_li = "".join([f'<li style="margin-bottom: 0.6rem;">{c}</li>' for c in cat["criteria"]])

    # Comparison table
    table_html = render_comparison_table(devices_dict, cat["device_ids"])

    # Detailed highlight cards
    cards_html = []
    for h in cat.get("highlights", []):
        did = h["id"]
        d = devices_dict.get(did)
        if not d:
            continue
        mfg = d.get("manufacturer", "")
        model = d.get("model", "")
        status = d.get("openwrt", {}).get("support_status", "UNKNOWN")
        soc_info = f"{d.get('soc', {}).get('vendor', '')} {d.get('soc', {}).get('model', '')} ({d.get('soc', {}).get('architecture', '')})"
        ram = d.get("ram", {}).get("capacity_mb", "N/A")
        flash = d.get("flash", {}).get("capacity_mb", "N/A")

        status_badge = f'<span class="badge-status status-{status.lower().replace("_", "-")}">{status.replace("_", " ")}</span>'

        cards_html.append(f"""
        <div class="card" style="margin-bottom: 2rem; border-left: 4px solid var(--accent);">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem; margin-bottom: 1rem;">
            <div>
              <span class="badge" style="background: rgba(6, 182, 212, 0.15); color: var(--accent); margin-bottom: 0.5rem; display: inline-block;">{h['role']}</span>
              <h3 style="color: var(--text-heading); font-size: 1.35rem; margin: 0 0 0.25rem 0;">
                <a href="../../devices/{did}/index.html">{mfg} {model}</a>
              </h3>
              <p style="color: var(--text-dim); font-size: 0.85rem; margin: 0;">Silicon: <code>{soc_info}</code> &bull; Memory: <strong>{ram} MB RAM</strong> / <strong>{flash} MB Flash</strong></p>
            </div>
            <div>
              {status_badge}
            </div>
          </div>
          <p style="font-size: 0.95rem; line-height: 1.6; margin-bottom: 1.25rem; color: var(--text);"><strong>Verdict:</strong> {h['verdict']}</p>
          <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
            <a href="../../devices/{did}/index.html" class="btn btn-outline">Explore Hardware Profile &rarr;</a>
            <a href="../../guides/install/{did}/index.html" class="btn btn-primary">Two-Stage Installation Guide</a>
            <a href="../../guides/recovery/{did}/index.html" class="btn btn-sm btn-outline">Disaster Recovery Procedure</a>
          </div>
        </div>
        """)

    content = f"""
    <div class="section-header">
      <div style="margin-bottom: 0.5rem;">
        <a href="../index.html" style="color: var(--accent); font-size: 0.85rem; text-decoration: none;">&larr; Back to All Hardware Guides</a>
      </div>
      <div>
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;">
          <span style="font-size: 2rem;">{cat['icon']}</span>
          <span class="badge badge-accent">{cat['badge']}</span>
        </div>
        <h1>{title}</h1>
        <p style="font-size: 1.1rem; max-width: 850px; line-height: 1.6; color: var(--text);">{cat['intro_lead']}</p>
      </div>
    </div>

    {category_nav}

    <div class="card" style="margin-bottom: 2.5rem; background: linear-gradient(135deg, rgba(17, 25, 39, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);">
      <h2 style="color: var(--text-heading); font-size: 1.25rem; margin-bottom: 1rem;">Architectural Selection & Evaluation Criteria</h2>
      <ul style="margin: 0 0 0 1.5rem; color: var(--text-muted); line-height: 1.7; font-size: 0.95rem;">
        {criteria_li}
      </ul>
    </div>

    <div style="margin-bottom: 1.5rem;">
      <h2 style="color: var(--text-heading); font-size: 1.35rem; margin-bottom: 0.5rem;">Curated Hardware Comparison Matrix</h2>
      <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1rem;">Direct side-by-side comparison of verified devices in this category.</p>
      {table_html}
    </div>

    <div style="margin-bottom: 3rem;">
      <h2 style="color: var(--text-heading); font-size: 1.35rem; margin-bottom: 1.5rem;">Deep Dives & Recommendations</h2>
      {"".join(cards_html)}
    </div>

    {bw_module.get_contribution_panel(f"data/devices/", title, rel_root="../..")}
    """

    header = bw_module.get_header(
        title=title,
        rel_root="../..",
        current_nav="categories",
        description=desc,
        canonical_path=canonical_path,
        json_ld=json_ld
    )
    footer = bw_module.get_footer(rel_root="../..")
    return header + content + footer

def generate_categories_hub(bw_module):
    title = "OpenWrt Hardware Buying & Deployment Guides"
    desc = "Curated category guides for OpenWrt router hardware across Wi-Fi 7, Wi-Fi 6, portable travel gateways, mesh networks, 2.5G multi-gigabit, and x86 firewalls."
    canonical_path = "categories/"

    cards_html = []
    for c in CATEGORIES_META:
        cards_html.append(f"""
        <div class="card" style="display: flex; flex-direction: column; justify-content: space-between; border-top: 3px solid var(--accent);">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
              <span style="font-size: 2rem;">{c['icon']}</span>
              <span class="badge" style="background: rgba(6, 182, 212, 0.15); color: var(--accent);">{c['badge']}</span>
            </div>
            <h3 style="color: var(--text-heading); font-size: 1.25rem; margin-bottom: 0.5rem;">
              <a href="{c['slug']}/index.html">{c['nav_title']}</a>
            </h3>
            <p style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.5; margin-bottom: 1.25rem;">{c['description']}</p>
          </div>
          <div>
            <a href="{c['slug']}/index.html" class="btn btn-outline" style="width: 100%; text-align: center;">View Curated Guide & Matrix &rarr;</a>
          </div>
        </div>
        """)

    content = f"""
    <div class="section-header">
      <div>
        <span class="badge badge-accent">Search Intent Guides</span>
        <h1>OpenWrt Hardware Buying & Deployment Guides</h1>
        <p>Curated, evidence-based hardware selections evaluated by networking engineers across silicon architecture, driver maturity, and real-world performance.</p>
      </div>
    </div>

    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1.5rem; margin-bottom: 3rem;">
      {"".join(cards_html)}
    </div>

    <div class="card" style="margin-bottom: 3rem;">
      <h2 style="color: var(--text-heading); font-size: 1.25rem; margin-bottom: 0.75rem;">Hardware Selection Principles</h2>
      <p style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.6; margin-bottom: 1rem;">
        Unlike generic consumer review websites that evaluate routers solely by retail Wi-Fi speed stickers, the OpenWrt Hardware Knowledge Base analyzes the underlying silicon architecture, driver upstream status, and hardware maintainability:
      </p>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem;">
        <div style="background: rgba(17, 25, 39, 0.5); padding: 1rem; border-radius: var(--radius-sm);">
          <strong style="color: var(--accent);">1. Upstream Drivers</strong>
          <p style="font-size: 0.85rem; color: var(--text-dim); margin-top: 0.25rem;">We prioritize chipsets supported by open-source Linux kernel drivers (mt76, ath9k, ath10k, ath11k, ath12k) over proprietary closed blobs.</p>
        </div>
        <div style="background: rgba(17, 25, 39, 0.5); padding: 1rem; border-radius: var(--radius-sm);">
          <strong style="color: var(--accent);">2. Storage Headroom</strong>
          <p style="font-size: 0.85rem; color: var(--text-dim); margin-top: 0.25rem;">Minimum 128 MB flash is required for modern OpenWrt 23.05/24.x kernels, LuCI web interface, WireGuard VPN, and security updates.</p>
        </div>
        <div style="background: rgba(17, 25, 39, 0.5); padding: 1rem; border-radius: var(--radius-sm);">
          <strong style="color: var(--accent);">3. Unbrickability</strong>
          <p style="font-size: 0.85rem; color: var(--text-dim); margin-top: 0.25rem;">Every recommended router features documented TFTP automated recovery or accessible 3.3V TTL serial UART pads.</p>
        </div>
      </div>
    </div>

    {bw_module.get_contribution_panel("data/devices/", "Hardware Guides Hub", rel_root="..")}
    """

    json_ld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": title,
        "description": desc,
        "url": f"{bw_module.BASE_URL}/{canonical_path}",
        "mainEntity": {
            "@type": "ItemList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": idx + 1,
                    "name": c["title"],
                    "url": f"{bw_module.BASE_URL}/categories/{c['slug']}/"
                }
                for idx, c in enumerate(CATEGORIES_META)
            ]
        }
    }

    header = bw_module.get_header(
        title=title,
        rel_root="..",
        current_nav="categories",
        description=desc,
        canonical_path=canonical_path,
        json_ld=json_ld
    )
    footer = bw_module.get_footer(rel_root="..")
    return header + content + footer

def build_categories(site_dir, devices_dict, bw_module):
    categories_dir = os.path.join(site_dir, "categories")
    os.makedirs(categories_dir, exist_ok=True)

    # Hub
    with open(os.path.join(categories_dir, "index.html"), "w", encoding="utf-8") as fp:
        fp.write(generate_categories_hub(bw_module))

    # Individual category pages
    for cat in CATEGORIES_META:
        cat_dir = os.path.join(categories_dir, cat["slug"])
        os.makedirs(cat_dir, exist_ok=True)
        with open(os.path.join(cat_dir, "index.html"), "w", encoding="utf-8") as fp:
            fp.write(generate_category_page(cat, devices_dict, bw_module))

    print(f"[SUCCESS] Generated categories hub and {len(CATEGORIES_META)} search-intent category landing pages in {categories_dir}")
