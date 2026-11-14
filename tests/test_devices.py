"""
tests/test_devices.py — Comprehensive unit tests for data/devices/
Validates JSON formatting, schema constraints, ID uniqueness,
source URLs, and sanitization of private keys and credentials.
"""

import json
import re
import glob
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEVICES_DIR = REPO_ROOT / "data" / "devices"
SCHEMA_FILE = REPO_ROOT / "data" / "schemas" / "device.schema.json"

VALID_STATUSES = [
    "OFFICIALLY_SUPPORTED",
    "COMMUNITY_VERIFIED",
    "PARTIALLY_VERIFIED",
    "EXPERIMENTAL",
    "UNSUPPORTED",
    "UNKNOWN"
]

def get_all_device_files():
    return list(DEVICES_DIR.glob("**/*.json"))

def test_device_files_exist():
    files = get_all_device_files()
    assert len(files) >= 15, f"Expected at least 15 device records, found {len(files)}"

def test_device_unique_ids():
    ids = {}
    for f in get_all_device_files():
        with open(f, "r", encoding="utf-8") as fp:
            data = json.load(fp)
            dev_id = data.get("id")
            assert dev_id, f"File {f.name} missing 'id'"
            assert dev_id not in ids, f"Duplicate device id '{dev_id}' in {f.name} and {ids.get(dev_id)}"
            ids[dev_id] = f.name

def test_device_required_fields_and_types():
    for f in get_all_device_files():
        with open(f, "r", encoding="utf-8") as fp:
            data = json.load(fp)
            assert "manufacturer" in data and isinstance(data["manufacturer"], str)
            assert "model" in data and isinstance(data["model"], str)
            assert "hardware_revision" in data
            assert "soc" in data and isinstance(data["soc"], dict)
            assert "vendor" in data["soc"] and "model" in data["soc"]
            assert "architecture" in data
            assert "ram_mb" in data and isinstance(data["ram_mb"], int) and data["ram_mb"] >= 32
            assert "flash" in data and "type" in data["flash"] and "capacity_mb" in data["flash"]
            assert "openwrt" in data and "target" in data["openwrt"] and "profile" in data["openwrt"]
            assert data["openwrt"]["support_status"] in VALID_STATUSES
            assert "sources" in data and len(data["sources"]) >= 1

def test_device_source_urls_validity():
    url_regex = re.compile(r"^https?://[^\s/$.?#].[^\s]*$")
    for f in get_all_device_files():
        with open(f, "r", encoding="utf-8") as fp:
            data = json.load(fp)
            for src in data.get("sources", []):
                assert "title" in src and src["title"]
                assert "url" in src and url_regex.match(src["url"]), f"Invalid URL {src.get('url')} in {f.name}"
                assert "date_accessed" in src

def test_no_private_keys_or_secrets():
    secret_patterns = [
        re.compile(r"BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY"),
        re.compile(r"Poonam@\d+"),
        re.compile(r"Rahul@\d+")
    ]
    for f in get_all_device_files():
        with open(f, "r", encoding="utf-8") as fp:
            content = fp.read()
            for pattern in secret_patterns:
                assert not pattern.search(content), f"Sensitive credential pattern found in {f.name}"
