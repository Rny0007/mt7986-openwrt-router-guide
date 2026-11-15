#!/usr/bin/env python3
"""
scripts/api_generator.py
Module G: Versioned Public Read-Only REST API & Bulk Data Exports.
Generates:
  - /api/v1/devices/index.json
  - /api/v1/devices/{id}.json
  - /api/v1/manufacturers/index.json
  - /api/v1/chipsets/index.json
  - /api/v1/chipsets/{id}.json
  - /api/v1/categories/index.json
  - /api/v1/security/index.json
  - /api/v1/lifecycle/index.json
  - /api/v1/export/devices.json & devices.csv
  - /api/v1/export/chipsets.json
  - /api/v1/export/security.json
  - /api/v1/openapi.json
  - /api/index.html (Interactive documentation)
"""

import os
import sys
import csv
import json
from datetime import datetime, timezone

def generate_api_and_exports(site_dir, devices, chipsets, categories_meta, cves_data, bw_module):
    api_dir = os.path.join(site_dir, "api")
    v1_dir = os.path.join(api_dir, "v1")
    dev_api_dir = os.path.join(v1_dir, "devices")
    chip_api_dir = os.path.join(v1_dir, "chipsets")
    export_dir = os.path.join(v1_dir, "export")

    os.makedirs(dev_api_dir, exist_ok=True)
    os.makedirs(chip_api_dir, exist_ok=True)
    os.makedirs(export_dir, exist_ok=True)

    now = datetime.now(timezone.utc).isoformat()

    # 1. /api/v1/devices/index.json (Complete catalog summary)
    device_summaries = []
    for d in devices:
        ports = d.get("ethernet_ports") or d.get("ethernet", {}).get("ports") or []
        wifi = d.get("wifi") or d.get("wireless") or []
        device_summaries.append({
            "id": d.get("id"),
            "manufacturer": d.get("manufacturer"),
            "model": d.get("model"),
            "hardware_revision": d.get("hardware_revision"),
            "support_status": d.get("openwrt", {}).get("support_status"),
            "target": d.get("openwrt", {}).get("target"),
            "profile": d.get("openwrt", {}).get("profile"),
            "soc": {
                "vendor": d.get("soc", {}).get("vendor"),
                "model": d.get("soc", {}).get("model"),
                "family": d.get("soc", {}).get("family")
            },
            "architecture": d.get("architecture"),
            "ram_mb": d.get("ram_mb"),
            "flash_mb": d.get("flash", {}).get("capacity_mb"),
            "port_count": len(ports),
            "wifi_generations": [w.get("generation") for w in wifi],
            "lifecycle_status": d.get("lifecycle", {}).get("openwrt_support_status"),
            "evidence_tier": d.get("metadata", {}).get("evidence_tier", "SILVER"),
            "last_verified": d.get("verification", {}).get("last_verified"),
            "links": {
                "self": f"{bw_module.BASE_URL}/api/v1/devices/{d.get('id')}.json",
                "html_profile": f"{bw_module.BASE_URL}/devices/{d.get('id')}/",
                "install_guide": f"{bw_module.BASE_URL}/guides/install/{d.get('id')}/",
                "recovery_guide": f"{bw_module.BASE_URL}/guides/recovery/{d.get('id')}/"
            }
        })

    with open(os.path.join(v1_dir, "devices", "index.json"), "w", encoding="utf-8") as fp:
        json.dump({
            "api_version": "v1",
            "generated_at": now,
            "total_count": len(device_summaries),
            "data": device_summaries
        }, fp, indent=2)

    # Individual device JSON files: /api/v1/devices/{id}.json
    for d in devices:
        dev_id = d.get("id")
        with open(os.path.join(dev_api_dir, f"{dev_id}.json"), "w", encoding="utf-8") as fp:
            json.dump({
                "api_version": "v1",
                "generated_at": now,
                "device": d
            }, fp, indent=2)

    # 2. /api/v1/manufacturers/index.json
    mfg_dict = {}
    for d in devices:
        m = d.get("manufacturer")
        if m not in mfg_dict:
            mfg_dict[m] = {"manufacturer": m, "device_count": 0, "device_ids": []}
        mfg_dict[m]["device_count"] += 1
        mfg_dict[m]["device_ids"].append(d.get("id"))

    mfg_list = sorted(list(mfg_dict.values()), key=lambda x: x["manufacturer"])
    with open(os.path.join(v1_dir, "manufacturers.json"), "w", encoding="utf-8") as fp:
        json.dump({
            "api_version": "v1",
            "generated_at": now,
            "total_count": len(mfg_list),
            "data": mfg_list
        }, fp, indent=2)

    # 3. /api/v1/chipsets/index.json & {id}.json
    chip_summaries = []
    for c in chipsets:
        cid = c.get("id")
        chip_summaries.append({
            "id": cid,
            "vendor": c.get("vendor"),
            "part_number": c.get("part_number"),
            "architecture": c.get("architecture"),
            "cores": c.get("cores"),
            "max_frequency_mhz": c.get("max_frequency_mhz"),
            "openwrt_target": c.get("openwrt_target"),
            "links": {
                "self": f"{bw_module.BASE_URL}/api/v1/chipsets/{cid}.json",
                "html_profile": f"{bw_module.BASE_URL}/chipsets/{cid}/"
            }
        })
        with open(os.path.join(chip_api_dir, f"{cid}.json"), "w", encoding="utf-8") as fp:
            json.dump({
                "api_version": "v1",
                "generated_at": now,
                "chipset": c
            }, fp, indent=2)

    with open(os.path.join(v1_dir, "chipsets", "index.json"), "w", encoding="utf-8") as fp:
        json.dump({
            "api_version": "v1",
            "generated_at": now,
            "total_count": len(chip_summaries),
            "data": chip_summaries
        }, fp, indent=2)

    # 4. /api/v1/categories/index.json
    with open(os.path.join(v1_dir, "categories.json"), "w", encoding="utf-8") as fp:
        json.dump({
            "api_version": "v1",
            "generated_at": now,
            "total_count": len(categories_meta),
            "data": categories_meta
        }, fp, indent=2)

    # 5. /api/v1/security/index.json
    with open(os.path.join(v1_dir, "security.json"), "w", encoding="utf-8") as fp:
        json.dump({
            "api_version": "v1",
            "generated_at": now,
            "total_count": len(cves_data.get("vulnerabilities", [])),
            "data": cves_data
        }, fp, indent=2)

    # 6. /api/v1/lifecycle/index.json
    lifecycle_list = []
    for d in devices:
        lifecycle_list.append({
            "id": d.get("id"),
            "model": f"{d.get('manufacturer')} {d.get('model')}",
            "lifecycle": d.get("lifecycle", {})
        })
    with open(os.path.join(v1_dir, "lifecycle.json"), "w", encoding="utf-8") as fp:
        json.dump({
            "api_version": "v1",
            "generated_at": now,
            "total_count": len(lifecycle_list),
            "data": lifecycle_list
        }, fp, indent=2)

    # 7. Complete Bulk Data Exports
    # devices.json
    with open(os.path.join(export_dir, "devices.json"), "w", encoding="utf-8") as fp:
        json.dump(devices, fp, indent=2)

    # chipsets.json
    with open(os.path.join(export_dir, "chipsets.json"), "w", encoding="utf-8") as fp:
        json.dump(chipsets, fp, indent=2)

    # security.json
    with open(os.path.join(export_dir, "security.json"), "w", encoding="utf-8") as fp:
        json.dump(cves_data, fp, indent=2)

    # devices.csv
    csv_path = os.path.join(export_dir, "devices.csv")
    csv_headers = [
        "id", "manufacturer", "model", "hardware_revision", "support_status",
        "target", "profile", "soc_vendor", "soc_model", "architecture",
        "ram_mb", "flash_mb", "flash_type", "ethernet_port_count", "max_speed_mbps",
        "has_2g_wifi", "has_5g_wifi", "has_6g_wifi", "discontinuation_status",
        "manufacturer_support_status", "openwrt_support_status", "evidence_tier",
        "completeness_score", "last_verified"
    ]
    with open(csv_path, "w", encoding="utf-8", newline="") as fp:
        writer = csv.writer(fp)
        writer.writerow(csv_headers)
        for d in devices:
            ports = d.get("ethernet_ports") or d.get("ethernet", {}).get("ports") or []
            max_spd = max([p.get("speed_mbps", 0) for p in ports]) if ports else 0
            wifi = d.get("wifi") or d.get("wireless") or []
            has_2g = any(w.get("frequency_ghz") == 2.4 or w.get("band") == "2.4GHz" for w in wifi)
            has_5g = any(w.get("frequency_ghz") == 5.0 or w.get("band") == "5GHz" for w in wifi)
            has_6g = any(w.get("frequency_ghz") == 6.0 or w.get("band") == "6GHz" for w in wifi)

            writer.writerow([
                d.get("id"),
                d.get("manufacturer"),
                d.get("model"),
                d.get("hardware_revision"),
                d.get("openwrt", {}).get("support_status"),
                d.get("openwrt", {}).get("target"),
                d.get("openwrt", {}).get("profile"),
                d.get("soc", {}).get("vendor"),
                d.get("soc", {}).get("model"),
                d.get("architecture"),
                d.get("ram_mb"),
                d.get("flash", {}).get("capacity_mb"),
                d.get("flash", {}).get("type"),
                len(ports),
                max_spd,
                has_2g,
                has_5g,
                has_6g,
                d.get("lifecycle", {}).get("discontinuation_status"),
                d.get("lifecycle", {}).get("manufacturer_support_status"),
                d.get("lifecycle", {}).get("openwrt_support_status"),
                d.get("metadata", {}).get("evidence_tier"),
                d.get("metadata", {}).get("completeness_score"),
                d.get("verification", {}).get("last_verified")
            ])

    # 8. OpenAPI Specification: /api/v1/openapi.json
    openapi_spec = {
        "openapi": "3.1.0",
        "info": {
            "title": "Global OpenWrt Router Hardware Knowledge Base API",
            "version": "1.0.0",
            "description": "Zero-dependency, high-performance static RESTful API providing evidence-based specifications, CVE security intelligence, firmware metadata, and lifecycle statuses for OpenWrt router hardware worldwide.",
            "license": {
                "name": "CC BY 4.0 / MIT",
                "url": "https://creativecommons.org/licenses/by/4.0/"
            }
        },
        "servers": [
            {
                "url": f"{bw_module.BASE_URL}/api/v1",
                "description": "Production Read-Only Public API"
            }
        ],
        "paths": {
            "/devices/index.json": {
                "get": {
                    "summary": "List all cataloged router hardware devices",
                    "responses": {
                        "200": { "description": "JSON array of device summaries" }
                    }
                }
            },
            "/devices/{id}.json": {
                "get": {
                    "summary": "Get full technical specification, firmware, and CVE security profile for a device",
                    "parameters": [
                        { "name": "id", "in": "path", "required": True, "schema": { "type": "string" } }
                    ],
                    "responses": {
                        "200": { "description": "Detailed device object" }
                    }
                }
            },
            "/chipsets/index.json": {
                "get": { "summary": "List all networking silicon architectures" }
            },
            "/security.json": {
                "get": { "summary": "List CVE security vulnerabilities affecting OpenWrt components" }
            },
            "/lifecycle.json": {
                "get": { "summary": "List hardware lifecycle, EOL, and deprecation statuses" }
            }
        }
    }
    with open(os.path.join(v1_dir, "openapi.json"), "w", encoding="utf-8") as fp:
        json.dump(openapi_spec, fp, indent=2)

    # 9. Interactive API Documentation HTML: /api/index.html
    api_html = generate_api_docs_html(bw_module)
    with open(os.path.join(api_dir, "index.html"), "w", encoding="utf-8") as fp:
        fp.write(api_html)

    print(f"[SUCCESS] Generated complete v1 REST API, OpenAPI 3.1 spec, and bulk exports in {v1_dir}")

def generate_api_docs_html(bw_module):
    title = "Public Read-Only REST API & Bulk Data Exports"
    desc = "Open, versioned REST API and CSV/JSON bulk data downloads for the Global OpenWrt Router Hardware Knowledge Base. Free, zero-auth, CDN-cached."
    canonical_path = "api/"

    content = f"""
    <div class="section-header">
      <div>
        <span class="badge badge-accent">Developer Platform</span>
        <h1>OpenWrt Router Hardware Public API (v1)</h1>
        <p>A fast, free, CDN-backed read-only REST API and complete data export engine for network engineers, security researchers, and developers.</p>
      </div>
    </div>

    <!-- API Highlights Grid -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-bottom: 2.5rem;">
      <div class="card" style="border-top: 3px solid var(--accent);">
        <h3 style="color: var(--text-heading); font-size: 1.15rem; margin-bottom: 0.5rem;">⚡ Zero Authentication</h3>
        <p style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.6;">No API keys, registration, or rate-limit friction required. Host-verified and served directly from GitHub global CDN infrastructure.</p>
      </div>
      <div class="card" style="border-top: 3px solid var(--success);">
        <h3 style="color: var(--text-heading); font-size: 1.15rem; margin-bottom: 0.5rem;">📊 Complete Bulk Downloads</h3>
        <p style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.6;">Export the entire 72-device hardware catalog, silicon profiles, and CVE vulnerability database in structured JSON or CSV format.</p>
      </div>
      <div class="card" style="border-top: 3px solid var(--warning);">
        <h3 style="color: var(--text-heading); font-size: 1.15rem; margin-bottom: 0.5rem;">🔒 CORS & HTTPS Enabled</h3>
        <p style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.6;">Full Cross-Origin Resource Sharing (CORS) support enables seamless browser client integration in SPAs, web dashboards, and LuCI widgets.</p>
      </div>
    </div>

    <!-- Bulk Exports Section -->
    <div class="card" style="margin-bottom: 3rem; background: linear-gradient(135deg, rgba(17, 25, 39, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);">
      <h2 style="color: var(--text-heading); font-size: 1.35rem; margin-bottom: 0.5rem;">📦 Instant Bulk Data Downloads</h2>
      <p style="color: var(--text-muted); font-size: 0.95rem; margin-bottom: 1.5rem;">Direct links to machine-readable dataset dumps updated automatically on every production commit.</p>
      
      <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
        <a href="v1/export/devices.csv" class="btn btn-primary" download>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
          Download Catalog (CSV)
        </a>
        <a href="v1/export/devices.json" class="btn btn-outline" download>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
          Full Devices Dump (JSON)
        </a>
        <a href="v1/export/chipsets.json" class="btn btn-outline" download>
          Silicon Architectures (JSON)
        </a>
        <a href="v1/export/security.json" class="btn btn-outline" download>
          CVE Vulnerability Database (JSON)
        </a>
        <a href="v1/openapi.json" class="btn btn-sm btn-outline" target="_blank" rel="noopener">
          OpenAPI 3.1 Specification
        </a>
      </div>
    </div>

    <!-- API Reference Table -->
    <div style="margin-bottom: 3rem;">
      <h2 style="color: var(--text-heading); font-size: 1.35rem; margin-bottom: 1rem;">REST API Endpoints (v1)</h2>
      
      <div class="table-responsive card" style="padding: 0.5rem;">
        <table class="data-table" style="width: 100%; border-collapse: collapse;">
          <thead>
            <tr>
              <th>Method</th>
              <th>Endpoint URL</th>
              <th>Description</th>
              <th>Sample Output</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><span class="badge" style="background: rgba(16, 185, 129, 0.15); color: var(--success); font-weight: 700;">GET</span></td>
              <td><code>/api/v1/devices/index.json</code></td>
              <td>Summary listing of all 72 cataloged devices with RAM, flash, ports, Wi-Fi, and lifecycle status.</td>
              <td><a href="v1/devices/index.json" target="_blank" class="btn btn-sm btn-outline">Inspect JSON</a></td>
            </tr>
            <tr>
              <td><span class="badge" style="background: rgba(16, 185, 129, 0.15); color: var(--success); font-weight: 700;">GET</span></td>
              <td><code>/api/v1/devices/&#123;id&#125;.json</code></td>
              <td>Complete device profile including Firmware Intelligence, Feature Matrix, CVE Security, and Schematics.</td>
              <td><a href="v1/devices/jio-jidu6101.json" target="_blank" class="btn btn-sm btn-outline">Example: JIDU6101</a></td>
            </tr>
            <tr>
              <td><span class="badge" style="background: rgba(16, 185, 129, 0.15); color: var(--success); font-weight: 700;">GET</span></td>
              <td><code>/api/v1/chipsets/index.json</code></td>
              <td>Catalog of all 20 profiled networking silicon architectures and target classifications.</td>
              <td><a href="v1/chipsets/index.json" target="_blank" class="btn btn-sm btn-outline">Inspect JSON</a></td>
            </tr>
            <tr>
              <td><span class="badge" style="background: rgba(16, 185, 129, 0.15); color: var(--success); font-weight: 700;">GET</span></td>
              <td><code>/api/v1/manufacturers.json</code></td>
              <td>Index of 31 router hardware manufacturers and mapped device counters.</td>
              <td><a href="v1/manufacturers.json" target="_blank" class="btn btn-sm btn-outline">Inspect JSON</a></td>
            </tr>
            <tr>
              <td><span class="badge" style="background: rgba(16, 185, 129, 0.15); color: var(--success); font-weight: 700;">GET</span></td>
              <td><code>/api/v1/security.json</code></td>
              <td>Registry of verified CVE vulnerabilities affecting OpenWrt networking packages and components.</td>
              <td><a href="v1/security.json" target="_blank" class="btn btn-sm btn-outline">Inspect JSON</a></td>
            </tr>
            <tr>
              <td><span class="badge" style="background: rgba(16, 185, 129, 0.15); color: var(--success); font-weight: 700;">GET</span></td>
              <td><code>/api/v1/lifecycle.json</code></td>
              <td>Hardware lifecycle statuses, manufacturer EOL dates, and OpenWrt deprecation horizons.</td>
              <td><a href="v1/lifecycle.json" target="_blank" class="btn btn-sm btn-outline">Inspect JSON</a></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Code Examples -->
    <div class="card" style="margin-bottom: 3rem;">
      <h2 style="color: var(--text-heading); font-size: 1.35rem; margin-bottom: 1rem;">Code Implementation Examples</h2>
      
      <h3 style="color: var(--accent); font-size: 1rem; margin-bottom: 0.5rem;">cURL (Terminal)</h3>
      <pre><code>curl -s "{bw_module.BASE_URL}/api/v1/devices/jio-jidu6101.json" | jq .device.feature_compatibility</code></pre>

      <h3 style="color: var(--accent); font-size: 1rem; margin-top: 1.5rem; margin-bottom: 0.5rem;">Python 3</h3>
      <pre><code>import urllib.request
import json

url = "{bw_module.BASE_URL}/api/v1/devices/index.json"
req = urllib.request.Request(url, headers={{"User-Agent": "OpenWrtHardwareClient/1.0"}})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())
    print(f"Total cataloged devices: {{data['total_count']}}")
    for d in data['data'][:5]:
        print(f"- {{d['manufacturer']}} {{d['model']}} ({{d['support_status']}})")</code></pre>

      <h3 style="color: var(--accent); font-size: 1rem; margin-top: 1.5rem; margin-bottom: 0.5rem;">JavaScript (Fetch / Async)</h3>
      <pre><code>async function fetchOpenWrtDevices() {{
  const res = await fetch('{bw_module.BASE_URL}/api/v1/devices/index.json');
  const {{ data }} = await res.json();
  const wifi6Devices = data.filter(d => d.wifi_generations.includes('Wi-Fi 6'));
  console.log(`Found ${{wifi6Devices.length}} Wi-Fi 6 routers supported by OpenWrt.`);
}}
fetchOpenWrtDevices();</code></pre>
    </div>

    {bw_module.get_contribution_panel("data/devices/", "Public API Documentation", rel_root="..")}
    """

    header = bw_module.get_header(
        title=title,
        rel_root="..",
        current_nav="api",
        description=desc,
        canonical_path=canonical_path,
        json_ld={
            "@context": "https://schema.org",
            "@type": "WebAPI",
            "name": title,
            "description": desc,
            "url": f"{bw_module.BASE_URL}/{canonical_path}",
            "documentation": f"{bw_module.BASE_URL}/{canonical_path}"
        }
    )
    footer = bw_module.get_footer(rel_root="..")
    return header + content + footer
