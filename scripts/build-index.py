#!/usr/bin/env python3
"""
build-index.py — Global OpenWrt Router Hardware Knowledge Base Index Generator
Crawls data/devices/ and data/chipsets/, validates schemas, checks ID uniqueness,
and compiles data/index.json and data/validation-report.json.
"""

import os
import sys
import json
import glob
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).resolve().parent.parent
DEVICES_DIR = REPO_ROOT / "data" / "devices"
CHIPSETS_DIR = REPO_ROOT / "data" / "chipsets"
SCHEMAS_DIR = REPO_ROOT / "data" / "schemas"
INDEX_PATH = REPO_ROOT / "data" / "index.json"
REPORT_PATH = REPO_ROOT / "data" / "validation-report.json"

def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_minimal(record, schema_name):
    errors = []
    if schema_name == "device":
        required = ["id", "manufacturer", "model", "hardware_revision", "soc", "architecture", "ram_mb", "flash", "openwrt", "verification", "sources"]
        for req in required:
            if req not in record:
                errors.append(f"Missing required field: {req}")
        
        status = record.get("openwrt", {}).get("support_status")
        valid_statuses = ["OFFICIALLY_SUPPORTED", "COMMUNITY_VERIFIED", "PARTIALLY_VERIFIED", "EXPERIMENTAL", "UNSUPPORTED", "UNKNOWN"]
        if status not in valid_statuses:
            errors.append(f"Invalid openwrt.support_status: {status}")
            
        if not record.get("sources") or len(record.get("sources", [])) == 0:
            errors.append("At least one source citation is required.")
            
    elif schema_name == "chipset":
        required = ["id", "vendor", "part_number", "marketing_name", "cpu", "openwrt_target", "wireless_subsystem", "hardware_acceleration", "openwrt_support_tier", "sources"]
        for req in required:
            if req not in record:
                errors.append(f"Missing required field: {req}")

    return errors

def main():
    print("=" * 60)
    print("Global OpenWrt Hardware KB: Validating & Compiling Index")
    print("=" * 60)

    devices = []
    chipsets = []
    device_ids = set()
    chipset_ids = set()
    validation_errors = []

    # Process Chipsets
    chipset_files = list(CHIPSETS_DIR.glob("*.json"))
    for cf in chipset_files:
        try:
            cdata = load_json(cf)
            cid = cdata.get("id")
            if not cid:
                validation_errors.append(f"{cf.name}: Missing 'id'")
                continue
            if cid in chipset_ids:
                validation_errors.append(f"Duplicate chipset id: {cid} in {cf.name}")
            chipset_ids.add(cid)

            errs = validate_minimal(cdata, "chipset")
            if errs:
                for e in errs:
                    validation_errors.append(f"{cf.name}: {e}")

            chipsets.append(cdata)
        except Exception as ex:
            validation_errors.append(f"{cf.name}: Failed to parse JSON: {ex}")

    # Process Devices
    device_files = list(DEVICES_DIR.glob("**/*.json"))
    status_counts = {
        "OFFICIALLY_SUPPORTED": 0,
        "COMMUNITY_VERIFIED": 0,
        "PARTIALLY_VERIFIED": 0,
        "EXPERIMENTAL": 0,
        "UNSUPPORTED": 0,
        "UNKNOWN": 0
    }

    for df in device_files:
        try:
            ddata = load_json(df)
            did = ddata.get("id")
            if not did:
                validation_errors.append(f"{df.name}: Missing 'id'")
                continue
            if did in device_ids:
                validation_errors.append(f"Duplicate device id: {did} in {df.name}")
            device_ids.add(did)

            errs = validate_minimal(ddata, "device")
            if errs:
                for e in errs:
                    validation_errors.append(f"{df.name}: {e}")

            status = ddata.get("openwrt", {}).get("support_status", "UNKNOWN")
            if status in status_counts:
                status_counts[status] += 1

            devices.append(ddata)
        except Exception as ex:
            validation_errors.append(f"{df.name}: Failed to parse JSON: {ex}")

    # Sort deterministically
    devices.sort(key=lambda x: (x.get("manufacturer", ""), x.get("model", "")))
    chipsets.sort(key=lambda x: (x.get("vendor", ""), x.get("marketing_name", "")))

    # Compile index
    index_payload = {
        "metadata": {
            "title": "Global OpenWrt Router Hardware Knowledge Base Index",
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "total_devices": len(devices),
            "total_chipsets": len(chipsets),
            "status_summary": status_counts
        },
        "devices": devices,
        "chipsets": chipsets
    }

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index_payload, f, indent=2, ensure_ascii=False)
    print(f"Generated index at {INDEX_PATH} ({len(devices)} devices, {len(chipsets)} chipsets)")

    # Compile validation report
    report_payload = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_device_records": len(devices),
        "total_chipset_records": len(chipsets),
        "status_breakdown": status_counts,
        "total_sources_cited": sum(len(d.get("sources", [])) for d in devices),
        "validation_passed": len(validation_errors) == 0,
        "errors": validation_errors
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report_payload, f, indent=2, ensure_ascii=False)
    print(f"Generated validation report at {REPORT_PATH}")

    if validation_errors:
        print(f"\n[ERROR] {len(validation_errors)} validation errors encountered:")
        for err in validation_errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("\n[SUCCESS] All schemas, unique IDs, and source requirements validated successfully!")
        sys.exit(0)

if __name__ == "__main__":
    main()
