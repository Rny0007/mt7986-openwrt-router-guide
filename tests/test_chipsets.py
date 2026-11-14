"""
tests/test_chipsets.py — Unit tests for data/chipsets/
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CHIPSETS_DIR = REPO_ROOT / "data" / "chipsets"

VALID_TIERS = [
    "TIER_1_MAINSTREAM",
    "TIER_2_STABLE",
    "TIER_3_COMMUNITY_ONLY",
    "TIER_4_UNSUPPORTED_PROPRIETARY"
]

def test_chipset_files_exist():
    files = list(CHIPSETS_DIR.glob("*.json"))
    assert len(files) >= 8, f"Expected at least 8 chipset profiles, found {len(files)}"

def test_chipset_schema_conformance():
    ids = set()
    for f in CHIPSETS_DIR.glob("*.json"):
        with open(f, "r", encoding="utf-8") as fp:
            data = json.load(fp)
            cid = data.get("id")
            assert cid, f"Missing id in {f.name}"
            assert cid not in ids, f"Duplicate chipset id: {cid}"
            ids.add(cid)

            assert "vendor" in data
            assert "part_number" in data
            assert "marketing_name" in data
            assert "cpu" in data and "cores" in data["cpu"] and "max_clock_mhz" in data["cpu"]
            assert "openwrt_target" in data
            assert data["openwrt_support_tier"] in VALID_TIERS
            assert len(data.get("sources", [])) >= 1
