#!/usr/bin/env python3
"""
scripts/audit-freshness.py
Module J: Data Freshness, Evidence Quality Scoring, and Review Queue.
Audits all 72+ device records for completeness, evidence tier, and verification staleness.
"""

import os
import sys
import json
from datetime import datetime, timezone

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(REPO_ROOT, "data")
DEVICES_DIR = os.path.join(DATA_DIR, "devices")

AUDIT_FIELDS = [
    "soc", "ram_mb", "flash", "wireless", "ethernet", "bootloader",
    "serial_uart", "openwrt", "installation", "recovery", "verification",
    "firmware", "security", "lifecycle", "feature_compatibility",
    "oem_relationships", "sources", "popularity"
]

def calculate_completeness(d):
    score = 0
    total_weights = 0
    weights = {
        "soc": 10,
        "ram_mb": 5,
        "flash": 5,
        "wireless": 10,
        "ethernet": 10,
        "openwrt": 15,
        "installation": 10,
        "recovery": 10,
        "verification": 10,
        "firmware": 5,
        "feature_compatibility": 5,
        "lifecycle": 5,
        "sources": 10
    }
    for field, weight in weights.items():
        total_weights += weight
        val = d.get(field)
        if val is not None and val != "" and val != []:
            score += weight
    return min(100, int((score / total_weights) * 100))

def determine_evidence_tier(d):
    evidence_list = d.get("verification", {}).get("evidence", [])
    evidence_text = " ".join(evidence_list).lower()
    sources = d.get("sources", [])
    src_types = {s.get("type") for s in sources}

    if "dmesg" in evidence_text or "physical hardware" in evidence_text or "boot log" in evidence_text:
        return "GOLD"
    elif "OPENWRT_GIT" in src_types or "UPSTREAM_GITHUB" in src_types or "dts" in evidence_text or "commit" in evidence_text:
        return "SILVER"
    elif len(sources) >= 1:
        return "BRONZE"
    return "UNVERIFIED"

def audit_catalog_freshness():
    devices = []
    for root, _, files in os.walk(DEVICES_DIR):
        for f in files:
            if f.endswith(".json"):
                with open(os.path.join(root, f), "r", encoding="utf-8") as fp:
                    try:
                        devices.append((os.path.join(root, f), json.load(fp)))
                    except Exception as e:
                        print(f"Error loading {f}: {e}")

    now = datetime.now(timezone.utc)
    stale_threshold_days = 180

    stale_records = []
    gold_count = 0
    silver_count = 0
    bronze_count = 0
    avg_completeness = 0

    audited_devices = []

    for path, d in devices:
        dev_id = d.get("id", os.path.basename(path))
        completeness = calculate_completeness(d)
        tier = determine_evidence_tier(d)
        if tier == "GOLD": gold_count += 1
        elif tier == "SILVER": silver_count += 1
        elif tier == "BRONZE": bronze_count += 1

        avg_completeness += completeness

        last_v_str = d.get("verification", {}).get("last_verified") or d.get("metadata", {}).get("last_verified_at") or "2026-01-01"
        try:
            last_v = datetime.strptime(last_v_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            days_since = (now - last_v).days
        except Exception:
            days_since = 999

        is_stale = days_since > stale_threshold_days
        if is_stale:
            stale_records.append({
                "id": dev_id,
                "model": f"{d.get('manufacturer')} {d.get('model')}",
                "last_verified": last_v_str,
                "days_since_verification": days_since,
                "support_status": d.get("openwrt", {}).get("support_status")
            })

        audited_devices.append({
            "id": dev_id,
            "completeness": completeness,
            "tier": tier,
            "last_verified": last_v_str,
            "stale": is_stale
        })

    total = len(devices)
    report = {
        "generated_at": now.isoformat(),
        "total_devices": total,
        "average_completeness_percent": round(avg_completeness / total, 1) if total else 0,
        "evidence_tiers": {
            "GOLD": gold_count,
            "SILVER": silver_count,
            "BRONZE": bronze_count
        },
        "stale_record_count": len(stale_records),
        "review_queue": stale_records
    }

    out_file = os.path.join(DATA_DIR, "freshness-report.json")
    with open(out_file, "w", encoding="utf-8") as fp:
        json.dump(report, fp, indent=2)

    print(f"============================================================")
    print(f"Hardware KB Freshness & Quality Audit")
    print(f"============================================================")
    print(f"Total Devices: {total}")
    print(f"Average Completeness: {report['average_completeness_percent']}%")
    print(f"Evidence Quality: {gold_count} Gold | {silver_count} Silver | {bronze_count} Bronze")
    print(f"Stale Records (>180d): {len(stale_records)}")
    print(f"Freshness report generated at: {out_file}")

if __name__ == "__main__":
    audit_catalog_freshness()
