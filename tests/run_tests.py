#!/usr/bin/env python3
"""
run_tests.py — Standalone Zero-Dependency Test Suite Runner
Executes device, chipset, and index integrity validations using standard library unittest.
"""

import unittest
import sys
from pathlib import Path

# Add tests directory to sys.path
TESTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TESTS_DIR))

import test_devices
import test_chipsets
import test_index
import test_website

class TestHardwareKB(unittest.TestCase):

    def test_devices_exist(self):
        test_devices.test_device_files_exist()

    def test_devices_unique_ids(self):
        test_devices.test_device_unique_ids()

    def test_devices_schema(self):
        test_devices.test_device_required_fields_and_types()

    def test_devices_source_urls(self):
        test_devices.test_device_source_urls_validity()

    def test_devices_no_secrets(self):
        test_devices.test_no_private_keys_or_secrets()

    def test_chipsets_exist(self):
        test_chipsets.test_chipset_files_exist()

    def test_chipsets_schema(self):
        test_chipsets.test_chipset_schema_conformance()

    def test_index_synced(self):
        test_index.test_index_json_exists_and_synced()

    def test_validation_report(self):
        test_index.test_validation_report_status()

    def test_website_generation(self):
        loader = unittest.defaultTestLoader.loadTestsFromTestCase(test_website.TestGeneratedWebsite)
        result = unittest.TestResult()
        loader.run(result)
        self.assertTrue(result.wasSuccessful(), f"Website tests failed: {result.errors + result.failures}")

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestHardwareKB)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
