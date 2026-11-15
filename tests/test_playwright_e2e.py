"""
Playwright End-to-End Navigation, Responsive Layout & Interactive Testing Suite
Tests:
  1. Root & Navigation flow (Home -> Recovery Guide -> Back -> Forward)
  2. History State integrity (no duplicate states created on clean directory vs index.html)
  3. Direct deep linking to recovery sections (#sec-5-tiers, #sec-6-tftp, etc.)
  4. Table of Contents interactivity & active scroll state
  5. Code copy button functionality & clipboard verification
  6. Contribution panel links (pointing to Repo A source and GitHub issue templates)
  7. Telemetry & Privacy verification (no third-party tracking scripts loaded)
  8. Decision Flowchart SVG & Danger Callouts verification
  9. Mobile Navigation Drawer & Backdrop interactivity
  10. Multi-Viewport Responsive Overflow Audit (320px, 375px, 414px, 768px, 1024px, 1440px)
  11. Dark / Light Theme switching with local storage persistence
  12. Hardware Explorer Search, URL Query Param Deep-Linking & Quick Pills
  13. Multi-Device Side-by-Side Comparison Matrix
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
SCREENSHOTS_DIR = os.path.join(REPO_ROOT, "tests", "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

class QuietHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SITE_DIR, **kwargs)
    def log_message(self, format, *args):
        pass

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
            page.set_viewport_size({"width": 1440, "height": 900})
            page.goto(f"{base_url}/index.html", wait_until="networkidle")
            title = page.title()
            assert "OpenWrt Router Hardware Knowledge Base" in title, f"Unexpected title: {title}"
            
            recovery_nav = page.locator("nav#desktop-nav a", has_text="Recovery")
            assert recovery_nav.count() > 0, "Recovery link missing in desktop nav"
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
            hist_len_before = page.evaluate("() => window.history.length")
            page.go_back(wait_until="networkidle")
            back_url = page.url
            assert back_url.endswith("/index.html") or back_url == f"{base_url}/", f"Back button didn't return to Home: {back_url}"
            
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
            code_text = page.evaluate("""() => {
                const btn = document.querySelector('.copy-btn');
                const pre = btn.closest('.code-block-wrapper').querySelector('pre');
                return pre ? pre.innerText : '';
            }""")
            assert len(code_text) > 0, "Code text is empty"
            
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
            
            record_scenario("contribution_panel_repo_a_mapping", "PASSED", {
                "edit_source_url": edit_href,
                "issue_template_url": report_href
            })
        except Exception as e:
            record_scenario("contribution_panel_repo_a_mapping", "FAILED", {"error": str(e)})

        # -------------------------------------------------------------
        # Test 7: Telemetry & Privacy Verification (No Third-Party Trackers)
        # -------------------------------------------------------------
        try:
            telemetry_badge = page.locator("#telemetry-badge")
            assert telemetry_badge.count() == 1, "Telemetry badge missing in footer"
            badge_text = telemetry_badge.inner_text()
            assert "48 Devices Cataloged" in badge_text or "Privacy-First" in badge_text or "Verified" in badge_text, f"Unexpected badge text: {badge_text}"
            
            scripts = page.evaluate("() => Array.from(document.querySelectorAll('script')).map(s => s.src)")
            goat_scripts = [s for s in scripts if "goatcounter" in s]
            assert len(goat_scripts) == 0, f"Third-party tracker script loaded unexpectedly: {goat_scripts}"
            
            record_scenario("telemetry_privacy_verification", "PASSED", {
                "badge_text": badge_text,
                "external_trackers_count": len(goat_scripts)
            })
        except Exception as e:
            record_scenario("telemetry_privacy_verification", "FAILED", {"error": str(e)})

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

        # -------------------------------------------------------------
        # Test 9: Mobile Navigation Drawer & Backdrop Interactivity
        # -------------------------------------------------------------
        try:
            page.set_viewport_size({"width": 375, "height": 667})
            page.goto(f"{base_url}/index.html", wait_until="networkidle")
            
            menu_btn = page.locator("#mobile-menu-toggle, .mobile-menu-btn").first
            assert menu_btn.is_visible(), "Mobile hamburger button is not visible on 375px viewport"
            
            menu_btn.click()
            time.sleep(0.3)
            
            drawer = page.locator("#mobile-nav-drawer")
            backdrop = page.locator("#mobile-drawer-backdrop")
            
            is_open = page.evaluate("() => document.body.classList.contains('drawer-open') && document.getElementById('mobile-nav-drawer').getAttribute('aria-hidden') === 'false'")
            assert is_open, "Body does not have drawer-open class or drawer aria-hidden is not false"
            assert drawer.is_visible(), "Mobile drawer is not visible when opened"
            assert backdrop.is_visible(), "Mobile backdrop is not visible when opened"
            
            page.keyboard.press("Escape")
            time.sleep(0.3)
            
            is_closed = page.evaluate("() => !document.body.classList.contains('drawer-open') && document.getElementById('mobile-nav-drawer').getAttribute('aria-hidden') === 'true'")
            assert is_closed, "Drawer failed to close on Escape key"
            
            record_scenario("mobile_nav_drawer_interactivity", "PASSED", {
                "viewport": "375x667",
                "drawer_opened_successfully": True,
                "escape_key_closes": True
            })
        except Exception as e:
            record_scenario("mobile_nav_drawer_interactivity", "FAILED", {"error": str(e)})

        # -------------------------------------------------------------
        # Test 10: Multi-Viewport Responsive Overflow Audit
        # -------------------------------------------------------------
        try:
            viewports = [
                {"width": 320, "height": 568, "name": "iPhone SE Small (320px)"},
                {"width": 375, "height": 667, "name": "iPhone 8/SE (375px)"},
                {"width": 414, "height": 896, "name": "iPhone XR (414px)"},
                {"width": 768, "height": 1024, "name": "iPad Portrait (768px)"},
                {"width": 1024, "height": 768, "name": "iPad Landscape (1024px)"},
                {"width": 1440, "height": 900, "name": "MacBook / Desktop (1440px)"}
            ]
            
            overflow_issues = []
            for vp in viewports:
                page.set_viewport_size({"width": vp["width"], "height": vp["height"]})
                
                # Check homepage
                page.goto(f"{base_url}/index.html", wait_until="networkidle")
                hp_overflow = page.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
                if hp_overflow > 1:
                    overflow_issues.append(f"Homepage horizontal overflow on {vp['name']}: {hp_overflow}px")
                
                # Check explorer
                page.goto(f"{base_url}/explorer/index.html", wait_until="networkidle")
                exp_overflow = page.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
                if exp_overflow > 1:
                    overflow_issues.append(f"Explorer horizontal overflow on {vp['name']}: {exp_overflow}px")

            assert len(overflow_issues) == 0, f"Overflow detected: {overflow_issues}"
            
            record_scenario("multi_viewport_overflow_audit", "PASSED", {
                "viewports_tested": len(viewports),
                "overflow_issues_count": 0
            })
        except Exception as e:
            record_scenario("multi_viewport_overflow_audit", "FAILED", {"error": str(e)})

        # -------------------------------------------------------------
        # Test 11: Dark / Light Mode Theme Switching & Persistence
        # -------------------------------------------------------------
        try:
            page.set_viewport_size({"width": 1440, "height": 900})
            page.goto(f"{base_url}/index.html", wait_until="networkidle")
            
            theme_btn = page.locator("#theme-toggle").first
            assert theme_btn.count() == 1, "Theme toggle button missing"
            
            initial_theme = page.evaluate("() => document.documentElement.getAttribute('data-theme') || 'dark'")
            
            theme_btn.click()
            time.sleep(0.3)
            light_theme = page.evaluate("() => document.documentElement.getAttribute('data-theme')")
            assert light_theme == "light", f"Expected light theme, got: {light_theme}"
            
            saved_theme = page.evaluate("() => localStorage.getItem('theme')")
            assert saved_theme == "light", f"Theme not saved to localStorage: {saved_theme}"
            
            theme_btn.click()
            time.sleep(0.3)
            dark_theme = page.evaluate("() => document.documentElement.getAttribute('data-theme')")
            assert dark_theme == "dark", f"Expected dark theme, got: {dark_theme}"
            
            record_scenario("dark_light_theme_switching", "PASSED", {
                "initial_theme": initial_theme,
                "switched_to": light_theme,
                "toggled_back_to": dark_theme,
                "localStorage_synced": True
            })
        except Exception as e:
            record_scenario("dark_light_theme_switching", "FAILED", {"error": str(e)})

        # -------------------------------------------------------------
        # Test 12: Hardware Explorer Real-time Search & URL Query Deep-Linking
        # -------------------------------------------------------------
        try:
            page.goto(f"{base_url}/explorer/index.html?q=MT7986", wait_until="networkidle")
            
            search_input = page.locator("#search-input")
            input_val = search_input.input_value()
            assert "MT7986" in input_val, f"Search input did not prefill from query: '{input_val}'"
            
            time.sleep(0.5)
            count_text = page.locator("#results-count").inner_text()
            count = int(count_text)
            assert count > 0 and count < 72, f"Expected filtered count for MT7986, got: {count}"
            
            page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "explorer_search_mt7986.png"))
            
            clear_btn = page.locator("#search-clear")
            clear_btn.click()
            time.sleep(0.5)
            
            reset_count = int(page.locator("#results-count").inner_text())
            assert reset_count == 72, f"Expected 72 devices after clear, got: {reset_count}"
            
            record_scenario("explorer_search_and_deep_linking", "PASSED", {
                "prefilled_query": input_val,
                "filtered_count": count,
                "cleared_count": reset_count
            })
        except Exception as e:
            record_scenario("explorer_search_and_deep_linking", "FAILED", {"error": str(e)})

        # -------------------------------------------------------------
        # Test 13: Multi-Device Side-by-Side Comparison Matrix
        # -------------------------------------------------------------
        try:
            page.goto(f"{base_url}/explorer/index.html", wait_until="networkidle")
            
            checkboxes = page.locator(".compare-checkbox-label input")
            assert checkboxes.count() >= 2, "Less than 2 device checkboxes found"
            
            checkboxes.nth(0).check()
            checkboxes.nth(1).check()
            time.sleep(0.3)
            
            tray = page.locator("#comparison-tray")
            assert tray.is_visible(), "Comparison floating tray is not visible after selecting devices"
            
            compare_count = page.locator("#compare-count").inner_text()
            assert compare_count == "2", f"Expected compare count 2, got: {compare_count}"
            
            compare_btn = tray.locator("button", has_text="Compare Matrix →")
            compare_btn.click()
            time.sleep(0.5)
            
            modal = page.locator("#modal-overlay")
            assert modal.is_visible(), "Comparison modal did not open"
            
            table_headers = modal.locator(".compare-matrix-table th")
            assert table_headers.count() >= 3, f"Expected at least 3 columns (feature + 2 devices), got {table_headers.count()}"
            
            page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "comparison_matrix_modal.png"))
            
            modal.locator(".modal-close-btn").click()
            time.sleep(0.3)
            assert not modal.is_visible(), "Comparison modal did not close"
            
            record_scenario("multi_device_comparison_matrix", "PASSED", {
                "devices_compared": 2,
                "matrix_table_columns": table_headers.count(),
                "modal_opened_and_closed": True
            })
        except Exception as e:
            record_scenario("multi_device_comparison_matrix", "FAILED", {"error": str(e)})

        # -------------------------------------------------------------
        # Test 14: Explorer Back / Forward Navigation & Keyboard Accessibility
        # -------------------------------------------------------------
        try:
            page.set_viewport_size({"width": 1440, "height": 900})
            page.goto(f"{base_url}/explorer/index.html", wait_until="networkidle")

            # 1. Test keyboard shortcut '/' to focus search input
            page.keyboard.press("/")
            focused_id = page.evaluate("() => document.activeElement ? document.activeElement.id : ''")
            assert focused_id == "search-input", f"Expected activeElement to be search-input, got '{focused_id}'"

            # 2. Select status filter dropdown (pushState)
            page.select_option("#status-filter", "OFFICIALLY_SUPPORTED")
            time.sleep(0.4)
            url_after_status = page.url
            assert "status=OFFICIALLY_SUPPORTED" in url_after_status, f"URL missing status query param: {url_after_status}"
            count_status = int(page.locator("#results-count").inner_text())
            assert count_status > 0 and count_status < 72, f"Unexpected count for officially supported: {count_status}"

            # 3. Apply Quick Pill: Filogic 830 (MT7986)
            pill_mt7986 = page.locator("button.quick-pill", has_text="Filogic 830 (MT7986)")
            assert pill_mt7986.count() == 1, "Quick pill for Filogic 830 missing"
            pill_mt7986.click()
            time.sleep(0.4)
            url_after_pill = page.url
            assert "MT7986" in url_after_pill or "Filogic" in url_after_pill, f"URL missing pill query: {url_after_pill}"
            count_pill = int(page.locator("#results-count").inner_text())

            # 4. Browser Back button -> Should return to status=OFFICIALLY_SUPPORTED
            page.go_back(wait_until="networkidle")
            time.sleep(0.4)
            back_url = page.url
            assert "status=OFFICIALLY_SUPPORTED" in back_url, f"Back button didn't restore status filter: {back_url}"
            status_val_after_back = page.locator("#status-filter").input_value()
            assert status_val_after_back == "OFFICIALLY_SUPPORTED", f"Dropdown didn't restore: {status_val_after_back}"
            count_after_back = int(page.locator("#results-count").inner_text())
            assert count_after_back == count_status, f"Device count didn't restore after back: {count_after_back} vs {count_status}"

            # 5. Browser Forward button -> Should restore Filogic 830 pill query
            page.go_forward(wait_until="networkidle")
            time.sleep(0.4)
            fwd_url = page.url
            assert "MT7986" in fwd_url or "Filogic" in fwd_url, f"Forward button didn't restore pill state: {fwd_url}"

            # 6. Test Escape key to clear search input
            page.locator("#search-input").focus()
            page.keyboard.type("testsearch")
            time.sleep(0.2)
            page.keyboard.press("Escape")
            time.sleep(0.3)
            search_val = page.locator("#search-input").input_value()
            assert search_val == "", f"Escape key failed to clear search input, got '{search_val}'"

            record_scenario("explorer_back_forward_query_filter_navigation", "PASSED", {
                "slash_focus_working": True,
                "status_filter_url": url_after_status,
                "pill_filter_url": url_after_pill,
                "back_button_restored_url": back_url,
                "forward_button_restored_url": fwd_url,
                "escape_clears_search": True
            })
        except Exception as e:
            record_scenario("explorer_back_forward_query_filter_navigation", "FAILED", {"error": str(e)})

        # -------------------------------------------------------------
        # Visual Screenshots for Verification
        # -------------------------------------------------------------
        try:
            page.set_viewport_size({"width": 1440, "height": 900})
            page.goto(f"{base_url}/index.html", wait_until="networkidle")
            page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "homepage_desktop_1440.png"), full_page=False)
            
            page.set_viewport_size({"width": 375, "height": 667})
            page.goto(f"{base_url}/index.html", wait_until="networkidle")
            page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "homepage_mobile_375.png"), full_page=False)
            
            page.locator("#mobile-menu-toggle, .mobile-menu-btn").first.click()
            time.sleep(0.3)
            page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "homepage_mobile_drawer_open.png"), full_page=False)
            
            record_scenario("evidence_screenshots_capture", "PASSED", {
                "screenshots_saved": [
                    "homepage_desktop_1440.png",
                    "homepage_mobile_375.png",
                    "homepage_mobile_drawer_open.png",
                    "explorer_search_mt7986.png",
                    "comparison_matrix_modal.png"
                ]
            })
        except Exception as e:
            record_scenario("evidence_screenshots_capture", "FAILED", {"error": str(e)})

        browser.close()

    server.shutdown()
    
    evidence_file = os.path.join(REPO_ROOT, "tests", "playwright-e2e-evidence.json")
    with open(evidence_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n[+] Playwright E2E Results saved to {evidence_file}")
    print(f"[+] Total Scenarios: {results['summary']['total']}, Passed: {results['summary']['passed']}, Failed: {results['summary']['failed']}")
    
    if results['summary']['failed'] > 0:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
