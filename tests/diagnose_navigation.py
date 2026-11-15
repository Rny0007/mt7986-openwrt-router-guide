import sys
import json
from playwright.sync_api import sync_playwright

CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
BASE_URL = "https://rny0007.github.io/openwrt-router-hardware-explorer"

results = {
    "test_1_home_to_recovery_and_back": {},
    "test_2_direct_recovery_and_back": {},
    "test_3_forward_navigation": {},
    "test_4_refresh": {},
    "test_5_deep_link": {},
    "test_6_trailing_slash_variants": {},
    "observed_issues": []
}

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Track console messages and redirects
    console_logs = []
    page.on("console", lambda msg: console_logs.append(f"[{msg.type}] {msg.text}"))

    # Test 1: Homepage -> Recovery guide -> browser Back
    print("Running Test 1: Home -> Recovery -> Back...")
    page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
    home_url = page.url
    
    # Click Recovery link
    recovery_link = page.locator("a[href*='guides/recovery']")
    if recovery_link.count() > 0:
        recovery_link.first.click()
        page.wait_for_load_state("networkidle")
        recovery_url_after_click = page.url
        # Go back
        page.go_back(wait_until="networkidle")
        url_after_back = page.url
        results["test_1_home_to_recovery_and_back"] = {
            "initial_home": home_url,
            "after_click": recovery_url_after_click,
            "after_back": url_after_back,
            "back_successful": (url_after_back == home_url)
        }
    else:
        results["test_1_home_to_recovery_and_back"] = {"error": "Recovery link not found on homepage"}

    # Test 2: Open recovery URL directly -> browser Back
    print("Running Test 2: Direct Recovery URL -> Back...")
    page.goto(f"{BASE_URL}/guides/recovery/index.html", wait_until="networkidle")
    direct_url = page.url
    page.go_back(wait_until="networkidle")
    url_after_direct_back = page.url
    results["test_2_direct_recovery_and_back"] = {
        "direct_url": direct_url,
        "after_back": url_after_direct_back,
        "note": "When opened directly with no history, go_back remains on direct_url or about:blank"
    }

    # Test 3: Forward navigation
    print("Running Test 3: Forward Navigation...")
    page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
    page.goto(f"{BASE_URL}/guides/recovery/index.html", wait_until="networkidle")
    page.go_back(wait_until="networkidle")
    page.go_forward(wait_until="networkidle")
    results["test_3_forward_navigation"] = {
        "forward_url": page.url,
        "forward_successful": ("guides/recovery" in page.url)
    }

    # Test 4: Refresh
    print("Running Test 4: Refresh...")
    page.reload(wait_until="networkidle")
    results["test_4_refresh"] = {
        "refreshed_url": page.url,
        "refresh_successful": ("guides/recovery" in page.url)
    }

    # Test 5: Deep-link access
    print("Running Test 5: Deep-link Access...")
    page.goto(f"{BASE_URL}/guides/recovery/index.html#tier-3", wait_until="networkidle")
    results["test_5_deep_link"] = {
        "deep_link_url": page.url,
        "deep_link_successful": ("#tier-3" in page.url or "guides/recovery" in page.url)
    }

    # Test 6: Trailing slash vs index.html variants
    print("Running Test 6: Trailing slash variants...")
    variants = [
        f"{BASE_URL}/guides/recovery",
        f"{BASE_URL}/guides/recovery/",
        f"{BASE_URL}/guides/recovery/index.html"
    ]
    variant_results = {}
    for v in variants:
        resp = page.goto(v, wait_until="networkidle")
        variant_results[v] = {
            "status": resp.status if resp else "N/A",
            "final_url": page.url
        }
    results["test_6_trailing_slash_variants"] = variant_results

    # Check for inconsistencies
    # Compare clean directory URL vs index.html
    # In GitHub Pages, visiting /guides/recovery without trailing slash gets 301 to /guides/recovery/
    clean_resp = variant_results.get(f"{BASE_URL}/guides/recovery")
    slash_resp = variant_results.get(f"{BASE_URL}/guides/recovery/")
    html_resp = variant_results.get(f"{BASE_URL}/guides/recovery/index.html")

    if html_resp and slash_resp and clean_resp:
        results["analysis"] = {
            "clean_url_final": clean_resp["final_url"],
            "slash_url_final": slash_resp["final_url"],
            "html_url_final": html_resp["final_url"]
        }

    browser.close()

print("\n--- DIAGNOSIS RESULTS ---")
print(json.dumps(results, indent=2))
with open("C:\\Users\\mrrny\\Desktop\\mt7986-openwrt-router-guide\\tests\\diagnosis-evidence.json", "w", encoding="utf-8") as out:
    json.dump(results, out, indent=2)
