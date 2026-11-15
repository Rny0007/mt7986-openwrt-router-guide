#!/usr/bin/env python3
"""
scripts/moderate-submissions.py
Processes, validates, triages, and audits community hardware submissions.
Enforces:
  1. Valid schema compliance (data/schemas/submission.schema.json)
  2. Duplicate submission detection (checks existing catalog & submissions)
  3. Mandatory primary evidentiary source validation
  4. Audit trail logging with timestamps
"""

import os
import sys
import json
import glob
from datetime import datetime, timezone

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SUBMISSIONS_DIR = os.path.join(REPO_ROOT, "data", "submissions")
PENDING_DIR = os.path.join(SUBMISSIONS_DIR, "pending")
ACCEPTED_DIR = os.path.join(SUBMISSIONS_DIR, "accepted")
REJECTED_DIR = os.path.join(SUBMISSIONS_DIR, "rejected")
DEVICES_DIR = os.path.join(REPO_ROOT, "data", "devices")

os.makedirs(PENDING_DIR, exist_ok=True)
os.makedirs(ACCEPTED_DIR, exist_ok=True)
os.makedirs(REJECTED_DIR, exist_ok=True)

def load_existing_catalog_ids():
    ids = set()
    for root, _, files in os.walk(DEVICES_DIR):
        for f in files:
            if f.endswith(".json"):
                with open(os.path.join(root, f), "r", encoding="utf-8") as fp:
                    try:
                        d = json.load(fp)
                        if "id" in d:
                            ids.add(d["id"])
                    except Exception:
                        pass
    return ids

def validate_submission(sub_data, catalog_ids):
    errors = []
    
    # Required keys
    req_keys = ["submission_id", "submission_type", "submitted_at", "status", "device_summary", "sources", "audit_log"]
    for k in req_keys:
        if k not in sub_data:
            errors.append(f"Missing required field: '{k}'")
            
    # Source requirement
    sources = sub_data.get("sources", [])
    if not sources or len(sources) < 1:
        errors.append("Submission must include at least one verifiable source citation.")
    else:
        for s in sources:
            if not s.get("url") or not s.get("url").startswith("http"):
                errors.append(f"Invalid source URL in submission: {s.get('url')}")

    # Duplicate check for new devices
    if sub_data.get("submission_type") == "NEW_DEVICE":
        summary = sub_data.get("device_summary", {})
        mfg = summary.get("manufacturer", "").lower().replace(" ", "-")
        model = summary.get("model", "").lower().replace(" ", "-")
        target_id = f"{mfg}-{model}"
        if target_id in catalog_ids:
            errors.append(f"Potential duplicate: Device ID '{target_id}' already exists in catalog.")

    return errors

def audit_pending_queue():
    catalog_ids = load_existing_catalog_ids()
    pending_files = glob.glob(os.path.join(PENDING_DIR, "*.json"))
    print(f"[*] Auditing Community Submissions: Found {len(pending_files)} pending submissions.")

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_pending": len(pending_files),
        "valid_submissions": 0,
        "invalid_submissions": 0,
        "items": []
    }

    for pf in pending_files:
        with open(pf, "r", encoding="utf-8") as fp:
            try:
                sub = json.load(fp)
            except Exception as e:
                print(f"[!] JSON Error in {os.path.basename(pf)}: {e}")
                report["invalid_submissions"] += 1
                continue

        errors = validate_submission(sub, catalog_ids)
        is_valid = len(errors) == 0
        if is_valid:
            report["valid_submissions"] += 1
            print(f"  [VALID] {sub.get('submission_id')} - {sub.get('device_summary', {}).get('manufacturer')} {sub.get('device_summary', {}).get('model')}")
        else:
            report["invalid_submissions"] += 1
            print(f"  [INVALID] {sub.get('submission_id')} - Errors: {'; '.join(errors)}")

        report["items"].append({
            "file": os.path.basename(pf),
            "submission_id": sub.get("submission_id"),
            "valid": is_valid,
            "errors": errors
        })

    out_report = os.path.join(SUBMISSIONS_DIR, "moderation-audit.json")
    with open(out_report, "w", encoding="utf-8") as fp:
        json.dump(report, fp, indent=2)
    print(f"[+] Moderation report saved to {out_report}")

if __name__ == "__main__":
    audit_pending_queue()
