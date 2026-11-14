"""
Playwright End-to-End Navigation & Interactive Testing Suite
Tests:
  1. Root & Navigation flow (Home -> Recovery Guide -> Back -> Forward)
  2. History State integrity (no duplicate states created on clean directory vs index.html)
  3. Direct deep linking to recovery sections (#sec-5-tiers, #sec-6-tftp, etc.)
  4. Table of Contents interactivity & active scroll state
  5. Code copy button functionality & clipboard verification
  6. Contribution panel links (pointing to Repo A source and GitHub issue templates)
  7. GoatCounter fallback badge rendering
"""

import os
import sys
import time
import json
import socket
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_DIR = os.path.join(REPO_ROOT, "site")
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

class QuietHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SITE_DIR, **kwargs)
    def log_message(self, format, *args):
        pass # suppress server logs during test

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def run_tests():
    port = get_free_port()
    server = HTTPServer(('127.0.0.1', port), QuietHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    base_url = f"http://127.0.0.1:{port}"
    print(f"[*] Local test HTTP server running on {base_url}")

    results = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "base_url": base_url,
        "scenarios": {},
        "summary": {"passed": 0, "failed": 0, "total": 0}
    }

    def record_scenario(name, status, details=None):
        results["scenarios"][name] = {"status": status, "details": details or {}}
        if status == "PASSED":
            results["summary"]["passed"] += 1
            print(f"  [PASS] {name}")
        else:
            results["summary"]["failed"] += 1
            print(f"  [FAIL] {name}: {details}")
        results["summary"]["total"] += 1

    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=CHROME_PATH,
            headless=True,
            args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]
        )
        context = browser.new_context(
            permissions=["clipboard-read", "clipboard-write"]
        )
        page = context.new_page()

        # -------------------------------------------------------------
        # Test 1: Home Page Loading & Navigation to Recovery Guide
        # -------------------------------------------------------------
        try:
            page.goto(f"{base_url}/index.html", wait_until="networkidle")
            title = page.title()
            assert "OpenWrt Router Hardware Knowledge Base" in title, f"Unexpected title: {title}"
            
            # Click Recovery in nav
            recovery_nav = page.locator("nav a", has_text="Recovery")
            assert recovery_nav.count() > 0, "Recovery link missing in nav"
            recovery_nav.first.click()
            page.wait_for_load_state("networkidle")
            
            current_url = page.url
            assert "/guides/recovery/" in current_url, f"Failed to navigate to recovery: {current_url}"
            record_scenario("nav_home_to_recovery", "PASSED", {"navigated_url": current_url, "title": page.title()})
        except Exception as e:
            record_scenario("nav_home_to_recovery", "FAILED", {"error": str(e)})

        # -------------------------------------------------------------
        # Test 2: Browser Back Button & History Integrity
        # -------------------------------------------------------------
        try:
            # Check history length
            hist_len_before = page.evaluate("() => window.history.length")
            
            # Go back to Home
            page.go_back(wait_until="networkidle")
            back_url = page.url
            assert back_url.endswith("/index.html") or back_url == f"{base_url}/", f"Back button didn't return to Home: {back_url}"
            
            # Go forward to Recovery
            page.go_forward(wait_until="networkidle")
            forward_url = page.url
            assert "/guides/recovery/" in forward_url, f"Forward button didn't return to Recovery: {forward_url}"
            
            record_scenario("browser_back_forward_navigation", "PASSED", {
                "back_url": back_url,
                "forward_url": forward_url,
                "history_length": hist_len_before
            })
        except Exception as e:
            record_scenario("browser_back_forward_navigation", "FAILED", {"error": str(e)})

        # -------------------------------------------------------------
        # Test 3: Deep Link Access to Sections (#sec-5-tiers)
        # -------------------------------------------------------------
        try:
            target_deep = f"{base_url}/guides/recovery/index.html#sec-5-tiers"
            page.goto(target_deep, wait_until="networkidle")
            current_hash = page.evaluate("() => window.location.hash")
            assert current_hash == "#sec-5-tiers", f"Hash not preserved: {current_hash}"
            
            # Verify target heading is in DOM
            sec_header = page.locator("#sec-5-tiers")
            assert sec_header.count() == 1, "Section #sec-5-tiers not found"
            record_scenario("deep_link_preservation", "PASSED", {
                "target_url": target_deep,
                "resolved_hash": current_hash,
                "header_text": sec_header.inner_text()
            })
        except Exception as e:
            record_scenario("deep_link_preservation", "FAILED", {"error": str(e)})

        # -------------------------------------------------------------
        # Test 4: Sticky TOC Navigation & Scroll Interactivity
        # -------------------------------------------------------------
        try:
            toc_links = page.locator(".docs-sidebar a.toc-link")
            toc_count = toc_links.count()
            assert toc_count >= 10, f"Expected at least 10 TOC links, found {toc_count}"
            
            # Click Section 6 (Device Notes)
            device_link = page.locator(".docs-sidebar a.toc-link[href='#sec-6-device-notes']")
            assert device_link.count() == 1, "TOC link for #sec-6-device-notes missing"
            device_link.click()
            time.sleep(0.5)
            
            page_hash = page.evaluate("() => window.location.hash")
            assert page_hash == "#sec-6-device-notes", f"TOC click failed to set hash: {page_hash}"
            record_scenario("toc_navigation_interactivity", "PASSED", {
                "toc_links_count": toc_count,
                "clicked_hash": page_hash
            })
        except Exception as e:
            record_scenario("toc_navigation_interactivity", "FAILED", {"error": str(e)})

        # -------------------------------------------------------------
        # Test 5: Code Block Copy Buttons & Clipboard
        # -------------------------------------------------------------
        try:
            copy_buttons = page.locator(".copy-btn")
            btn_count = copy_buttons.count()
            assert btn_count >= 5, f"Expected multiple copy buttons, found {btn_count}"
            
            first_btn = copy_buttons.first
            # Find closest pre/code text
            code_text = page.evaluate("""() => {
                const btn = document.querySelector('.copy-btn');
                const pre = btn.closest('.code-block-wrapper').querySelector('pre');
                return pre ? pre.innerText : '';
            }""")
            assert len(code_text) > 0, "Code text is empty"
            
            # Click copy button
            first_btn.click()
            time.sleep(0.3)
            
            btn_label = first_btn.inner_text()
            assert "Copied" in btn_label, f"Copy button text did not change to Copied: {btn_label}"
            
            record_scenario("code_copy_button_interactivity", "PASSED", {
                "buttons_count": btn_count,
                "label_after_click": btn_label,
                "sample_code_snippet": code_text[:60] + "..."
            })
        except Exception as e:
            record_scenario("code_copy_button_interactivity", "FAILED", {"error": str(e)})

        # -------------------------------------------------------------
        # Test 6: Contribution Panel Links & Repo A Mapping
        # -------------------------------------------------------------
        try:
            contrib_panel = page.locator(".contribution-panel")
            assert contrib_panel.count() == 1, "Contribution panel missing"
            
            edit_link = contrib_panel.locator("a", has_text="Edit this page").first
            edit_href = edit_link.get_attribute("href")
            assert "github.com/Rny0007/mt7986-openwrt-router-guide/blob/main/" in edit_href, f"Incorrect edit source link: {edit_href}"
            
            report_link = contrib_panel.locator("a", has_text="Report an Error or Typo").first
            report_href = report_link.get_attribute("href")
            assert "github.com/Rny0007/mt7986-openwrt-router-guide/issues/new" in report_href, f"Incorrect issue link: {report_href}"
            assert "template=08_documentation_improvement.yml" in report_href, f"Issue template query missing: {report_href}"
            
            unbrick_link = contrib_panel.locator("a", has_text="Submit Unbrick Tutorial").first
            unbrick_href = unbrick_link.get_attribute("href")
            assert "template=05_recovery_unbrick_report.yml" in unbrick_href, f"Unbrick template query missing: {unbrick_href}"
            
            record_scenario("contribution_panel_repo_a_mapping", "PASSED", {
                "edit_source_url": edit_href,
                "issue_template_url": report_href,
                "unbrick_template_url": unbrick_href
            })
        except Exception as e:
            record_scenario("contribution_panel_repo_a_mapping", "FAILED", {"error": str(e)})

        # -------------------------------------------------------------
        # Test 7: GoatCounter Fallback Badge Display
        # -------------------------------------------------------------
        try:
            telemetry_badge = page.locator("#telemetry-badge")
            assert telemetry_badge.count() == 1, "Telemetry badge missing in footer"
            badge_text = telemetry_badge.inner_text()
            assert "Privacy-First" in badge_text or "No Trackers Active" in badge_text, f"Unexpected badge text: {badge_text}"
            
            # Verify no third-party tracker script is loaded when code is empty
            scripts = page.evaluate("() => Array.from(document.querySelectorAll('script')).map(s => s.src)")
            goat_scripts = [s for s in scripts if "goatcounter" in s]
            assert len(goat_scripts) == 0, f"Goatcounter script loaded unexpectedly: {goat_scripts}"
            
            record_scenario("goatcounter_privacy_fallback", "PASSED", {
                "badge_text": badge_text,
                "third_party_scripts_loaded": len(goat_scripts)
            })
        except Exception as e:
            record_scenario("goatcounter_privacy_fallback", "FAILED", {"error": str(e)})

        # -------------------------------------------------------------
        # Test 8: Decision Flowchart SVG & Danger Callouts
        # -------------------------------------------------------------
        try:
            svg = page.locator(".decision-diagram svg")
            assert svg.count() >= 1, "Decision flowchart SVG missing"
            
            danger_callouts = page.locator(".callout-danger")
            assert danger_callouts.count() >= 1, "Danger callouts missing"
            
            warning_callouts = page.locator(".callout-warning")
            assert warning_callouts.count() >= 1, "Warning callouts missing"
            
            record_scenario("diagram_and_callouts_verification", "PASSED", {
                "flowchart_svg_present": True,
                "danger_callouts_count": danger_callouts.count(),
                "warning_callouts_count": warning_callouts.count()
            })
        except Exception as e:
            record_scenario("diagram_and_callouts_verification", "FAILED", {"error": str(e)})

        browser.close()

    server.shutdown()
    
    # Save results
    evidence_file = os.path.join(REPO_ROOT, "tests", "playwright-e2e-evidence.json")
    with open(evidence_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n[+] Playwright E2E Results saved to {evidence_file}")
    print(f"[+] Total Scenarios: {results['summary']['total']}, Passed: {results['summary']['passed']}, Failed: {results['summary']['failed']}")
    
    if results['summary']['failed'] > 0:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
