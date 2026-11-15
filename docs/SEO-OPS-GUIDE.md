# Google Search Console & Technical SEO Operations Runbook

**Platform:** Global OpenWrt Router Hardware Knowledge Base  
**Canonical Domain:** `https://rny0007.github.io/openwrt-router-hardware-explorer/`  
**Authoritative Source:** [Rny0007/mt7986-openwrt-router-guide](https://github.com/Rny0007/mt7986-openwrt-router-guide)  
**Standard:** OpenWrt Technical SEO & Rich Snippet Specification v2.2  

---

## 1. Google Search Console Setup & Verification

### 1.1 Property Configuration
- **Property Type:** URL-prefix property: `https://rny0007.github.io/openwrt-router-hardware-explorer/`
- **Recommended Verification Method:** HTML Tag or GitHub Repository DNS TXT Record.
- **Verification Tag Insertion:** The `<meta name="google-site-verification" content="...">` tag is injected into `scripts/build-website.py` `get_header()`.

### 1.2 Sitemap Submission
Submit the master XML sitemap immediately after initial deployment:
```
Sitemap URL: https://rny0007.github.io/openwrt-router-hardware-explorer/sitemap.xml
```
- **Total Indexed URLs:** 258+ canonical URLs (Root, Explorer, Categories Hub, 8 Search Intent Guides, 72 Device Profiles, 72 Installation Guides, 72 Recovery Guides, 20 Silicon Architectures, API Docs).
- **Update Frequency:** Rebuilt and re-stamped with ISO 8601 `lastmod` on every production build.

---

## 2. Structured Data & Rich Results Validation

The platform automatically injects Schema.org JSON-LD structured data into all published pages:

| Page Category | Schema.org Type | Key Properties Validated |
|---|---|---|
| **Device Profiles** | `TechArticle` / `Product` | `headline`, `description`, `author`, `publisher`, `mainEntityOfPage` |
| **Category Landing Pages** | `ItemList` & `TechArticle` | `itemListElement` array, `position`, `name`, `url` |
| **Installation & Recovery Guides** | `HowTo` / `TechArticle` | `step` array, `tool`, `supply`, `estimatedCost`, `prepTime` |
| **Silicon Architecture Pages** | `TechArticle` | `about`, `operatingSystem`, `processorArchitecture` |
| **Public API Documentation** | `WebAPI` | `name`, `documentation`, `termsOfService`, `license` |
| **All Pages** | `BreadcrumbList` | Hierarchical trail: Home → Directory → Target Item |

### Testing Procedure
Validate rich snippet compliance using the Google Rich Results Test:
```bash
# Test Rich Snippets via Google Search Console API or Web Interface:
https://search.google.com/test/rich-results?url=https%3A%2F%2Frny0007.github.io%2Fopenwrt-router-hardware-explorer%2Fdevices%2Fjio-jidu6101%2F
```

---

## 3. Canonical URLs & Trailing Slash Policy

To eliminate duplicate content penalties in Google's indexing pipeline:
1. **Directory-Based Routing:** Every resource resolves to a directory with a trailing slash (e.g. `/devices/jio-jidu6101/`).
2. **Explicit Canonical Tags:** Every HTML document emits an explicit `<link rel="canonical" href="https://rny0007.github.io/openwrt-router-hardware-explorer/path/">`.
3. **Open Graph Mirrors:** `og:url` strictly mirrors the canonical URL to prevent Facebook/Twitter scraping divergence.
4. **Automated Audit Suite:** Run `tests/audit_site_html.py` before every release to guarantee:
   - 0 missing canonical tags.
   - 0 duplicate meta descriptions.
   - Exactly 1 `<h1>` heading per page.

---

## 4. Crawl Optimization & robots.txt

The production `robots.txt` is statically generated to permit search engines to index all hardware documentation while cleanly disallowing internal scratch or test directories:

```
User-agent: *
Allow: /
Disallow: /tests/
Disallow: /scratch/
Sitemap: https://rny0007.github.io/openwrt-router-hardware-explorer/sitemap.xml
```

---

## 5. Privacy-Conscious Telemetry & Analytics

The website utilizes **GoatCounter** for privacy-conscious, cookieless, GDPR-compliant analytics:
- **No Cookies:** Complies with EU ePrivacy and GDPR regulations without requiring invasive cookie banners.
- **No Personal Data:** IP addresses are hashed with a daily salt and never stored.
- **Clean Fallback:** If `GOATCOUNTER_CODE` is empty in `scripts/build-website.py`, telemetry scripts are omitted entirely with zero console errors or network warnings.

---

## 6. Search Console Performance Monitoring Checklist

Weekly operations protocol:
1. **Index Coverage Report:** Verify 0 pages marked *Error* (5xx) or *Excluded* (crawl anomalies).
2. **URL Inspection:** Inspect high-priority intent pages (e.g. `/categories/best-openwrt-routers/`).
3. **Core Web Vitals:** Verify LCP < 2.5s, FID/INP < 200ms, and CLS < 0.1 across desktop and mobile.
4. **Search Queries Monitoring:** Track CTR for high-volume keywords:
   - *"openwrt compatible routers 2026"*
   - *"openwrt wifi 7 router support"*
   - *"jidu6101 openwrt installation"*
   - *"linksys wrt1900acs openwrt recovery"*
   - *"best openwrt travel router wireguard"*
