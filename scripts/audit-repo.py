import os
import re
import json
import urllib.parse

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DEVICE_DIR = os.path.join(REPO_ROOT, "data", "devices")
CHIPSET_DIR = os.path.join(REPO_ROOT, "data", "chipsets")
SCHEMAS_DIR = os.path.join(REPO_ROOT, "data", "schemas")
DOCS_DIR = os.path.join(REPO_ROOT, "docs")

findings = {
    "CRITICAL": [],
    "HIGH": [],
    "MEDIUM": [],
    "LOW": [],
    "INFORMATIONAL": []
}

def audit_devices():
    devices = []
    ids = set()
    for root, _, files in os.walk(DEVICE_DIR):
        for f in files:
            if f.endswith(".json"):
                fpath = os.path.join(root, f)
                with open(fpath, "r", encoding="utf-8") as fp:
                    try:
                        data = json.load(fp)
                    except Exception as e:
                        findings["CRITICAL"].append(f"Device JSON parse error in {f}: {e}")
                        continue
                devices.append((fpath, data))
                
                dev_id = data.get("id")
                if not dev_id:
                    findings["CRITICAL"].append(f"Device missing 'id': {f}")
                elif dev_id in ids:
                    findings["CRITICAL"].append(f"Duplicate device ID: {dev_id}")
                else:
                    ids.add(dev_id)
                
                # Verify support_status
                openwrt_info = data.get("openwrt", {})
                status = openwrt_info.get("support_status")
                allowed_statuses = {
                    "OFFICIALLY_SUPPORTED", "COMMUNITY_VERIFIED", "PARTIALLY_VERIFIED",
                    "EXPERIMENTAL", "UNSUPPORTED", "UNKNOWN"
                }
                if status not in allowed_statuses:
                    findings["HIGH"].append(f"Device {dev_id} has invalid support_status '{status}'")
                
                # Check sources
                sources = data.get("sources", [])
                if not sources:
                    findings["HIGH"].append(f"Device {dev_id} has no source citations")
                else:
                    for s in sources:
                        url = s.get("url")
                        if not url or not url.startswith("http"):
                            findings["MEDIUM"].append(f"Device {dev_id} has missing or non-http source URL: {url}")
                
                # Check hardware category / switch vs router
                if dev_id == "zyxel-gs1900-8":
                    ports = data.get("ethernet", {}).get("ports", [])
                    wan_ports = [p for p in ports if p.get("type") == "WAN"]
                    if len(wan_ports) > 0:
                        findings["HIGH"].append(f"Zyxel GS1900-8 is a switch but lists WAN port")
                    else:
                        findings["INFORMATIONAL"].append("Zyxel GS1900-8 verified as dedicated managed switch")

                # Check Ubiquiti UniFi 6 Plus
                if dev_id == "ubiquiti-unifi-6-plus":
                    flash = data.get("flash", {})
                    if flash.get("type") == "SPI-NOR" and flash.get("capacity_mb") == 64:
                        findings["MEDIUM"].append("Ubiquiti UniFi 6+ flash is listed as 64MB SPI-NOR; upstream hardware is 16MB NOR + 4GB eMMC")

                # Check JIDU6101 vs JIDU6201
                if dev_id == "jio-jidu6101":
                    soc = data.get("soc", {}).get("model")
                    if soc != "MT7986A":
                        findings["CRITICAL"].append(f"JIDU6101 should be MT7986A, got {soc}")
                if dev_id == "jio-jidu6201":
                    soc = data.get("soc", {}).get("model")
                    if soc != "MT7981B":
                        findings["CRITICAL"].append(f"JIDU6201 should be MT7981B, got {soc}")

    findings["INFORMATIONAL"].append(f"Audited {len(devices)} device records across data/devices/")
    return devices

def audit_chipsets():
    chipsets = []
    ids = set()
    for root, _, files in os.walk(CHIPSET_DIR):
        for f in files:
            if f.endswith(".json"):
                fpath = os.path.join(root, f)
                with open(fpath, "r", encoding="utf-8") as fp:
                    try:
                        data = json.load(fp)
                    except Exception as e:
                        findings["CRITICAL"].append(f"Chipset JSON parse error in {f}: {e}")
                        continue
                chipsets.append((fpath, data))
                cid = data.get("id")
                if not cid:
                    findings["CRITICAL"].append(f"Chipset missing 'id': {f}")
                elif cid in ids:
                    findings["CRITICAL"].append(f"Duplicate chipset ID: {cid}")
                else:
                    ids.add(cid)
                
                # Check architecture
                cpu = data.get("cpu", {})
                if not cpu.get("architecture"):
                    findings["HIGH"].append(f"Chipset {cid} missing cpu.architecture")
    findings["INFORMATIONAL"].append(f"Audited {len(chipsets)} chipset records across data/chipsets/")
    return chipsets

def audit_secrets_and_paths():
    secret_patterns = [
        (re.compile(r"BEGIN (?:RSA|OPENSSH|EC|DSA) PRIVATE KEY"), "CRITICAL", "Private key detected"),
        (re.compile(r"gh[pousr]_[A-Za-z0-9_]{36,255}"), "CRITICAL", "GitHub personal access token detected"),
        (re.compile(r"file:///[A-Za-z]:[\\/]"), "HIGH", "Hardcoded absolute file:/// URI detected"),
        (re.compile(r"C:\\Users\\[a-zA-Z0-9_]+"), "MEDIUM", "Personal Windows user profile path detected"),
        (re.compile(r"(?:password|passwd|secret)\s*[:=]\s*['\"][^<>\n\r]{6,}['\"]", re.IGNORECASE), "HIGH", "Potential hardcoded password/secret string")
    ]
    
    scanned_count = 0
    for root, dirs, files in os.walk(REPO_ROOT):
        if ".git" in root or "__pycache__" in root or "node_modules" in root:
            continue
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in [".md", ".json", ".py", ".yml", ".yaml", ".html", ".js", ".css", ".txt", ".cff"]:
                scanned_count += 1
                fpath = os.path.join(root, f)
                rel_path = os.path.relpath(fpath, REPO_ROOT)
                with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
                    content = fp.read()
                    for pattern, level, desc in secret_patterns:
                        matches = pattern.findall(content)
                        if matches:
                            # Filter out false positives in PROGRESS.md or AGENT.md describing rules
                            filtered_matches = []
                            for m in matches:
                                if "PROGRESS.md" in rel_path or "AGENT.md" in rel_path or "audit-repo.py" in rel_path:
                                    continue
                                filtered_matches.append(m)
                            if filtered_matches:
                                findings[level].append(f"{desc} in {rel_path}: {len(filtered_matches)} occurrence(s)")

    findings["INFORMATIONAL"].append(f"Scanned {scanned_count} files for secrets, tokens, personal paths, and file:// links")

def audit_docs_content():
    # Check multi-wan doc
    multiwan_doc = os.path.join(REPO_ROOT, "docs", "networking", "multi-wan-failover.md")
    if os.path.exists(multiwan_doc):
        with open(multiwan_doc, "r", encoding="utf-8") as fp:
            text = fp.read()
            if "COMMUNITY_CONFIGURATION — REAL-WORLD VALIDATION PENDING" not in text:
                findings["HIGH"].append("docs/networking/multi-wan-failover.md lacks mandatory label 'COMMUNITY_CONFIGURATION — REAL-WORLD VALIDATION PENDING'")

    # Check docs/supported-devices.md
    supported_doc = os.path.join(REPO_ROOT, "docs", "supported-devices.md")
    if os.path.exists(supported_doc):
        with open(supported_doc, "r", encoding="utf-8") as fp:
            for line_no, line in enumerate(fp, 1):
                if "JIDU6201" in line and "MT7986A" in line:
                    findings["HIGH"].append(f"docs/supported-devices.md:{line_no} incorrectly lists JIDU6201 as MT7986A instead of MT7981B")
                if "Acer Predator Connect W6" in line and "Community Supported" in line:
                    findings["MEDIUM"].append(f"docs/supported-devices.md:{line_no} claims Acer Predator Connect W6 is Community Supported without documenting secure boot lock")

audit_devices()
audit_chipsets()
audit_secrets_and_paths()
audit_docs_content()

print(json.dumps(findings, indent=2))
with open(os.path.join(REPO_ROOT, "data", "audit-report.json"), "w", encoding="utf-8") as out:
    json.dump(findings, out, indent=2)
