"""
tests/test_index.py — Tests index.json integrity and sync with data/devices/
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEVICES_DIR = REPO_ROOT / "data" / "devices"
INDEX_FILE = REPO_ROOT / "data" / "index.json"
REPORT_FILE = REPO_ROOT / "data" / "validation-report.json"

def test_index_json_exists_and_synced():
    assert INDEX_FILE.exists(), "data/index.json does not exist"
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert "metadata" in data
        assert "devices" in data
        assert "chipsets" in data

        device_files = list(DEVICES_DIR.glob("**/*.json"))
        assert len(data["devices"]) == len(device_files), "index.json device count mismatch with data/devices/"

def test_validation_report_status():
    assert REPORT_FILE.exists(), "data/validation-report.json does not exist"
    with open(REPORT_FILE, "r", encoding="utf-8") as f:
        report = json.load(f)
        assert report.get("validation_passed") is True, f"Validation report failed: {report.get('errors')}"
        assert len(report.get("errors", [])) == 0
