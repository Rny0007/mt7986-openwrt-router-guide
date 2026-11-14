import os
import unittest
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE_DIR = os.path.join(REPO_ROOT, "site")

class TestGeneratedWebsite(unittest.TestCase):
    def test_core_pages_exist(self):
        core_files = [
            "index.html",
            "explorer/index.html",
            "devices/index.html",
            "chipsets/index.html",
            "diagrams/index.html",
            "guides/installation/index.html",
            "guides/recovery/index.html",
            "guides/multi-wan/index.html",
            "methodology/index.html",
            "contributing/index.html",
            "about/index.html",
            "licensing/index.html",
            "404.html",
            "robots.txt",
            "sitemap.xml",
            "manifest.webmanifest",
            "favicon.svg",
            "assets/css/style.css",
            "assets/js/main.js"
        ]
        for rel_path in core_files:
            fpath = os.path.join(SITE_DIR, rel_path)
            self.assertTrue(os.path.exists(fpath), f"Missing core file: {rel_path}")
            self.assertGreater(os.path.getsize(fpath), 0, f"Empty core file: {rel_path}")

    def test_sitemap_validity(self):
        sitemap_path = os.path.join(SITE_DIR, "sitemap.xml")
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        # Ensure url tags exist
        urls = root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url")
        self.assertGreater(len(urls), 25, f"Expected >25 URLs in sitemap, found {len(urls)}")

    def test_all_device_pages_generated(self):
        devices_dir = os.path.join(SITE_DIR, "devices")
        subdirs = [d for d in os.listdir(devices_dir) if os.path.isdir(os.path.join(devices_dir, d))]
        self.assertEqual(len(subdirs), 18, f"Expected 18 device pages, got {len(subdirs)}")
        for d in subdirs:
            page = os.path.join(devices_dir, d, "index.html")
            self.assertTrue(os.path.exists(page), f"Device {d} missing index.html")
            with open(page, "r", encoding="utf-8") as fp:
                html = fp.read()
                self.assertIn("TechArticle", html, f"Device {d} missing JSON-LD TechArticle")
                self.assertIn("<h1", html, f"Device {d} missing H1 tag")

    def test_all_chipset_pages_generated(self):
        chipsets_dir = os.path.join(SITE_DIR, "chipsets")
        subdirs = [c for c in os.listdir(chipsets_dir) if os.path.isdir(os.path.join(chipsets_dir, c))]
        self.assertEqual(len(subdirs), 11, f"Expected 11 chipset pages, got {len(subdirs)}")
        for c in subdirs:
            page = os.path.join(chipsets_dir, c, "index.html")
            self.assertTrue(os.path.exists(page), f"Chipset {c} missing index.html")

    def test_no_file_uris_or_secrets_in_site(self):
        for root, _, files in os.walk(SITE_DIR):
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in [".html", ".css", ".js", ".xml", ".txt", ".md"]:
                    fpath = os.path.join(root, f)
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
                        content = fp.read()
                        self.assertNotIn("file:///", content, f"Hardcoded file:/// in {fpath}")
                        self.assertNotIn("C:\\Users\\", content, f"Hardcoded C:\\Users\\ in {fpath}")

if __name__ == "__main__":
    unittest.main()
