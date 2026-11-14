#!/usr/bin/env python3
"""
scripts/build-website.py
Generates the complete, professional, zero-dependency static website
for the Global OpenWrt Router Hardware Knowledge Base & Explorer.
Outputs to: site/
"""

import os
import sys
import json
import shutil
import urllib.parse
from datetime import datetime, timezone

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(REPO_ROOT, "data")
DEVICES_DIR = os.path.join(DATA_DIR, "devices")
CHIPSETS_DIR = os.path.join(DATA_DIR, "chipsets")
SITE_DIR = os.path.join(REPO_ROOT, "site")

BASE_URL = "https://rny0007.github.io/openwrt-router-hardware-explorer"

# Optional GoatCounter Site Code (Leave empty string to keep disabled with clean fallback)
GOATCOUNTER_CODE = ""

def load_data():
    devices = []
    for root, _, files in os.walk(DEVICES_DIR):
        for f in files:
            if f.endswith(".json"):
                with open(os.path.join(root, f), "r", encoding="utf-8") as fp:
                    devices.append(json.load(fp))
    devices.sort(key=lambda d: (d.get("manufacturer", ""), d.get("model", "")))

    chipsets = []
    for root, _, files in os.walk(CHIPSETS_DIR):
        for f in files:
            if f.endswith(".json"):
                with open(os.path.join(root, f), "r", encoding="utf-8") as fp:
                    chipsets.append(json.load(fp))
    chipsets.sort(key=lambda c: (c.get("vendor", ""), c.get("part_number", "")))

    return devices, chipsets

def get_header(title, rel_root=".", current_nav="", description=None, canonical_path=None, json_ld=None):
    nav_links = [
        ("Home", f"{rel_root}/index.html", "home"),
        ("Explorer", f"{rel_root}/explorer/index.html", "explorer"),
        ("Devices", f"{rel_root}/devices/index.html", "devices"),
        ("Chipsets", f"{rel_root}/chipsets/index.html", "chipsets"),
        ("Diagrams", f"{rel_root}/diagrams/index.html", "diagrams"),
        ("Installation", f"{rel_root}/guides/installation/index.html", "installation"),
        ("Recovery", f"{rel_root}/guides/recovery/index.html", "recovery"),
        ("Failover", f"{rel_root}/guides/multi-wan/index.html", "multi-wan"),
        ("Methodology", f"{rel_root}/methodology/index.html", "methodology"),
        ("About", f"{rel_root}/about/index.html", "about"),
    ]

    nav_html = ""
    for label, url, key in nav_links:
        active_cls = ' class="active"' if current_nav == key else ''
        nav_html += f'<a href="{url}"{active_cls}>{label}</a>\n'

    desc = description or f"Technical reference, specifications, and OpenWrt compatibility documentation for {title}."
    canon_url = f"{BASE_URL}/{canonical_path}" if canonical_path is not None else f"{BASE_URL}/"

    json_ld_script = ""
    if json_ld:
        json_ld_script = f"""  <script type="application/ld+json">
{json.dumps(json_ld, indent=2)}
  </script>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — OpenWrt Router Hardware Knowledge Base</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canon_url}">
  <meta property="og:title" content="{title} — OpenWrt Router Hardware Knowledge Base">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canon_url}">
  <meta property="og:site_name" content="OpenWrt Router Hardware Knowledge Base">
  <meta property="og:type" content="article">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <link rel="icon" type="image/svg+xml" href="{rel_root}/assets/favicon.svg">
  <link rel="manifest" href="{rel_root}/manifest.webmanifest">
  <link rel="stylesheet" href="{rel_root}/assets/css/style.css">
{json_ld_script}
</head>
<body>
  <header class="site-header">
    <div class="header-inner">
      <a href="{rel_root}/index.html" class="brand">
        <svg class="logo-icon" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect width="32" height="32" rx="8" fill="#1e293b"/>
          <path d="M6 16C6 10.4772 10.4772 6 16 6C21.5228 6 26 10.4772 26 16" stroke="#06b6d4" stroke-width="2.5" stroke-linecap="round"/>
          <path d="M10 16C10 12.6863 12.6863 10 16 10C19.3137 10 22 12.6863 22 16" stroke="#10b981" stroke-width="2.5" stroke-linecap="round"/>
          <circle cx="16" cy="16" r="2.5" fill="#f8fafc"/>
          <rect x="8" y="21" width="16" height="5" rx="2" fill="#334155"/>
          <circle cx="12" cy="23.5" r="1" fill="#10b981"/>
          <circle cx="16" cy="23.5" r="1" fill="#06b6d4"/>
          <circle cx="20" cy="23.5" r="1" fill="#f59e0b"/>
        </svg>
        <span class="brand-text">OpenWrt<strong>HardwareKB</strong></span>
      </a>
      <nav class="nav-links">
        {nav_html}
      </nav>
      <div class="header-actions">
        <button id="theme-toggle" class="btn-icon" aria-label="Toggle theme">
          <svg class="sun-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
          <svg class="moon-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        </button>
        <a href="https://github.com/Rny0007/mt7986-openwrt-router-guide" target="_blank" rel="noopener" class="btn btn-sm btn-outline">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/></svg>
          Source Repo
        </a>
      </div>
    </div>
  </header>
  <main class="main-content">
"""

def get_footer(rel_root=".", goatcounter_code=""):
    gc_script = ""
    if goatcounter_code:
        gc_script = f'<script data-goatcounter="https://{goatcounter_code}.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'

    return f"""
  </main>
  <footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-col">
        <h3>OpenWrt Hardware Knowledge Base</h3>
        <p>An independent, evidence-based hardware taxonomy, reverse-engineering repository, and operational deployment guide for open-source router hardware.</p>
        <p class="copyright">Docs: <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener">CC BY 4.0</a> | Code: <a href="https://opensource.org/licenses/MIT" target="_blank" rel="noopener">MIT License</a></p>
        <div class="visitor-telemetry" style="margin-top: 1rem;">
          <span class="telemetry-badge" id="telemetry-badge">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
            Cookie-Free Analytics: <strong>{f"Active ({goatcounter_code})" if goatcounter_code else "Privacy-First / No Trackers Active"}</strong>
          </span>
        </div>
      </div>
      <div class="footer-col">
        <h4>Navigation</h4>
        <ul>
          <li><a href="{rel_root}/explorer/index.html">Hardware Explorer</a></li>
          <li><a href="{rel_root}/devices/index.html">Device Directory</a></li>
          <li><a href="{rel_root}/chipsets/index.html">Silicon Architectures</a></li>
          <li><a href="{rel_root}/diagrams/index.html">Interactive Diagrams</a></li>
          <li><a href="{rel_root}/guides/installation/index.html">Two-Stage Installation</a></li>
          <li><a href="{rel_root}/guides/recovery/index.html">TFTP & UART Recovery</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Community & Standards</h4>
        <ul>
          <li><a href="{rel_root}/methodology/index.html">Research Methodology</a></li>
          <li><a href="{rel_root}/contributing/index.html">Contributor Handbook</a></li>
          <li><a href="{rel_root}/about/index.html">Project Governance</a></li>
          <li><a href="{rel_root}/licensing/index.html">Licensing & Attribution</a></li>
          <li><a href="https://github.com/Rny0007/mt7986-openwrt-router-guide/issues" target="_blank" rel="noopener">Submit Hardware Verification</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>Independent research project. Not affiliated with or endorsed by OpenWrt, Reliance Jio, MediaTek, Arcadyan, Qualcomm, Broadcom, or ASUS.</p>
    </div>
  </footer>
  <script src="{rel_root}/assets/js/main.js"></script>
  {gc_script}
</body>
</html>
"""

def get_contribution_panel(source_path, page_title, rel_root="."):
    enc_path = urllib.parse.quote(source_path)
    enc_title = urllib.parse.quote(f"[Docs]: Feedback on {page_title}")
    enc_unbrick_title = urllib.parse.quote(f"[Recovery]: Unbrick Verification for {page_title}")
    enc_verify_title = urllib.parse.quote(f"[Verification]: Tested Hardware on {page_title}")

    return f"""
    <section class="contribution-panel" aria-label="Contribution and Community Verification">
      <div class="contribution-header">
        <div class="contribution-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
        </div>
        <div>
          <h3>Community Verification & Improvement Panel</h3>
          <p>This documentation is maintained in the authoritative source repository (Repo A). See an error, tested this procedure on physical hardware, or have verified serial logs?</p>
        </div>
      </div>
      <div class="contribution-actions">
        <a href="https://github.com/Rny0007/mt7986-openwrt-router-guide/blob/main/{source_path}" target="_blank" rel="noopener" class="btn btn-sm btn-outline">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/></svg>
          Edit this page on GitHub
        </a>
        <a href="https://github.com/Rny0007/mt7986-openwrt-router-guide/issues/new?template=08_documentation_improvement.yml&page_url={enc_path}&title={enc_title}&labels=documentation,enhancement" target="_blank" rel="noopener" class="btn btn-sm btn-outline">
          Report an Error or Typo
        </a>
        <a href="https://github.com/Rny0007/mt7986-openwrt-router-guide/issues/new?template=05_recovery_unbrick_report.yml&title={enc_unbrick_title}&labels=recovery-guide,unbrick-verified" target="_blank" rel="noopener" class="btn btn-sm btn-outline">
          Submit Unbrick Tutorial
        </a>
        <a href="https://github.com/Rny0007/mt7986-openwrt-router-guide/issues/new?template=02_hardware_revision_verification.yml&title={enc_verify_title}&labels=hardware-verified,testing-report" target="_blank" rel="noopener" class="btn btn-sm btn-outline">
          Verified on My Device
        </a>
        <a href="{rel_root}/contributing/index.html" class="btn btn-sm btn-primary">
          Contribution Guidelines
        </a>
      </div>
    </section>
    """

def build_css():
    css_content = """/* OpenWrt Hardware Knowledge Base — Premium Design System (Figma & NOC Inspired) */
:root {
  --bg: #0b0f19;
  --bg-secondary: #111827;
  --bg-card: #162032;
  --bg-card-hover: #1e293b;
  --border: #243046;
  --border-focus: #38bdf8;
  --text: #e2e8f0;
  --text-muted: #94a3b8;
  --text-heading: #ffffff;
  --primary: #06b6d4;
  --primary-hover: #0891b2;
  --accent: #8b5cf6;
  --success: #10b981;
  --success-bg: rgba(16, 185, 129, 0.15);
  --warning: #f59e0b;
  --warning-bg: rgba(245, 158, 11, 0.15);
  --danger: #ef4444;
  --danger-bg: rgba(239, 68, 68, 0.15);
  --info: #3b82f6;
  --info-bg: rgba(59, 130, 246, 0.15);
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.4);
  --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.5), 0 2px 4px -2px rgba(0,0,0,0.4);
  --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.6), 0 4px 6px -4px rgba(0,0,0,0.5);
  --transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

[data-theme="light"] {
  --bg: #f8fafc;
  --bg-secondary: #f1f5f9;
  --bg-card: #ffffff;
  --bg-card-hover: #f8fafc;
  --border: #e2e8f0;
  --border-focus: #0284c7;
  --text: #334155;
  --text-muted: #64748b;
  --text-heading: #0f172a;
  --primary: #0284c7;
  --primary-hover: #0369a1;
  --accent: #7c3aed;
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.08);
  --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background-color: var(--bg);
  color: var(--text);
  font-family: var(--font-sans);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

a { color: var(--primary); text-decoration: none; transition: var(--transition); }
a:hover { color: var(--primary-hover); text-decoration: underline; }

/* Header */
.site-header {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(11, 15, 25, 0.85);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
}
[data-theme="light"] .site-header {
  background: rgba(248, 250, 252, 0.9);
}
.header-inner {
  max-width: 1300px;
  margin: 0 auto;
  padding: 0.75rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}
.brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.15rem;
  color: var(--text-heading);
  text-decoration: none;
}
.brand strong { color: var(--primary); }
.logo-icon { width: 32px; height: 32px; }

.nav-links {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}
.nav-links a {
  color: var(--text-muted);
  font-size: 0.88rem;
  font-weight: 500;
  padding: 0.4rem 0.75rem;
  border-radius: var(--radius-sm);
  text-decoration: none;
}
.nav-links a:hover, .nav-links a.active {
  color: var(--text-heading);
  background: var(--bg-card);
  border: 1px solid var(--border);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.btn-icon {
  background: var(--bg-card);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 0.45rem;
  border-radius: var(--radius-sm);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
.btn-icon svg { width: 18px; height: 18px; }
[data-theme="dark"] .sun-icon { display: block; }
[data-theme="dark"] .moon-icon { display: none; }
[data-theme="light"] .sun-icon { display: none; }
[data-theme="light"] .moon-icon { display: block; }

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  padding: 0.6rem 1.2rem;
  border-radius: var(--radius-sm);
  font-size: 0.9rem;
  cursor: pointer;
  border: none;
  transition: var(--transition);
  text-decoration: none;
}
.btn:hover { text-decoration: none; }
.btn-primary {
  background: linear-gradient(135deg, var(--primary), #0284c7);
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(6, 182, 212, 0.35);
}
.btn-primary:hover {
  filter: brightness(1.1);
  transform: translateY(-1px);
}
.btn-outline {
  background: var(--bg-card);
  border: 1px solid var(--border);
  color: var(--text);
}
.btn-outline:hover {
  border-color: var(--primary);
  color: var(--text-heading);
}
.btn-sm { padding: 0.35rem 0.75rem; font-size: 0.82rem; }

/* Main Layout */
.main-content {
  max-width: 1300px;
  margin: 0 auto;
  padding: 2.5rem 1.5rem 5rem;
}

/* NOC Documentation Layout */
.docs-layout {
  display: grid;
  grid-template-columns: 260px minmax(0, 1fr);
  gap: 2.5rem;
  align-items: start;
}
.docs-sidebar {
  position: sticky;
  top: 5rem;
  max-height: calc(100vh - 6rem);
  overflow-y: auto;
  padding: 1.25rem;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  font-size: 0.85rem;
}
.docs-sidebar h4 {
  color: var(--text-heading);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-size: 0.78rem;
  margin-bottom: 0.8rem;
}
.docs-sidebar ul {
  list-style: none;
}
.docs-sidebar li {
  margin-bottom: 0.5rem;
}
.docs-sidebar a {
  color: var(--text-muted);
  display: block;
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-sm);
}
.docs-sidebar a:hover, .docs-sidebar a.active-toc {
  color: var(--primary);
  background: var(--bg-secondary);
  text-decoration: none;
}
.docs-content {
  min-width: 0;
}

/* Callouts */
.callout {
  padding: 1.25rem;
  border-radius: var(--radius-sm);
  margin: 1.5rem 0;
  border-left: 4px solid var(--primary);
  background: var(--bg-secondary);
  font-size: 0.92rem;
  line-height: 1.6;
}
.callout-note {
  border-left-color: var(--info);
  background: var(--info-bg);
}
.callout-warning {
  border-left-color: var(--warning);
  background: var(--warning-bg);
}
.callout-danger {
  border-left-color: var(--danger);
  background: var(--danger-bg);
}
.callout strong {
  display: block;
  margin-bottom: 0.35rem;
  color: var(--text-heading);
}

/* Code Blocks with Copy */
.code-block-wrapper {
  position: relative;
  margin: 1.25rem 0;
}
.copy-btn {
  position: absolute;
  top: 0.6rem;
  right: 0.6rem;
  background: #1e293b;
  border: 1px solid var(--border);
  color: var(--text-muted);
  font-size: 0.75rem;
  padding: 0.25rem 0.55rem;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: var(--transition);
}
.copy-btn:hover {
  color: var(--text-heading);
  border-color: var(--primary);
}

/* Hero */
.hero {
  padding: 3rem 0 4rem;
  text-align: center;
  max-width: 900px;
  margin: 0 auto;
}
.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.35rem 0.9rem;
  background: rgba(6, 182, 212, 0.12);
  border: 1px solid rgba(6, 182, 212, 0.3);
  color: var(--primary);
  border-radius: 9999px;
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
}
.hero h1 {
  font-size: 2.85rem;
  line-height: 1.15;
  color: var(--text-heading);
  font-weight: 800;
  letter-spacing: -0.025em;
  margin-bottom: 1.25rem;
}
.hero p.lead {
  font-size: 1.15rem;
  color: var(--text-muted);
  line-height: 1.6;
  margin-bottom: 2rem;
}
.hero-cta {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 3rem;
}

/* Stats Counter */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.25rem;
  margin-bottom: 4rem;
}
.stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  padding: 1.5rem;
  border-radius: var(--radius-md);
  text-align: center;
  box-shadow: var(--shadow-sm);
}
.stat-val {
  font-size: 2.4rem;
  font-weight: 800;
  color: var(--primary);
  line-height: 1;
  margin-bottom: 0.5rem;
}
.stat-label {
  font-size: 0.85rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}

/* Cards & Grids */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 1.75rem;
  flex-wrap: wrap;
  gap: 1rem;
}
.section-header h1, .section-header h2 {
  font-size: 1.65rem;
  color: var(--text-heading);
  letter-spacing: -0.02em;
}
.section-header p {
  color: var(--text-muted);
  font-size: 0.95rem;
  margin-top: 0.25rem;
}

.grid-3 {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3.5rem;
}

.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 1.5rem;
  transition: var(--transition);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.card:hover {
  border-color: var(--primary);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  gap: 0.5rem;
}
.card-title {
  font-size: 1.15rem;
  color: var(--text-heading);
  font-weight: 700;
}
.card-meta {
  color: var(--text-muted);
  font-size: 0.85rem;
  margin-bottom: 1rem;
}
.card-body {
  font-size: 0.9rem;
  color: var(--text);
  margin-bottom: 1.25rem;
}

/* Badges */
.badge {
  display: inline-flex;
  align-items: center;
  padding: 0.2rem 0.55rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.badge-success { background: var(--success-bg); color: var(--success); border: 1px solid rgba(16, 185, 129, 0.3); }
.badge-warning { background: var(--warning-bg); color: var(--warning); border: 1px solid rgba(245, 158, 11, 0.3); }
.badge-danger { background: var(--danger-bg); color: var(--danger); border: 1px solid rgba(239, 68, 68, 0.3); }
.badge-info { background: var(--info-bg); color: var(--info); border: 1px solid rgba(59, 130, 246, 0.3); }
.badge-secondary { background: rgba(139, 92, 246, 0.15); color: #a78bfa; border: 1px solid rgba(139, 92, 246, 0.3); }
.badge-muted { background: rgba(148, 163, 184, 0.15); color: #94a3b8; border: 1px solid rgba(148, 163, 184, 0.3); }

/* Specs Table */
.table-container {
  overflow-x: auto;
  margin: 1.25rem 0;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
}
.spec-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.88rem;
}
.spec-table th, .spec-table td {
  padding: 0.7rem 0.85rem;
  text-align: left;
  border-bottom: 1px solid var(--border);
}
.spec-table th {
  color: var(--text-muted);
  font-weight: 600;
  background: var(--bg-secondary);
  white-space: nowrap;
}

/* Breadcrumbs */
.breadcrumbs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-bottom: 1.25rem;
}
.breadcrumbs a { color: var(--text-muted); }
.breadcrumbs a:hover { color: var(--primary); }
.breadcrumbs span { color: var(--border); }

/* Guide Pagination */
.guide-pagination {
  display: flex;
  justify-content: space-between;
  gap: 1.5rem;
  margin: 3rem 0;
  flex-wrap: wrap;
}
.guide-nav-link {
  flex: 1;
  min-width: 250px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  padding: 1.25rem;
  border-radius: var(--radius-md);
  text-decoration: none;
  transition: var(--transition);
}
.guide-nav-link:hover {
  border-color: var(--primary);
  transform: translateY(-2px);
  text-decoration: none;
}
.guide-nav-link span {
  font-size: 0.78rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  display: block;
  margin-bottom: 0.25rem;
}
.guide-nav-link strong {
  font-size: 1.05rem;
  color: var(--text-heading);
}

/* Contribution Panel */
.contribution-panel {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 1.75rem;
  margin-top: 3.5rem;
}
.contribution-header {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  margin-bottom: 1.25rem;
}
.contribution-icon {
  background: rgba(6, 182, 212, 0.15);
  color: var(--primary);
  padding: 0.6rem;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
}
.contribution-header h3 {
  color: var(--text-heading);
  font-size: 1.15rem;
  margin-bottom: 0.25rem;
}
.contribution-header p {
  color: var(--text-muted);
  font-size: 0.88rem;
  line-height: 1.5;
}
.contribution-actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

/* Visitor Telemetry Badge */
.visitor-telemetry {
  display: inline-block;
}
.telemetry-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border);
  padding: 0.3rem 0.65rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  color: var(--text-muted);
}
.telemetry-badge strong {
  color: var(--success);
}

/* Code Snippets */
pre, code {
  font-family: var(--font-mono);
  font-size: 0.88rem;
}
pre {
  background: #090d16;
  border: 1px solid var(--border);
  padding: 1.25rem;
  border-radius: var(--radius-md);
  overflow-x: auto;
  margin: 1rem 0;
  color: #38bdf8;
}

/* Footer */
.site-footer {
  background: var(--bg-secondary);
  border-top: 1px solid var(--border);
  padding: 3.5rem 1.5rem 2rem;
  font-size: 0.88rem;
}
.footer-inner {
  max-width: 1300px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 2.5rem;
  margin-bottom: 2.5rem;
}
.footer-col h3, .footer-col h4 {
  color: var(--text-heading);
  margin-bottom: 1rem;
}
.footer-col p { color: var(--text-muted); margin-bottom: 0.75rem; line-height: 1.6; }
.footer-col ul { list-style: none; }
.footer-col li { margin-bottom: 0.5rem; }
.footer-col a { color: var(--text-muted); }
.footer-col a:hover { color: var(--primary); }
.footer-bottom {
  max-width: 1300px;
  margin: 0 auto;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border);
  text-align: center;
  color: var(--text-muted);
  font-size: 0.8rem;
}

/* Responsive */
@media (max-width: 900px) {
  .footer-inner { grid-template-columns: 1fr; }
  .nav-links { display: none; }
  .hero h1 { font-size: 2.2rem; }
  .docs-layout { grid-template-columns: 1fr; }
  .docs-sidebar { display: none; }
}

@media (prefers-reduced-motion: reduce) {
  * { transition: none !important; animation: none !important; }
}
"""
    return css_content

def build_js():
    js_content = """/* OpenWrt Hardware Knowledge Base — Zero Dependency Frontend Logic */
document.addEventListener('DOMContentLoaded', () => {
  // Theme Toggle with LocalStorage
  const themeToggle = document.getElementById('theme-toggle');
  const currentTheme = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
  document.documentElement.setAttribute('data-theme', currentTheme);

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const theme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', theme);
      localStorage.setItem('theme', theme);
    });
  }

  // Interactive Live Filter for Directory & Explorer
  const searchInput = document.getElementById('search-input');
  const cards = document.querySelectorAll('.filter-card');
  if (searchInput && cards.length > 0) {
    searchInput.addEventListener('input', (e) => {
      const query = e.target.value.toLowerCase().trim();
      cards.forEach(card => {
        const text = card.textContent.toLowerCase();
        if (text.includes(query)) {
          card.style.display = '';
        } else {
          card.style.display = 'none';
        }
      });
    });
  }

  // Code Copy Buttons
  document.querySelectorAll('pre').forEach((pre) => {
    const wrapper = document.createElement('div');
    wrapper.className = 'code-block-wrapper';
    pre.parentNode.insertBefore(wrapper, pre);
    wrapper.appendChild(pre);

    const btn = document.createElement('button');
    btn.className = 'copy-btn';
    btn.textContent = 'Copy';
    btn.setAttribute('aria-label', 'Copy code snippet to clipboard');
    wrapper.appendChild(btn);

    btn.addEventListener('click', async () => {
      const code = pre.querySelector('code') ? pre.querySelector('code').innerText : pre.innerText;
      try {
        await navigator.clipboard.writeText(code);
        btn.textContent = 'Copied!';
        setTimeout(() => { btn.textContent = 'Copy'; }, 2000);
      } catch (err) {
        btn.textContent = 'Failed';
        setTimeout(() => { btn.textContent = 'Copy'; }, 2000);
      }
    });
  });

  // Table of Contents Active Spy
  const tocLinks = document.querySelectorAll('.docs-sidebar a');
  const sections = [];
  tocLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href && href.startsWith('#')) {
      const target = document.querySelector(href);
      if (target) sections.push({ link, target });
    }
  });

  if (sections.length > 0) {
    window.addEventListener('scroll', () => {
      let current = '';
      sections.forEach(s => {
        const top = s.target.getBoundingClientRect().top;
        if (top <= 120) current = s.link.getAttribute('href');
      });
      tocLinks.forEach(l => {
        if (l.getAttribute('href') === current) {
          l.classList.add('active-toc');
        } else {
          l.classList.remove('active-toc');
        }
      });
    }, { passive: true });
  }
});
"""
    return js_content

def build_favicon():
    return """<svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="32" height="32" rx="8" fill="#0f172a"/>
  <path d="M6 16C6 10.4772 10.4772 6 16 6C21.5228 6 26 10.4772 26 16" stroke="#06b6d4" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M10 16C10 12.6863 12.6863 10 16 10C19.3137 10 22 12.6863 22 16" stroke="#10b981" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="16" cy="16" r="2.5" fill="#f8fafc"/>
  <rect x="8" y="21" width="16" height="5" rx="2" fill="#334155"/>
  <circle cx="12" cy="23.5" r="1" fill="#10b981"/>
  <circle cx="16" cy="23.5" r="1" fill="#06b6d4"/>
  <circle cx="20" cy="23.5" r="1" fill="#f59e0b"/>
</svg>"""

def build_robots():
    return f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}/sitemap.xml
"""

def build_manifest():
    return json.dumps({
        "name": "OpenWrt Router Hardware Knowledge Base",
        "short_name": "OpenWrtKB",
        "start_url": "./index.html",
        "display": "standalone",
        "background_color": "#0b0f19",
        "theme_color": "#06b6d4",
        "description": "Evidence-based hardware database, interactive diagrams, and technical recovery guides for OpenWrt compatible routers.",
        "icons": [
            {
                "src": "assets/favicon.svg",
                "sizes": "any",
                "type": "image/svg+xml"
            }
        ]
    }, indent=2)

def get_badge_class(status):
    mapping = {
        "OFFICIALLY_SUPPORTED": "badge-success",
        "COMMUNITY_VERIFIED": "badge-warning",
        "PARTIALLY_VERIFIED": "badge-info",
        "POTENTIALLY_COMPATIBLE": "badge-secondary",
        "EXPERIMENTAL": "badge-warning",
        "UNSUPPORTED": "badge-danger",
        "UNKNOWN": "badge-muted"
    }
    return mapping.get(status, "badge-info")

def generate_homepage(devices, chipsets):
    official_count = sum(1 for d in devices if d.get("openwrt", {}).get("support_status") == "OFFICIALLY_SUPPORTED")
    manufacturers = len(set(d.get("manufacturer") for d in devices if d.get("manufacturer")))
    featured_devices = devices[:6]
    featured_chipsets = chipsets[:6]

    device_cards = ""
    for d in featured_devices:
        dev_id = d["id"]
        status = d.get("openwrt", {}).get("support_status", "UNKNOWN")
        badge_cls = get_badge_class(status)
        soc = f"{d.get('soc', {}).get('vendor', '')} {d.get('soc', {}).get('model', '')}"
        ram = d.get("ram_mb", "N/A")
        flash_cap = d.get('flash', {}).get('capacity_mb') or d.get('flash', {}).get('mb') or 'N/A'
        flash = f"{flash_cap} MB {d.get('flash', {}).get('type', '')}"

        device_cards += f"""
        <div class="card filter-card">
          <div>
            <div class="card-header">
              <span class="card-title">{d.get('manufacturer')} {d.get('model')}</span>
              <span class="badge {badge_cls}">{status.replace('_', ' ')}</span>
            </div>
            <div class="card-meta">SoC: <strong>{soc}</strong> | Arch: {d.get('architecture')}</div>
            <p class="card-body">RAM: {ram} MB | Flash: {flash} | Target: <code>{d.get('openwrt', {}).get('target', 'N/A')}</code></p>
          </div>
          <a href="devices/{dev_id}/index.html" class="btn btn-sm btn-outline">View Hardware Profile &rarr;</a>
        </div>
        """

    chipset_cards = ""
    for c in featured_chipsets:
        cid = c["id"]
        tier = c.get("openwrt_support_tier", "Tier 2")
        badge_cls = "badge-success" if "Tier 1" in tier else "badge-info"
        chipset_cards += f"""
        <div class="card filter-card">
          <div>
            <div class="card-header">
              <span class="card-title">{c.get('vendor')} {c.get('part_number')}</span>
              <span class="badge {badge_cls}">{tier}</span>
            </div>
            <div class="card-meta">{c.get('marketing_name')} | {c.get('cpu', {}).get('core_type')}</div>
            <p class="card-body">Cores: {c.get('cpu', {}).get('cores')}x @ {c.get('cpu', {}).get('max_clock_mhz')} MHz | Target: <code>{c.get('openwrt_target')}</code></p>
          </div>
          <a href="chipsets/{cid}/index.html" class="btn btn-sm btn-outline">Explore Silicon Architecture &rarr;</a>
        </div>
        """

    content = f"""
    <section class="hero">
      <div class="hero-badge">Evidence-Based OpenWrt Knowledge Base v2.0</div>
      <h1>Global Open-Source Router Hardware Intelligence</h1>
      <p class="lead">Discover, verify, and compare OpenWrt-compatible routers, switches, and embedded network platforms. Powered by verified upstream device trees, FCC teardowns, and primary research.</p>
      <div class="hero-cta">
        <a href="explorer/index.html" class="btn btn-primary">⚡ Launch Interactive Explorer</a>
        <a href="diagrams/index.html" class="btn btn-outline">📊 View Architecture Diagrams</a>
        <a href="devices/index.html" class="btn btn-outline">📁 Device Directory ({len(devices)})</a>
      </div>
    </section>

    <section class="stats-grid">
      <div class="stat-card">
        <div class="stat-val">{len(devices)}</div>
        <div class="stat-label">Verified Devices</div>
      </div>
      <div class="stat-card">
        <div class="stat-val">{len(chipsets)}</div>
        <div class="stat-label">Silicon Platforms</div>
      </div>
      <div class="stat-card">
        <div class="stat-val">{official_count}</div>
        <div class="stat-label">Officially Supported</div>
      </div>
      <div class="stat-card">
        <div class="stat-val">{manufacturers}</div>
        <div class="stat-label">Global Manufacturers</div>
      </div>
    </section>

    <div class="section-header">
      <div>
        <h2>Featured Router & Hardware Platforms</h2>
        <p>Explore production and enterprise router platforms verified on OpenWrt mainline.</p>
      </div>
      <a href="devices/index.html" class="btn btn-sm btn-outline">Browse All {len(devices)} Devices &rarr;</a>
    </div>
    <div class="grid-3">
      {device_cards}
    </div>

    <div class="section-header">
      <div>
        <h2>Core Networking Silicon Architectures</h2>
        <p>MediaTek Filogic, Qualcomm IPQ, Rockchip, Realtek DSA, Broadcom, and x86_64.</p>
      </div>
      <a href="chipsets/index.html" class="btn btn-sm btn-outline">Browse All {len(chipsets)} Chipsets &rarr;</a>
    </div>
    <div class="grid-3">
      {chipset_cards}
    </div>

    <section style="background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 2.5rem; margin-top: 3rem;">
      <h2 style="color: var(--text-heading); margin-bottom: 1rem;">Architectural Reference & Community Deployments</h2>
      <p style="color: var(--text-muted); margin-bottom: 1.5rem; max-width: 800px;">
        This knowledge base includes verified field-tested reference architectures, including the <strong>Arcadyan / Jio JIDU6101</strong> (MediaTek MT7986A Filogic 830) two-stage installation, sysfs LED controls, and dual-WAN automatic failover automation blueprints.
      </p>
      <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
        <a href="guides/installation/index.html" class="btn btn-primary">Two-Stage Installation Guide</a>
        <a href="guides/recovery/index.html" class="btn btn-outline">TFTP & UART Recovery Guide</a>
        <a href="guides/multi-wan/index.html" class="btn btn-outline">Multi-WAN Failover Blueprint</a>
      </div>
    </section>
    """
    desc = "Global OpenWrt hardware knowledge base. Explore, compare, and verify OpenWrt-compatible routers, switches, and SoCs across global vendors."
    return get_header("Global Hardware Intelligence", current_nav="home", description=desc, canonical_path="") + content + get_footer()

def generate_device_directory(devices):
    rows = ""
    for d in devices:
        dev_id = d["id"]
        status = d.get("openwrt", {}).get("support_status", "UNKNOWN")
        badge_cls = get_badge_class(status)
        soc = f"{d.get('soc', {}).get('vendor', '')} {d.get('soc', {}).get('model', '')}"
        ports = len(d.get("ethernet_ports") or d.get("ethernet", {}).get("ports") or [])
        flash_cap = d.get('flash', {}).get('capacity_mb') or d.get('flash', {}).get('mb') or 'N/A'
        flash = f"{flash_cap} MB {d.get('flash', {}).get('type', '')}"

        rows += f"""
        <tr class="filter-card">
          <td><strong><a href="{dev_id}/index.html">{d.get('manufacturer')} {d.get('model')}</a></strong></td>
          <td>{soc}</td>
          <td>{d.get('ram_mb', 'N/A')} MB</td>
          <td>{flash}</td>
          <td>{ports} Ports</td>
          <td><code>{d.get('openwrt', {}).get('target', 'N/A')}</code></td>
          <td><span class="badge {badge_cls}">{status.replace('_', ' ')}</span></td>
          <td><a href="{dev_id}/index.html" class="btn btn-sm btn-outline">Profile</a></td>
        </tr>
        """

    content = f"""
    <div class="section-header">
      <div>
        <h1>OpenWrt Supported Devices Directory</h1>
        <p>Comprehensive catalog of {len(devices)} verified router, access point, switch, and SBC platforms.</p>
      </div>
      <div>
        <input type="text" id="search-input" placeholder="Search devices by name, SoC, target..." style="padding: 0.5rem 1rem; border-radius: var(--radius-sm); border: 1px solid var(--border); background: var(--bg-card); color: var(--text); min-width: 280px;">
      </div>
    </div>

    <div class="table-container">
      <table class="spec-table">
        <thead>
          <tr>
            <th>Device Model</th>
            <th>SoC / Platform</th>
            <th>RAM</th>
            <th>Flash Storage</th>
            <th>Ethernet</th>
            <th>OpenWrt Target</th>
            <th>Support Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
    </div>
    """
    desc = f"Complete catalog of {len(devices)} OpenWrt-compatible routers, switches, and access points with verified hardware specifications and targets."
    return get_header("Device Directory", rel_root="..", current_nav="devices", description=desc, canonical_path="devices/") + content + get_footer(rel_root="..")

def generate_device_page(d):
    dev_id = d["id"]
    status = d.get("openwrt", {}).get("support_status", "UNKNOWN")
    badge_cls = get_badge_class(status)
    soc = d.get("soc", {})
    flash = d.get("flash", {})
    openwrt = d.get("openwrt", {})
    ports = d.get("ethernet_ports") or d.get("ethernet", {}).get("ports") or []
    wireless = d.get("wifi") or d.get("wireless") or []
    sources = d.get("sources", [])

    ports_li = []
    for p in ports:
        pname = p.get('label') or p.get('name') or p.get('port_id') or 'Port'
        ptype = p.get('connector') or p.get('type') or 'Ethernet'
        speed = p.get('speed_mbps', 'N/A')
        dsa = p.get('dsa_port') or p.get('port_id') or 'eth0'
        poe = f" ({p['poe']})" if p.get('poe') else ""
        ports_li.append(f"<li><strong>{pname}</strong> ({ptype}{poe}): {speed} Mbps — Interface <code>{dsa}</code></li>")
    ports_html = "".join(ports_li) or "<li>No physical Ethernet ports documented.</li>"

    wireless_li = []
    for w in wireless:
        gen = w.get('generation') or w.get('standard') or 'Wi-Fi'
        band = w.get('band') or (f"{w.get('frequency_ghz')} GHz" if w.get('frequency_ghz') else "Wi-Fi")
        chip = w.get('chipset') or 'Integrated'
        streams = w.get('mimo') or w.get('spatial_streams') or 'N/A'
        rate = f", Max Rate: {w['max_phy_rate_mbps']} Mbps" if w.get('max_phy_rate_mbps') else ""
        wireless_li.append(f"<li><strong>{gen} ({band})</strong>: Chipset <code>{chip}</code>, MIMO/Streams: {streams}{rate}</li>")
    wireless_html = "".join(wireless_li)

    limitations_html = "".join([f"<li>{lim}</li>" for lim in openwrt.get("known_limitations", [])]) or "<li>No critical hardware limitations reported.</li>"
    sources_html = "".join([f"<li><a href='{s.get('url')}' target='_blank' rel='noopener'>{s.get('title')}</a> ({s.get('type')})</li>" for s in sources])

    flash_cap = flash.get('capacity_mb') or flash.get('mb') or 'N/A'
    switch_model = d.get('switch', {}).get('model') or d.get('ethernet', {}).get('switch_chip') or 'Integrated SoC MAC / DSA'
    serial_uart = d.get('serial_uart', {}) or d.get('recovery', {})

    canonical_url = f"{BASE_URL}/devices/{dev_id}/"

    json_ld = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": f"{d.get('manufacturer')} {d.get('model')} OpenWrt Hardware Specifications & Installation",
        "description": f"Verified OpenWrt support status, hardware specs, flash layout, and recovery for {d.get('manufacturer')} {d.get('model')}.",
        "author": { "@type": "Person", "name": "Rny0007" },
        "url": canonical_url
    }

    content = f"""
    <div class="breadcrumbs">
      <a href="../../index.html">Home</a> <span>/</span>
      <a href="../index.html">Devices</a> <span>/</span>
      <strong>{d.get('manufacturer')} {d.get('model')}</strong>
    </div>

    <div class="section-header">
      <div>
        <h1 style="font-size: 2.2rem; color: var(--text-heading);">{d.get('manufacturer')} {d.get('model')}</h1>
        <p style="color: var(--text-muted);">Hardware Revision: <code>{d.get('hardware_revision', 'v1')}</code> | Internal Board ID: <code>{d.get('internal_board_name', 'N/A')}</code></p>
      </div>
      <div>
        <span class="badge {badge_cls}" style="font-size: 0.9rem; padding: 0.4rem 0.8rem;">{status.replace('_', ' ')}</span>
      </div>
    </div>

    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 2rem; margin-top: 2rem;">
      <div>
        <div class="card" style="margin-bottom: 2rem;">
          <h2 style="color: var(--text-heading); font-size: 1.25rem; margin-bottom: 1rem;">Core Silicon & Processing Specifications</h2>
          <table class="spec-table">
            <tr><th>SoC Vendor & Model</th><td>{soc.get('vendor')} {soc.get('model')} ({soc.get('family', 'Embedded')})</td></tr>
            <tr><th>CPU Architecture</th><td>{d.get('architecture')} ({soc.get('cores', 'N/A')} Cores @ {soc.get('frequency_mhz', 'N/A')} MHz)</td></tr>
            <tr><th>RAM Memory</th><td>{d.get('ram_mb', 'N/A')} MB</td></tr>
            <tr><th>Flash Memory</th><td>{flash_cap} MB ({flash.get('type', 'N/A')})</td></tr>
            <tr><th>Switch ASIC</th><td>{switch_model}</td></tr>
          </table>
        </div>

        <div class="card" style="margin-bottom: 2rem;">
          <h2 style="color: var(--text-heading); font-size: 1.25rem; margin-bottom: 1rem;">Networking & Wireless Subsystem</h2>
          <h3 style="font-size: 1rem; color: var(--text-heading); margin-top: 0.5rem;">Physical Ethernet Ports</h3>
          <ul style="margin: 0.5rem 0 1rem 1.5rem; font-size: 0.9rem; color: var(--text);">
            {ports_html}
          </ul>
          <h3 style="font-size: 1rem; color: var(--text-heading); margin-top: 1rem;">Wireless Radios</h3>
          <ul style="margin: 0.5rem 0 1rem 1.5rem; font-size: 0.9rem; color: var(--text);">
            {wireless_html or '<li>No internal wireless radios (Dedicated Wired Device / Switch / SBC)</li>'}
          </ul>
        </div>

        <div class="card">
          <h2 style="color: var(--text-heading); font-size: 1.25rem; margin-bottom: 1rem;">Known Limitations & Operational Notes</h2>
          <ul style="margin: 0.5rem 0 1rem 1.5rem; font-size: 0.9rem; color: var(--text);">
            {limitations_html}
          </ul>
        </div>
      </div>

      <div>
        <div class="card" style="margin-bottom: 2rem;">
          <h2 style="color: var(--text-heading); font-size: 1.25rem; margin-bottom: 1rem;">OpenWrt Target Integration</h2>
          <table class="spec-table">
            <tr><th>Target</th><td><code>{openwrt.get('target', 'N/A')}</code></td></tr>
            <tr><th>Subtarget</th><td><code>{openwrt.get('subtarget', 'generic')}</code></td></tr>
            <tr><th>Device Profile</th><td><code>{openwrt.get('profile', 'generic')}</code></td></tr>
            <tr><th>First Supported</th><td>{openwrt.get('first_supported_version', 'N/A')}</td></tr>
            <tr><th>Device Tree File</th><td><code>{openwrt.get('device_tree_file', 'N/A')}</code></td></tr>
          </table>
          <div style="margin-top: 1.25rem; display: flex; flex-direction: column; gap: 0.5rem;">
            <a href="{openwrt.get('firmware_selector_url') or 'https://firmware-selector.openwrt.org'}" target="_blank" rel="noopener" class="btn btn-sm btn-primary" style="justify-content: center;">Download Official Firmware &rarr;</a>
            <a href="../../guides/install/{dev_id}/index.html" class="btn btn-sm btn-outline" style="justify-content: center;">View Installation Guide &rarr;</a>
            <a href="../../guides/recovery/{dev_id}/index.html" class="btn btn-sm btn-outline" style="justify-content: center;">View Recovery Guide &rarr;</a>
          </div>
        </div>

        <div class="card" style="margin-bottom: 2rem;">
          <h2 style="color: var(--text-heading); font-size: 1.25rem; margin-bottom: 1rem;">Installation & Recovery</h2>
          <p style="font-size: 0.9rem; margin-bottom: 0.5rem;"><strong>Flashing Method:</strong> {d.get('installation', {}).get('method', 'Standard')}</p>
          <p style="font-size: 0.9rem; margin-bottom: 0.5rem;"><strong>Installation Risk:</strong> <span class="badge { 'badge-danger' if d.get('installation', {}).get('risk') == 'HIGH' else ('badge-warning' if d.get('installation', {}).get('risk') == 'MEDIUM' else 'badge-success') }">{d.get('installation', {}).get('risk', 'MEDIUM')}</span></p>
          <p style="font-size: 0.9rem; margin-bottom: 0.5rem;"><strong>Serial UART:</strong> { 'Available (3.3V TTL)' if serial_uart.get('available') else 'Not populated' }</p>
          <p style="font-size: 0.9rem;"><strong>Recovery Method:</strong> {d.get('recovery', {}).get('method', 'TFTP Push')}</p>
        </div>

        <div class="card">
          <h2 style="color: var(--text-heading); font-size: 1.25rem; margin-bottom: 1rem;">Primary Evidence & Sources</h2>
          <ul style="margin: 0.5rem 0 0 1.5rem; font-size: 0.85rem; color: var(--text-muted);">
            {sources_html}
          </ul>
        </div>
      </div>
    </div>

    {get_contribution_panel(f"data/devices/{d.get('id').split('-')[0]}/{dev_id}.json", f"{d.get('manufacturer')} {d.get('model')}", rel_root="../..")}
    """
    desc = f"Verified OpenWrt hardware profile for {d.get('manufacturer')} {d.get('model')}. CPU, RAM, flash layout, Ethernet, Wi-Fi, and flashing instructions."
    return get_header(f"{d.get('manufacturer')} {d.get('model')}", rel_root="../..", current_nav="devices", description=desc, canonical_path=f"devices/{dev_id}/", json_ld=json_ld) + content + get_footer(rel_root="../..")

def generate_device_install_guide(d):
    dev_id = d["id"]
    status = d.get("openwrt", {}).get("support_status", "UNKNOWN")
    badge_cls = get_badge_class(status)
    soc = d.get("soc", {})
    flash = d.get("flash", {})
    openwrt = d.get("openwrt", {})
    inst = d.get("installation", {})
    method = inst.get("method", "OEM Web Interface / Firmware Upload")
    risk = inst.get("risk", "MEDIUM")
    risk_badge = "badge-danger" if risk == "HIGH" else ("badge-warning" if risk == "MEDIUM" else "badge-success")
    
    flash_cap = flash.get('capacity_mb') or flash.get('mb') or 'N/A'
    fw_url = openwrt.get("firmware_selector_url") or "https://firmware-selector.openwrt.org"

    if "Direct Image Flash" in method:
        method_steps = f"""
        <ol style="margin-left: 1.5rem; line-height: 1.8;">
          <li><strong>Download Official Image:</strong> Obtain the official OpenWrt raw disk image (<code>openwrt-{openwrt.get('target', 'target')}-{openwrt.get('subtarget', 'generic')}-{dev_id}-ext4-factory.img.gz</code>) from <a href="{fw_url}" target="_blank" rel="noopener">OpenWrt Firmware Selector</a>.</li>
          <li><strong>Decompress Image:</strong> Gunzip the downloaded file: <code>gunzip openwrt-*.img.gz</code>.</li>
          <li><strong>Flash to Storage Media:</strong> Use BalenaEtcher, Raspberry Pi Imager, or <code>dd</code> to write the image directly to your microSD card, eMMC module, or NVMe drive:
            <pre><code># Linux/macOS write command (verify correct drive target!)
sudo dd if=openwrt-*.img of=/dev/sdX bs=4M status=progress conv=fsync</code></pre>
          </li>
          <li><strong>Insert Media and Boot:</strong> Insert the microSD card into the device, connect an Ethernet cable between LAN port and your PC, and connect power.</li>
          <li><strong>Access First Boot:</strong> Wait 45-60 seconds for partition expansion and initial service startup. Open browser to <code>http://192.168.1.1</code>.</li>
        </ol>
        """
    elif "Two-Stage" in method:
        method_steps = f"""
        <ol style="margin-left: 1.5rem; line-height: 1.8;">
          <li><strong>Pre-installation Flash Backup:</strong> SSH into the OEM firmware shell and dump factory calibration partitions (<code>Factory</code>, <code>MFG</code>) via <code>dd</code> to preserve RF calibration.</li>
          <li><strong>Stage 1 (Ramdisk Boot):</strong> Transfer <code>openwrt-{openwrt.get('target', 'target')}-initramfs-factory.ubi</code> to <code>/tmp</code> and write to secondary boot partition. Configure temporary U-Boot bootargs:
            <pre><code>ubiformat /dev/mtd6 -y -f /tmp/openwrt-factory.ubi
fw_setenv bootcmd "ubi detach; ubi part ubi2; ubi read 46000000 kernel; bootm 0x46000000"
sync && reboot</code></pre>
          </li>
          <li><strong>Stage 2 (Permanent Sysupgrade):</strong> Upon boot into OpenWrt RAM at <code>192.168.1.1</code>, upload the permanent sysupgrade image and flash permanently:
            <pre><code>sysupgrade -n /tmp/openwrt-sysupgrade.bin</code></pre>
          </li>
        </ol>
        """
    elif "TFTP" in method:
        recovery = d.get("recovery", {})
        tftp_ip = recovery.get("tftp_ip", "192.168.1.1")
        server_ip = recovery.get("tftp_server_ip", "192.168.1.2")
        filename = recovery.get("tftp_filename", f"{dev_id}.bin")
        method_steps = f"""
        <ol style="margin-left: 1.5rem; line-height: 1.8;">
          <li><strong>Configure Host PC:</strong> Connect Ethernet cable to router LAN Port 1. Assign static IP <code>{server_ip}</code>, subnet mask <code>255.255.255.0</code> to host PC interface.</li>
          <li><strong>Prepare TFTP Server:</strong> Place the OpenWrt factory image renamed as <code>{filename}</code> into your TFTP root directory. Start TFTP server (e.g. <code>dnsmasq</code>, <code>tftpd32</code>, or <code>atftpd</code>).</li>
          <li><strong>Trigger Bootloader TFTP Recovery:</strong> Power off the router. Press and hold the Reset / WPS button, then apply power. Maintain button hold for 10-15 seconds until power/status LED starts pulsing rapidly.</li>
          <li><strong>Monitor Transfer & Flash:</strong> Verify in TFTP server log that router requests <code>{filename}</code>. Allow 3 to 5 minutes for automated writing to flash. <strong>Do not disconnect power!</strong></li>
          <li><strong>Access OpenWrt:</strong> Restore host PC to DHCP. Router will reboot into OpenWrt at <code>192.168.1.1</code>.</li>
        </ol>
        """
    elif "Vendor CLI" in method:
        method_steps = f"""
        <ol style="margin-left: 1.5rem; line-height: 1.8;">
          <li><strong>Access Vendor Debug Shell:</strong> Connect via Telnet or SSH using vendor administrative or engineering credentials.</li>
          <li><strong>Transfer OpenWrt Firmware:</strong> Transfer OpenWrt factory image to <code>/tmp</code> using SCP, TFTP, or curl:
            <pre><code>cd /tmp
tftp -g -r openwrt-factory.bin {d.get('recovery', {}).get('tftp_server_ip', '192.168.1.2')}</code></pre>
          </li>
          <li><strong>Write to Flash Partition:</strong> Identify active kernel/rootfs partition and write firmware:
            <pre><code>mtd -r write openwrt-factory.bin firmware</code></pre>
          </li>
          <li><strong>Reboot into OpenWrt:</strong> Allow router to complete writing and automatically reboot. Access LuCI web interface at <code>http://192.168.1.1</code>.</li>
        </ol>
        """
    elif "Serial UART" in method:
        method_steps = f"""
        <ol style="margin-left: 1.5rem; line-height: 1.8;">
          <li><strong>Hardware Preparation:</strong> Connect a 3.3V USB-to-UART adapter to router TX, RX, GND pins. <strong>DO NOT CONNECT VCC</strong>.</li>
          <li><strong>Open Terminal Console:</strong> Run <code>screen /dev/ttyUSB0 115200</code> or PuTTY at 115200 8-N-1.</li>
          <li><strong>Interrupt Bootloader:</strong> Power on router and strike Enter or spacebar to interrupt U-Boot countdown.</li>
          <li><strong>Transfer and Boot Image:</strong> Configure U-Boot network parameters, download factory ramdisk or UBI via TFTP, and write to flash partitions.</li>
        </ol>
        """
    else:
        method_steps = f"""
        <ol style="margin-left: 1.5rem; line-height: 1.8;">
          <li><strong>Download Official Image:</strong> Download the official OpenWrt <strong>factory</strong> image (e.g. <code>openwrt-{openwrt.get('target', 'target')}-{openwrt.get('subtarget', 'generic')}-{dev_id}-squashfs-factory.bin</code>) from <a href="{fw_url}" target="_blank" rel="noopener">OpenWrt Firmware Selector</a>.</li>
          <li><strong>Verify Checksum:</strong> Verify SHA256 checksum of downloaded firmware image against official release manifests before proceeding.</li>
          <li><strong>Log into OEM Web Interface:</strong> Connect PC via Ethernet cable to LAN port. Open browser to vendor gateway (e.g. <code>http://192.168.1.1</code> or <code>http://192.168.0.1</code>) and log into management portal.</li>
          <li><strong>Upload OpenWrt Factory Image:</strong> Navigate to <em>System Tools &rarr; Firmware Upgrade</em>. Select the OpenWrt <code>factory.bin</code> file and initiate upgrade.</li>
          <li><strong>Flash Process & Wait:</strong> The router will verify the image, flash internal storage, and reboot. This takes 2 to 4 minutes. <strong>Do not unplug power or disconnect Ethernet during this process!</strong></li>
          <li><strong>Access OpenWrt:</strong> Once status LED stabilizes, navigate to <code>http://192.168.1.1</code> to access LuCI web interface.</li>
        </ol>
        """

    canonical_url = f"{BASE_URL}/guides/install/{dev_id}/"

    json_ld = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": f"How to Install OpenWrt on {d.get('manufacturer')} {d.get('model')}",
        "description": f"Verified step-by-step instructions to install and configure OpenWrt on {d.get('manufacturer')} {d.get('model')}.",
        "url": canonical_url
    }

    content = f"""
    <div class="breadcrumbs">
      <a href="../../../index.html">Home</a> <span>/</span>
      <a href="../../installation/index.html">Guides</a> <span>/</span>
      <a href="../../../devices/{dev_id}/index.html">{d.get('manufacturer')} {d.get('model')}</a> <span>/</span>
      <strong>Installation Guide</strong>
    </div>

    <div class="section-header">
      <div>
        <div style="display: flex; gap: 0.5rem; align-items: center; margin-bottom: 0.5rem;">
          <span class="badge {badge_cls}">{status.replace('_', ' ')}</span>
          <span class="badge {risk_badge}">Installation Risk: {risk}</span>
        </div>
        <h1 style="font-size: 2.2rem; color: var(--text-heading);">{d.get('manufacturer')} {d.get('model')} OpenWrt Installation Guide</h1>
        <p style="color: var(--text-muted);">Architecture: <code>{d.get('architecture')}</code> | Target: <code>{openwrt.get('target', 'N/A')}/{openwrt.get('subtarget', 'generic')}</code> | Profile: <code>{openwrt.get('profile', 'generic')}</code></p>
      </div>
    </div>

    <div class="callout callout-warning">
      <strong>MANDATORY FACTORY CALIBRATION BACKUP:</strong>
      Before installing OpenWrt, backup all factory partition data (including ART, Factory, and EEPROM partitions). These contain factory RF calibration parameters, Wi-Fi MAC addresses, and regulatory domain constraints unique to your unit.
    </div>

    <div class="card" style="margin-bottom: 2rem;">
      <h2 style="color: var(--text-heading); font-size: 1.25rem; margin-bottom: 1rem;">1. Hardware & Platform Prerequisites</h2>
      <table class="spec-table">
        <tr><th>Device Model</th><td>{d.get('manufacturer')} {d.get('model')} (Rev: <code>{d.get('hardware_revision', 'v1')}</code>)</td></tr>
        <tr><th>Processor (SoC)</th><td>{soc.get('vendor')} {soc.get('model')} ({soc.get('cores', 'N/A')} Cores @ {soc.get('frequency_mhz', 'N/A')} MHz)</td></tr>
        <tr><th>RAM / Flash Storage</th><td>{d.get('ram_mb', 'N/A')} MB RAM / {flash_cap} MB {flash.get('type', '')} Flash</td></tr>
        <tr><th>OpenWrt Target</th><td><code>{openwrt.get('target', 'N/A')}/{openwrt.get('subtarget', 'generic')}</code></td></tr>
        <tr><th>Target Profile</th><td><code>{openwrt.get('profile', 'generic')}</code></td></tr>
        <tr><th>First Supported Version</th><td>{openwrt.get('first_supported_version', 'Mainline')}</td></tr>
        <tr><th>Flashing Method</th><td><strong>{method}</strong></td></tr>
      </table>
      <div style="margin-top: 1.25rem;">
        <a href="{fw_url}" target="_blank" rel="noopener" class="btn btn-primary">Download Official Firmware from OpenWrt &rarr;</a>
      </div>
    </div>

    <div class="card" style="margin-bottom: 2rem;">
      <h2 style="color: var(--text-heading); font-size: 1.25rem; margin-bottom: 1rem;">2. Step-by-Step Installation Procedure</h2>
      {method_steps}
    </div>

    <div class="card" style="margin-bottom: 2rem;">
      <h2 style="color: var(--text-heading); font-size: 1.25rem; margin-bottom: 1rem;">3. First Boot & Initial Configuration</h2>
      <ol style="margin-left: 1.5rem; line-height: 1.8;">
        <li>Connect your computer to LAN Port 1 using a Cat6 Ethernet patch cable.</li>
        <li>Verify computer receives IP address in subnet <code>192.168.1.0/24</code> via DHCP (e.g. <code>192.168.1.150</code>).</li>
        <li>Open terminal and verify ping to router gateway: <code>ping 192.168.1.1</code>.</li>
        <li>SSH into router: <code>ssh root@192.168.1.1</code> (no password initially required).</li>
        <li>Set secure administrator password immediately:
          <pre><code>passwd</code></pre>
        </li>
        <li>Open web browser and navigate to <code>http://192.168.1.1</code> to log into LuCI Web Interface.</li>
      </ol>
    </div>

    <div class="card" style="margin-bottom: 2rem;">
      <h2 style="color: var(--text-heading); font-size: 1.25rem; margin-bottom: 1rem;">4. Post-Installation Verification & Troubleshooting</h2>
      <table class="spec-table">
        <thead>
          <tr><th>Symptom / Check</th><th>Probable Cause</th><th>Resolution Action</th></tr>
        </thead>
        <tbody>
          <tr>
            <td>No DHCP lease on computer</td>
            <td>Computer connected to WAN port instead of LAN port</td>
            <td>Connect cable to LAN Port 1; assign static IP <code>192.168.1.50</code> on host PC.</td>
          </tr>
          <tr>
            <td>Status LED pulsing continuously</td>
            <td>Router booting into failsafe or storage expanding</td>
            <td>Wait up to 3 minutes; if still pulsing, power cycle while holding reset for 2 sec to trigger failsafe.</td>
          </tr>
          <tr>
            <td>LuCI web interface not loading</td>
            <td>Minimal image installed without uhttpd/luci packages</td>
            <td>Connect WAN port to upstream internet, SSH in, and run: <code>opkg update && opkg install luci</code>.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="guide-pagination">
      <a href="../../../devices/{dev_id}/index.html" class="guide-nav-link">
        <span>&larr; Hardware Profile</span>
        <strong>{d.get('manufacturer')} {d.get('model')} Profile</strong>
      </a>
      <a href="../../recovery/{dev_id}/index.html" class="guide-nav-link" style="text-align: right;">
        <span>Recovery Guide &rarr;</span>
        <strong>Disaster Recovery for {d.get('model')}</strong>
      </a>
    </div>

    {get_contribution_panel(f"data/devices/{d.get('id').split('-')[0]}/{dev_id}.json", f"{d.get('manufacturer')} {d.get('model')} Installation Guide", rel_root="../../..")}
    """
    desc = f"Step-by-step OpenWrt installation guide for {d.get('manufacturer')} {d.get('model')}. Flashing instructions, prerequisites, sysupgrade, and initial network configuration."
    return get_header(f"{d.get('manufacturer')} {d.get('model')} Installation Guide", rel_root="../../..", current_nav="installation", description=desc, canonical_path=f"guides/install/{dev_id}/", json_ld=json_ld) + content + get_footer(rel_root="../../..")

def generate_device_recovery_guide(d):
    dev_id = d["id"]
    status = d.get("openwrt", {}).get("support_status", "UNKNOWN")
    badge_cls = get_badge_class(status)
    soc = d.get("soc", {})
    flash = d.get("flash", {})
    openwrt = d.get("openwrt", {})
    recovery = d.get("recovery", {})
    serial_uart = d.get("serial_uart", {}) or recovery
    
    rec_method = recovery.get("method", "TFTP Boot / Push Recovery")
    tftp_ip = recovery.get("tftp_ip", "192.168.1.1")
    server_ip = recovery.get("tftp_server_ip", "192.168.1.2")
    tftp_file = recovery.get("tftp_filename", f"{dev_id}.bin")
    baud_rate = serial_uart.get("baud_rate") or recovery.get("uart_baud") or 115200
    uart_avail = "Available" if (serial_uart.get("available") or serial_uart.get("populated")) else "Unpopulated / Header Pads"

    canonical_url = f"{BASE_URL}/guides/recovery/{dev_id}/"

    json_ld = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": f"Disaster Recovery & Unbricking Guide for {d.get('manufacturer')} {d.get('model')}",
        "description": f"Verified unbricking procedure, TFTP restoration, and 3.3V UART serial recovery for {d.get('manufacturer')} {d.get('model')}.",
        "url": canonical_url
    }

    content = f"""
    <div class="breadcrumbs">
      <a href="../../../index.html">Home</a> <span>/</span>
      <a href="../../recovery/index.html">Guides</a> <span>/</span>
      <a href="../../../devices/{dev_id}/index.html">{d.get('manufacturer')} {d.get('model')}</a> <span>/</span>
      <strong>Disaster Recovery</strong>
    </div>

    <div class="section-header">
      <div>
        <div style="display: flex; gap: 0.5rem; align-items: center; margin-bottom: 0.5rem;">
          <span class="badge {badge_cls}">{status.replace('_', ' ')}</span>
          <span class="badge badge-danger">High Risk Hardware Operations</span>
        </div>
        <h1 style="font-size: 2.2rem; color: var(--text-heading);">{d.get('manufacturer')} {d.get('model')} Disaster Recovery & Unbricking</h1>
        <p style="color: var(--text-muted);">Primary Recovery Protocol: <strong>{rec_method}</strong> | UART Serial: <strong>{uart_avail}</strong> @ {baud_rate} baud</p>
      </div>
    </div>

    <!-- CRITICAL ELECTRICAL WARNING -->
    <div class="callout callout-danger">
      <strong>CRITICAL SAFETY MANDATE — NEVER CONNECT VCC (RED WIRE):</strong>
      When connecting a USB-to-TTL serial adapter to the {d.get('model')} PCB, connect <strong>ONLY GND, TX, and RX</strong>.
      The router provides its own 3.3V/1.8V power rail when plugged into its AC adapter. Connecting the red VCC wire from your USB adapter will backfeed voltage into the power management IC and <strong>permanently destroy the SoC and flash chips</strong>!
      Ensure your USB adapter logic level is set to <strong>3.3V TTL</strong> (never 5V, never RS-232 +/-12V).
    </div>

    <div class="card" style="margin-bottom: 2rem;">
      <h2 style="color: var(--text-heading); font-size: 1.25rem; margin-bottom: 1rem;">1. Recovery Escalation Hierarchy</h2>
      <p style="color: var(--text-muted); margin-bottom: 1rem;">Always attempt recovery in order of increasing intervention. Do not disassemble the enclosure until software fail-safes are exhausted.</p>
      <table class="spec-table">
        <thead>
          <tr><th>Tier</th><th>Method</th><th>When to Use</th><th>Hardware Required</th></tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Tier 1</strong></td>
            <td>OpenWrt Failsafe Mode</td>
            <td>Kernel boots, network config broken, forgotten root password</td>
            <td>Ethernet cable, computer set to DHCP or static <code>192.168.1.2</code></td>
          </tr>
          <tr>
            <td><strong>Tier 2</strong></td>
            <td>TFTP Automated Bootloader Push</td>
            <td>Bootloader intact, corrupted kernel / rootfs, boot loop</td>
            <td>Ethernet cable, TFTP server utility (e.g. <code>dnsmasq</code> / <code>tftpd32</code>)</td>
          </tr>
          <tr>
            <td><strong>Tier 3</strong></td>
            <td>3.3V TTL Serial UART Console</td>
            <td>Bootloader prompt accessible, TFTP fails, diagnose boot failure</td>
            <td>3.3V USB-UART adapter (CP2102/FTDI), jumper wires, soldering iron (if pads unpopulated)</td>
          </tr>
          <tr>
            <td><strong>Tier 4</strong></td>
            <td>External SPI Flash Programmer</td>
            <td>Bootloader erased/corrupted (hard brick), no serial output</td>
            <td>CH341A programmer, SOIC-8 / SOIC-16 test clip, full mtd0 raw flash dump</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="card" style="margin-bottom: 2rem;">
      <h2 style="color: var(--text-heading); font-size: 1.25rem; margin-bottom: 1rem;">2. Tier 1: OpenWrt Failsafe Mode</h2>
      <ol style="margin-left: 1.5rem; line-height: 1.8;">
        <li>Disconnect all cables from router except power and LAN Port 1 to your computer.</li>
        <li>Set computer network interface to static IP: <code>192.168.1.2</code>, netmask: <code>255.255.255.0</code>, gateway: <code>192.168.1.1</code>.</li>
        <li>Power on the router. As soon as the status or power LED begins blinking, press the <strong>WPS / Reset</strong> button repeatedly.</li>
        <li>The status LED will begin blinking extremely rapidly (10 Hz), indicating Failsafe mode is active.</li>
        <li>Connect via Telnet: <code>telnet 192.168.1.1</code>. No password is required.</li>
        <li>Reset configuration to factory defaults:
          <pre><code>mount_root
firstboot -y
sync && reboot</code></pre>
        </li>
      </ol>
    </div>

    <div class="card" style="margin-bottom: 2rem;">
      <h2 style="color: var(--text-heading); font-size: 1.25rem; margin-bottom: 1rem;">3. Tier 2: Bootloader TFTP Restoration</h2>
      <table class="spec-table" style="margin-bottom: 1rem;">
        <tr><th>Router Recovery IP</th><td><code>{tftp_ip}</code></td></tr>
        <tr><th>Host PC TFTP Server IP</th><td><code>{server_ip}</code></td></tr>
        <tr><th>Subnet Mask</th><td><code>255.255.255.0</code></td></tr>
        <tr><th>Expected TFTP Filename</th><td><code>{tftp_file}</code></td></tr>
      </table>
      <ol style="margin-left: 1.5rem; line-height: 1.8;">
        <li>Download official OpenWrt factory firmware image from the repository.</li>
        <li>Rename image file to <code>{tftp_file}</code> and place in TFTP server root directory.</li>
        <li>Configure host PC Ethernet to static IP <code>{server_ip}</code>.</li>
        <li>Power off router. Hold Reset button down and power on. Hold for 10-15 seconds until TFTP request is detected.</li>
        <li>Observe file transfer in TFTP server logs. Allow 3-5 minutes for flash write and reboot.</li>
      </ol>
    </div>

    <div class="card" style="margin-bottom: 2rem;">
      <h2 style="color: var(--text-heading); font-size: 1.25rem; margin-bottom: 1rem;">4. Tier 3: 3.3V TTL Serial UART Console</h2>
      <table class="spec-table" style="margin-bottom: 1rem;">
        <thead>
          <tr><th>Adapter Pin</th><th>Router Header</th><th>Mandatory Instruction</th></tr>
        </thead>
        <tbody>
          <tr><td><strong>GND (Black)</strong></td><td>GND Pad / Pin</td><td>Connect securely to establish common ground reference.</td></tr>
          <tr><td><strong>RX (White)</strong></td><td>TX Pad / Pin</td><td>Connect adapter RX to router TX.</td></tr>
          <tr><td><strong>TX (Green)</strong></td><td>RX Pad / Pin</td><td>Connect adapter TX to router RX.</td></tr>
          <tr><td><strong>VCC (Red)</strong></td><td><span style="color: var(--danger); font-weight: bold;">DISCONNECTED</span></td><td><strong>DO NOT CONNECT!</strong> Router powers itself from AC barrel jack.</td></tr>
        </tbody>
      </table>
      <p style="font-size: 0.92rem; margin-bottom: 1rem;">Configure your terminal emulator (PuTTY, Minicom, Picocom, or Screen):</p>
      <pre><code># Linux / macOS screen command
screen /dev/ttyUSB0 {baud_rate} 8N1

# Picocom command
picocom -b {baud_rate} -d 8 -p n -f n /dev/ttyUSB0</code></pre>
      <p style="font-size: 0.92rem; margin-top: 1rem;">Power on router and observe U-Boot bootlog. Press Enter/Space to enter U-Boot shell:</p>
      <pre><code># Check environment variables
printenv

# Boot kernel via TFTP
setenv ipaddr {tftp_ip}
setenv serverip {server_ip}
tftpboot 0x46000000 {tftp_file}
bootm 0x46000000</code></pre>
    </div>

    <div class="card" style="margin-bottom: 2rem;">
      <h2 style="color: var(--text-heading); font-size: 1.25rem; margin-bottom: 1rem;">5. Calibration & Partition Preservation</h2>
      <div class="callout callout-note">
        If you previously dumped your <code>Factory</code>, <code>ART</code>, or <code>MFG</code> partitions prior to bricking, you can restore them via serial console or OpenWrt shell:
        <pre><code>mtd write /tmp/mtd_Factory.bin Factory
mtd write /tmp/mtd_ART.bin art</code></pre>
        <strong>Never flash another router's calibration partition!</strong> Each contains unique physical RF power calibration values and factory MAC addresses.
      </div>
    </div>

    <div class="guide-pagination">
      <a href="../../install/{dev_id}/index.html" class="guide-nav-link">
        <span>&larr; Installation Guide</span>
        <strong>Install OpenWrt on {d.get('model')}</strong>
      </a>
      <a href="../../../devices/{dev_id}/index.html" class="guide-nav-link" style="text-align: right;">
        <span>Hardware Profile &rarr;</span>
        <strong>{d.get('manufacturer')} {d.get('model')} Specifications</strong>
      </a>
    </div>

    {get_contribution_panel(f"data/devices/{d.get('id').split('-')[0]}/{dev_id}.json", f"{d.get('manufacturer')} {d.get('model')} Recovery Guide", rel_root="../../..")}
    """
    desc = f"Complete disaster recovery and unbricking instructions for {d.get('manufacturer')} {d.get('model')}. TFTP recovery, 3.3V UART serial unbricking, and bootloader restoration."
    return get_header(f"{d.get('manufacturer')} {d.get('model')} Disaster Recovery Guide", rel_root="../../..", current_nav="recovery", description=desc, canonical_path=f"guides/recovery/{dev_id}/", json_ld=json_ld) + content + get_footer(rel_root="../../..")

def generate_chipset_directory(chipsets):
    cards = ""
    for c in chipsets:
        cid = c["id"]
        tier = c.get("openwrt_support_tier", "Tier 2")
        badge_cls = "badge-success" if "Tier 1" in tier else "badge-info"
        cpu = c.get("cpu", {})
        node = f"{c.get('process_node_nm')}nm" if c.get('process_node_nm') else "N/A"

        cards += f"""
        <div class="card filter-card">
          <div>
            <div class="card-header">
              <span class="card-title">{c.get('vendor')} {c.get('part_number')}</span>
              <span class="badge {badge_cls}">{tier}</span>
            </div>
            <div class="card-meta">Marketing: <strong>{c.get('marketing_name')}</strong> | Process: {node}</div>
            <p class="card-body">
              Architecture: <code>{cpu.get('architecture')}</code> ({cpu.get('core_type')})<br>
              Cores: {cpu.get('cores')} @ {cpu.get('max_clock_mhz')} MHz<br>
              Target: <code>{c.get('openwrt_target')}</code>
            </p>
          </div>
          <a href="{cid}/index.html" class="btn btn-sm btn-outline">Inspect Silicon Profile &rarr;</a>
        </div>
        """

    content = f"""
    <div class="section-header">
      <div>
        <h1>Silicon & SoC Architectures Directory</h1>
        <p>Architectural specifications, packet offload engines, and open-source driver modules across 11 network platforms.</p>
      </div>
      <div>
        <input type="text" id="search-input" placeholder="Search chipsets by vendor, part number, arch..." style="padding: 0.5rem 1rem; border-radius: var(--radius-sm); border: 1px solid var(--border); background: var(--bg-card); color: var(--text); min-width: 280px;">
      </div>
    </div>

    <div class="grid-3">
      {cards}
    </div>
    """
    desc = "Architectural directory of 11 router SoCs and wireless silicon platforms supported in OpenWrt, including MediaTek Filogic, Qualcomm, Rockchip, and Broadcom."
    return get_header("Silicon Architectures", rel_root="..", current_nav="chipsets", description=desc, canonical_path="chipsets/") + content + get_footer(rel_root="..")

def generate_chipset_page(c, devices):
    cid = c["id"]
    cpu = c.get("cpu", {})
    drivers = c.get("linux_driver", {})
    wireless = c.get("wireless_subsystem", {})
    accel = c.get("hardware_acceleration", {})
    tier = c.get("openwrt_support_tier", "Tier 2")
    badge_cls = "badge-success" if "Tier 1" in tier else "badge-info"

    matching_devices = [d for d in devices if d.get("chipset_ref") == cid or d.get("soc", {}).get("model", "").lower() in cid.lower()]
    dev_links = "".join([f"<li><a href='../../devices/{d['id']}/index.html'>{d.get('manufacturer')} {d.get('model')}</a> ({d.get('openwrt', {}).get('support_status', 'N/A')})</li>" for d in matching_devices]) or "<li>Catalog records in progress.</li>"

    content = f"""
    <div class="breadcrumbs">
      <a href="../../index.html">Home</a> <span>/</span>
      <a href="../index.html">Chipsets</a> <span>/</span>
      <strong>{c.get('vendor')} {c.get('part_number')}</strong>
    </div>

    <div class="section-header">
      <div>
        <h1 style="font-size: 2.2rem; color: var(--text-heading);">{c.get('vendor')} {c.get('part_number')}</h1>
        <p style="color: var(--text-muted);">Commercial Designation: <strong>{c.get('marketing_name')}</strong> | Process Node: {c.get('process_node_nm')}nm</p>
      </div>
      <div>
        <span class="badge {badge_cls}" style="font-size: 0.9rem; padding: 0.4rem 0.8rem;">{tier}</span>
      </div>
    </div>

    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 2rem; margin-top: 2rem;">
      <div>
        <div class="card" style="margin-bottom: 2rem;">
          <h2 style="color: var(--text-heading); font-size: 1.25rem; margin-bottom: 1rem;">CPU & Hardware Architecture</h2>
          <table class="spec-table">
            <tr><th>Instruction Set</th><td><code>{cpu.get('architecture')}</code></td></tr>
            <tr><th>Microarchitecture</th><td>{cpu.get('core_type')}</td></tr>
            <tr><th>CPU Cores</th><td>{cpu.get('cores')} Physical Cores</td></tr>
            <tr><th>Peak Frequency</th><td>{cpu.get('max_clock_mhz')} MHz</td></tr>
            <tr><th>Hardware Flow Offloading</th><td>{accel.get('flow_offload', 'Software only')}</td></tr>
            <tr><th>Hardware Cryptography</th><td>{ 'Yes (AES-NI / Cryptographic Engine)' if accel.get('crypto_engine') else 'Software' }</td></tr>
          </table>
        </div>

        <div class="card" style="margin-bottom: 2rem;">
          <h2 style="color: var(--text-heading); font-size: 1.25rem; margin-bottom: 1rem;">Upstream Linux & OpenWrt Kernel Drivers</h2>
          <table class="spec-table">
            <tr><th>Wireless Module</th><td><code>{drivers.get('wireless_mac80211', 'Non-integrated / External')}</code></td></tr>
            <tr><th>Ethernet Driver</th><td><code>{drivers.get('ethernet_driver', 'Generic')}</code></td></tr>
            <tr><th>Switch / DSA Driver</th><td><code>{drivers.get('switch_driver', 'Discrete Switch / Direct DSA')}</code></td></tr>
            <tr><th>OpenWrt Target</th><td><code>{c.get('openwrt_target')} / {c.get('openwrt_subtarget', 'generic')}</code></td></tr>
          </table>
        </div>

        <div class="card">
          <h2 style="color: var(--text-heading); font-size: 1.25rem; margin-bottom: 1rem;">Verified Devices Powered by this Chipset</h2>
          <ul style="margin: 0.5rem 0 0 1.5rem; font-size: 0.9rem; color: var(--text);">
            {dev_links}
          </ul>
        </div>
      </div>

      <div>
        <div class="card">
          <h2 style="color: var(--text-heading); font-size: 1.25rem; margin-bottom: 1rem;">Silicon Classification</h2>
          <p style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 1rem;">
            {c.get('notes', 'High-performance networking silicon with active upstream Linux and OpenWrt driver support.')}
          </p>
          <a href="../../explorer/index.html" class="btn btn-sm btn-outline" style="width: 100%; justify-content: center;">Filter in Device Explorer &rarr;</a>
        </div>
      </div>
    </div>

    {get_contribution_panel(f"data/chipsets/{cid}.json", f"{c.get('vendor')} {c.get('part_number')}", rel_root="../..")}
    """
    desc = f"Architectural and driver profile for {c.get('vendor')} {c.get('part_number')} ({c.get('marketing_name')}) in OpenWrt Linux."
    return get_header(f"{c.get('vendor')} {c.get('part_number')}", rel_root="../..", current_nav="chipsets", description=desc, canonical_path=f"chipsets/{cid}/") + content + get_footer(rel_root="../..")

def generate_diagrams_page():
    content = """
    <div class="section-header">
      <div>
        <h1>Interactive Network & Hardware Diagrams</h1>
        <p>Original vector schematics illustrating silicon architecture, recovery tiers, and multi-WAN failover pipelines.</p>
      </div>
    </div>

    <!-- Diagram A: Chipset to Device Graph -->
    <div class="card" style="margin-bottom: 3rem;">
      <h2 style="color: var(--text-heading); font-size: 1.35rem; margin-bottom: 0.5rem;">A. Chipset Silicon to Retail Device Taxonomy</h2>
      <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1.5rem;">Visual mapping of core networking silicon to production OpenWrt devices.</p>
      
      <div style="background: #090d16; border: 1px solid var(--border); border-radius: var(--radius-md); padding: 1.5rem; overflow-x: auto;">
        <svg viewBox="0 0 960 480" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="g-chip" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#0284c7"/>
              <stop offset="100%" stop-color="#0369a1"/>
            </linearGradient>
            <linearGradient id="g-dev" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#1e293b"/>
              <stop offset="100%" stop-color="#0f172a"/>
            </linearGradient>
          </defs>

          <!-- Silicon Column (Left) -->
          <text x="140" y="30" fill="#94a3b8" font-size="14" font-weight="700" text-anchor="middle">SILICON SOC / PLATFORM</text>
          
          <g transform="translate(40, 60)">
            <rect width="200" height="70" rx="8" fill="url(#g-chip)" stroke="#38bdf8" stroke-width="1.5"/>
            <text x="100" y="28" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">MediaTek MT7986A</text>
            <text x="100" y="48" fill="#bae6fd" font-size="11" text-anchor="middle">Filogic 830 (Quad A53 2.0G)</text>
          </g>

          <g transform="translate(40, 160)">
            <rect width="200" height="70" rx="8" fill="url(#g-chip)" stroke="#38bdf8" stroke-width="1.5"/>
            <text x="100" y="28" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">MediaTek MT7981B</text>
            <text x="100" y="48" fill="#bae6fd" font-size="11" text-anchor="middle">Filogic 820 (Dual A53 1.3G)</text>
          </g>

          <g transform="translate(40, 260)">
            <rect width="200" height="70" rx="8" fill="url(#g-chip)" stroke="#38bdf8" stroke-width="1.5"/>
            <text x="100" y="28" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">MediaTek MT7988A</text>
            <text x="100" y="48" fill="#bae6fd" font-size="11" text-anchor="middle">Filogic 880 (Quad A73 Wi-Fi 7)</text>
          </g>

          <g transform="translate(40, 360)">
            <rect width="200" height="70" rx="8" fill="url(#g-chip)" stroke="#38bdf8" stroke-width="1.5"/>
            <text x="100" y="28" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">Qualcomm IPQ8072A</text>
            <text x="100" y="48" fill="#bae6fd" font-size="11" text-anchor="middle">Hawkeye (Quad A53 2.2G)</text>
          </g>

          <!-- Retail Devices Column (Right) -->
          <text x="800" y="30" fill="#94a3b8" font-size="14" font-weight="700" text-anchor="middle">VERIFIED OPENWRT DEVICE</text>

          <g transform="translate(680, 50)">
            <rect width="240" height="40" rx="6" fill="url(#g-dev)" stroke="#10b981" stroke-width="1.5"/>
            <text x="120" y="24" fill="#f8fafc" font-size="12" font-weight="600" text-anchor="middle">Jio / Arcadyan JIDU6101 (6j01)</text>
          </g>

          <g transform="translate(680, 100)">
            <rect width="240" height="40" rx="6" fill="url(#g-dev)" stroke="#10b981" stroke-width="1.5"/>
            <text x="120" y="24" fill="#f8fafc" font-size="12" font-weight="600" text-anchor="middle">GL.iNet GL-MT6000 (Flint 2)</text>
          </g>

          <g transform="translate(680, 150)">
            <rect width="240" height="40" rx="6" fill="url(#g-dev)" stroke="#10b981" stroke-width="1.5"/>
            <text x="120" y="24" fill="#f8fafc" font-size="12" font-weight="600" text-anchor="middle">Banana Pi BPI-R3 (SFP+)</text>
          </g>

          <g transform="translate(680, 210)">
            <rect width="240" height="40" rx="6" fill="url(#g-dev)" stroke="#f59e0b" stroke-width="1.5"/>
            <text x="120" y="24" fill="#f8fafc" font-size="12" font-weight="600" text-anchor="middle">Jio / Arcadyan JIDU6201 (6j02)</text>
          </g>

          <g transform="translate(680, 260)">
            <rect width="240" height="40" rx="6" fill="url(#g-dev)" stroke="#10b981" stroke-width="1.5"/>
            <text x="120" y="24" fill="#f8fafc" font-size="12" font-weight="600" text-anchor="middle">GL.iNet GL-MT3000 (Beryl AX)</text>
          </g>

          <g transform="translate(680, 320)">
            <rect width="240" height="40" rx="6" fill="url(#g-dev)" stroke="#10b981" stroke-width="1.5"/>
            <text x="120" y="24" fill="#f8fafc" font-size="12" font-weight="600" text-anchor="middle">Banana Pi BPI-R4 (10GbE)</text>
          </g>

          <g transform="translate(680, 380)">
            <rect width="240" height="40" rx="6" fill="url(#g-dev)" stroke="#10b981" stroke-width="1.5"/>
            <text x="120" y="24" fill="#f8fafc" font-size="12" font-weight="600" text-anchor="middle">Xiaomi AX9000 (Tri-Band)</text>
          </g>

          <!-- Connecting Curves -->
          <path d="M 240 95 C 460 95, 460 70, 680 70" fill="none" stroke="#06b6d4" stroke-width="2"/>
          <path d="M 240 95 C 460 95, 460 120, 680 120" fill="none" stroke="#06b6d4" stroke-width="2"/>
          <path d="M 240 95 C 460 95, 460 170, 680 170" fill="none" stroke="#06b6d4" stroke-width="2"/>
          <path d="M 240 195 C 460 195, 460 230, 680 230" fill="none" stroke="#06b6d4" stroke-width="2"/>
          <path d="M 240 195 C 460 195, 460 280, 680 280" fill="none" stroke="#06b6d4" stroke-width="2"/>
          <path d="M 240 295 C 460 295, 460 340, 680 340" fill="none" stroke="#06b6d4" stroke-width="2"/>
          <path d="M 240 395 C 460 395, 460 400, 680 400" fill="none" stroke="#06b6d4" stroke-width="2"/>
        </svg>
      </div>
    </div>

    <!-- Diagram B: Filogic 830 Architecture Block -->
    <div class="card" style="margin-bottom: 3rem;">
      <h2 style="color: var(--text-heading); font-size: 1.35rem; margin-bottom: 0.5rem;">B. MediaTek Filogic 830 (MT7986A) Hardware Silicon Architecture</h2>
      <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1.5rem;">Low-level subsystem interconnect: Host CPU, hardware NAT offload, SGMII, and RF transceivers.</p>
      
      <div style="background: #090d16; border: 1px solid var(--border); border-radius: var(--radius-md); padding: 1.5rem; overflow-x: auto;">
        <svg viewBox="0 0 960 420" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg">
          <rect x="40" y="40" width="560" height="340" rx="12" fill="#0f172a" stroke="#0284c7" stroke-width="2" stroke-dasharray="8 4"/>
          <text x="60" y="70" fill="#38bdf8" font-size="16" font-weight="800">MediaTek MT7986A System-on-Chip (Filogic 830)</text>

          <rect x="70" y="100" width="220" height="90" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
          <text x="180" y="130" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">Quad ARM Cortex-A53</text>
          <text x="180" y="150" fill="#94a3b8" font-size="11" text-anchor="middle">2.0 GHz Peak | 64-bit aarch64</text>
          <text x="180" y="170" fill="#38bdf8" font-size="11" text-anchor="middle">32KB L1 + 512KB L2 Cache</text>

          <rect x="320" y="100" width="250" height="90" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="1.5"/>
          <text x="445" y="130" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">Packet Processing Engine (PPE)</text>
          <text x="445" y="150" fill="#10b981" font-size="11" text-anchor="middle">Hardware Flow Offload (Firewall4 / nft)</text>
          <text x="445" y="170" fill="#94a3b8" font-size="11" text-anchor="middle">Wire-Speed NAT / Routing Table Bypass</text>

          <rect x="70" y="220" width="220" height="80" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
          <text x="180" y="250" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">Dual 2.5G SGMII GMAC</text>
          <text x="180" y="270" fill="#94a3b8" font-size="11" text-anchor="middle">GMAC1 (eth1) & GMAC2 (eth0)</text>

          <rect x="320" y="220" width="250" height="80" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
          <text x="445" y="250" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">Wireless Ethernet Dispatch (WED)</text>
          <text x="445" y="270" fill="#94a3b8" font-size="11" text-anchor="middle">Direct Wi-Fi-to-Ethernet DMA</text>

          <g transform="translate(670, 70)">
            <rect width="250" height="110" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="1.5"/>
            <text x="125" y="30" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">MT7976C Dual-Band RF</text>
            <text x="125" y="55" fill="#f59e0b" font-size="11" text-anchor="middle">4x4 2.4 GHz + 4x4 5.0 GHz (HE160)</text>
            <text x="125" y="75" fill="#94a3b8" font-size="11" text-anchor="middle">AX6000 Aggregate Throughput</text>
            <text x="125" y="95" fill="#94a3b8" font-size="10" text-anchor="middle">Dedicated AXI Bus Link</text>
          </g>

          <g transform="translate(670, 220)">
            <rect width="250" height="110" rx="8" fill="#1e293b" stroke="#06b6d4" stroke-width="1.5"/>
            <text x="125" y="30" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">MediaTek MT7531AE Switch</text>
            <text x="125" y="55" fill="#06b6d4" font-size="11" text-anchor="middle">7-Port Gigabit DSA Switch</text>
            <text x="125" y="75" fill="#94a3b8" font-size="11" text-anchor="middle">LAN1 – LAN4 Discrete Ports</text>
            <text x="125" y="95" fill="#94a3b8" font-size="10" text-anchor="middle">2.5 Gbps SGMII Backhaul (eth0)</text>
          </g>

          <path d="M 570 260 L 670 260" stroke="#06b6d4" stroke-width="2.5"/>
          <path d="M 570 125 L 670 125" stroke="#f59e0b" stroke-width="2.5"/>
        </svg>
      </div>
    </div>

    <!-- Diagram C: 5-Tier Recovery Flow -->
    <div class="card" style="margin-bottom: 3rem;">
      <h2 style="color: var(--text-heading); font-size: 1.35rem; margin-bottom: 0.5rem;">C. 5-Tier OpenWrt Recovery & De-Bricking Hierarchy</h2>
      <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1.5rem;">Escalation methodology from software rollback to in-circuit flash programming.</p>
      
      <div style="background: #090d16; border: 1px solid var(--border); border-radius: var(--radius-md); padding: 1.5rem; overflow-x: auto;">
        <svg viewBox="0 0 960 360" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg">
          <g transform="translate(40, 40)">
            <rect width="160" height="260" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="1.5"/>
            <text x="80" y="35" fill="#10b981" font-size="14" font-weight="800" text-anchor="middle">TIER 1</text>
            <text x="80" y="60" fill="#ffffff" font-size="12" font-weight="700" text-anchor="middle">Failsafe Shell</text>
            <text x="80" y="100" fill="#94a3b8" font-size="10" text-anchor="middle">Reset button timing</text>
            <text x="80" y="120" fill="#94a3b8" font-size="10" text-anchor="middle">SSH @ 192.168.1.1</text>
            <text x="80" y="140" fill="#94a3b8" font-size="10" text-anchor="middle">firstboot -y</text>
            <rect x="20" y="210" width="120" height="30" rx="4" fill="rgba(16, 185, 129, 0.2)"/>
            <text x="80" y="230" fill="#10b981" font-size="11" font-weight="700" text-anchor="middle">Zero Risk</text>
          </g>

          <g transform="translate(220, 40)">
            <rect width="160" height="260" rx="8" fill="#1e293b" stroke="#06b6d4" stroke-width="1.5"/>
            <text x="80" y="35" fill="#06b6d4" font-size="14" font-weight="800" text-anchor="middle">TIER 2</text>
            <text x="80" y="60" fill="#ffffff" font-size="12" font-weight="700" text-anchor="middle">OEM Web Failsafe</text>
            <text x="80" y="100" fill="#94a3b8" font-size="10" text-anchor="middle">Hold Reset 10s</text>
            <text x="80" y="120" fill="#94a3b8" font-size="10" text-anchor="middle">U-Boot HTTP daemon</text>
            <text x="80" y="140" fill="#94a3b8" font-size="10" text-anchor="middle">Upload stock/sysupgrade</text>
            <rect x="20" y="210" width="120" height="30" rx="4" fill="rgba(6, 182, 212, 0.2)"/>
            <text x="80" y="230" fill="#06b6d4" font-size="11" font-weight="700" text-anchor="middle">Low Risk</text>
          </g>

          <g transform="translate(400, 40)">
            <rect width="160" height="260" rx="8" fill="#1e293b" stroke="#3b82f6" stroke-width="1.5"/>
            <text x="80" y="35" fill="#3b82f6" font-size="14" font-weight="800" text-anchor="middle">TIER 3</text>
            <text x="80" y="60" fill="#ffffff" font-size="12" font-weight="700" text-anchor="middle">TFTP Net Recovery</text>
            <text x="80" y="100" fill="#94a3b8" font-size="10" text-anchor="middle">PC static IP host</text>
            <text x="80" y="120" fill="#94a3b8" font-size="10" text-anchor="middle">Automated TFTP pull</text>
            <text x="80" y="140" fill="#94a3b8" font-size="10" text-anchor="middle">RAM initramfs boot</text>
            <rect x="20" y="210" width="120" height="30" rx="4" fill="rgba(59, 130, 246, 0.2)"/>
            <text x="80" y="230" fill="#3b82f6" font-size="11" font-weight="700" text-anchor="middle">Moderate Risk</text>
          </g>

          <g transform="translate(580, 40)">
            <rect width="160" height="260" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="1.5"/>
            <text x="80" y="35" fill="#f59e0b" font-size="14" font-weight="800" text-anchor="middle">TIER 4</text>
            <text x="80" y="60" fill="#ffffff" font-size="12" font-weight="700" text-anchor="middle">3.3V Serial UART</text>
            <text x="80" y="100" fill="#94a3b8" font-size="10" text-anchor="middle">TTL adapter (115200)</text>
            <text x="80" y="120" fill="#94a3b8" font-size="10" text-anchor="middle">GND, TX, RX pins</text>
            <text x="80" y="140" fill="#f87171" font-size="10" text-anchor="middle">STRICTLY NO VCC</text>
            <rect x="20" y="210" width="120" height="30" rx="4" fill="rgba(245, 158, 11, 0.2)"/>
            <text x="80" y="230" fill="#f59e0b" font-size="11" font-weight="700" text-anchor="middle">Hardware Soldering</text>
          </g>

          <g transform="translate(760, 40)">
            <rect width="160" height="260" rx="8" fill="#1e293b" stroke="#ef4444" stroke-width="1.5"/>
            <text x="80" y="35" fill="#ef4444" font-size="14" font-weight="800" text-anchor="middle">TIER 5</text>
            <text x="80" y="60" fill="#ffffff" font-size="12" font-weight="700" text-anchor="middle">SPI Programmer</text>
            <text x="80" y="100" fill="#94a3b8" font-size="10" text-anchor="middle">CH341A / T48 flasher</text>
            <text x="80" y="120" fill="#94a3b8" font-size="10" text-anchor="middle">SOIC8 / WSON clip</text>
            <text x="80" y="140" fill="#94a3b8" font-size="10" text-anchor="middle">Restore raw fullchip</text>
            <rect x="20" y="210" width="120" height="30" rx="4" fill="rgba(239, 68, 68, 0.2)"/>
            <text x="80" y="230" fill="#ef4444" font-size="11" font-weight="700" text-anchor="middle">Expert Operation</text>
          </g>
        </svg>
      </div>
    </div>

    {get_contribution_panel("docs/hardware-overview.md", "Architecture Diagrams", rel_root="..")}
    """
    desc = "Interactive SVG architecture diagrams for MediaTek Filogic SoCs, OpenWrt recovery tiers, and multi-WAN failover networks."
    return get_header("Architecture Diagrams", rel_root="..", current_nav="diagrams", description=desc, canonical_path="diagrams/") + content + get_footer(rel_root="..")

def generate_installation_guide():
    content = """
    <div class="breadcrumbs">
      <a href="../../index.html">Home</a> <span>/</span>
      <a href="../recovery/index.html">Guides</a> <span>/</span>
      <strong>Two-Stage Installation</strong>
    </div>

    <div class="section-header">
      <div>
        <h1>Two-Stage OpenWrt Installation Guide</h1>
        <p>Verified protocol for MediaTek MT7986A / Filogic 830 dual-slot SPI-NAND routers.</p>
      </div>
    </div>

    <div class="callout callout-warning">
      <strong>CRITICAL SAFETY PREREQUISITE:</strong> Never flash any router without dumping and verifying your factory calibration partitions (<code>Factory</code>, <code>MFG</code>). These contain unique MAC addresses and radio RF calibration parameters that cannot be recovered from public images.
    </div>

    <div class="card" style="margin-bottom: 2rem;">
      <h2 style="color: var(--text-heading); font-size: 1.3rem; margin-bottom: 1rem;">1. Mandatory Pre-Installation Flash Backup</h2>
      <p style="font-size: 0.92rem; color: var(--text); margin-bottom: 1rem;">Log into your router via SSH and transfer full binary dumps to your host computer:</p>
      <pre><code># [Router Shell]
cat /proc/mtd
dd if=/dev/mtd0 of=/tmp/mtd0_fullchip.bin bs=128k
dd if=/dev/mtd3 of=/tmp/mtd3_Factory.bin
dd if=/dev/mtd7 of=/tmp/mtd7_MFG.bin

# [Host PC Terminal]
scp root@192.168.1.1:/tmp/mtd*_*.bin ./backup/</code></pre>
    </div>

    <div class="card" style="margin-bottom: 2rem;">
      <h2 style="color: var(--text-heading); font-size: 1.3rem; margin-bottom: 1rem;">2. Stage 1: Ramdisk Staging in Secondary Slot</h2>
      <p style="font-size: 0.92rem; color: var(--text); margin-bottom: 1rem;">Write the initial ramdisk kernel to <code>mtd6</code> and set temporary U-Boot parameters to bypass OEM signature checks without touching permanent bootloader code:</p>
      <pre><code>ubiformat /dev/mtd6 -y -f /tmp/openwrt-factory.ubi
fw_setenv bootcmd "ubi detach; ubi part ubi2; ubi read 46000000 kernel; fdt addr \\$(fdtcontroladdr); fdt rm /signature; bootm 0x46000000"
fw_setenv dual_boot.slot_0_invalid 1
fw_setenv dual_boot.slot_1_invalid 1
sync && reboot</code></pre>
    </div>

    <div class="card">
      <h2 style="color: var(--text-heading); font-size: 1.3rem; margin-bottom: 1rem;">3. Stage 2: Permanent Sysupgrade Flashing</h2>
      <p style="font-size: 0.92rem; color: var(--text); margin-bottom: 1rem;">The router reboots into OpenWrt operating purely in DDR3 RAM at <code>192.168.1.1</code>. Upload the final official OpenWrt 25.12.6 sysupgrade image and flash permanently:</p>
      <pre><code>sysupgrade -n /tmp/openwrt-sysupgrade.bin</code></pre>
    </div>

    <div class="guide-pagination">
      <a href="../../index.html" class="guide-nav-link">
        <span>&larr; Previous</span>
        <strong>Home Overview</strong>
      </a>
      <a href="../recovery/index.html" class="guide-nav-link" style="text-align: right;">
        <span>Next Guide &rarr;</span>
        <strong>Disaster Recovery & Unbricking</strong>
      </a>
    </div>

    {get_contribution_panel("docs/installation.md", "Two-Stage Installation Guide", rel_root="../..")}
    """
    desc = "Step-by-step two-stage installation guide for OpenWrt on MediaTek Filogic 830 / MT7986A routers without hardware disassembly."
    return get_header("Two-Stage Installation", rel_root="../..", current_nav="installation", description=desc, canonical_path="guides/installation/") + content + get_footer(rel_root="../..")

def generate_recovery_guide():
    json_ld = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": "OpenWrt Disaster Recovery Guide: TFTP Recovery & 3.3V TTL UART Unbricking",
        "description": "Comprehensive engineering guide to unbricking OpenWrt routers via TFTP, OEM web failsafe, 3.3V UART serial console, and SPI flash restoration.",
        "author": { "@type": "Person", "name": "Rny0007" },
        "url": f"{BASE_URL}/guides/recovery/"
    }

    content = f"""
    <div class="breadcrumbs">
      <a href="../../index.html">Home</a> <span>/</span>
      <a href="index.html">Guides</a> <span>/</span>
      <strong>Disaster Recovery & Unbricking</strong>
    </div>

    <div class="section-header">
      <div>
        <div style="display: flex; gap: 0.5rem; align-items: center; margin-bottom: 0.5rem;">
          <span class="badge badge-success">OpenWrt 25.12.6 / Mainline</span>
          <span class="badge badge-danger">Risk Level: High (Hardware Operations)</span>
          <span class="badge badge-info">Verified: 2026-11-15</span>
        </div>
        <h1 style="font-size: 2.3rem;">Disaster Recovery & Unbricking Guide</h1>
        <p>Comprehensive engineering methodology for diagnosing, recovering, and unbricking OpenWrt routers across 5 escalation tiers.</p>
      </div>
    </div>

    <div class="docs-layout">
      <!-- Sticky Desktop Table of Contents -->
      <aside class="docs-sidebar" aria-label="Table of Contents">
        <h4>Table of Contents</h4>
        <ul>
          <li><a href="#sec-1-diagnosis" class="toc-link">1. Initial Diagnosis & Faults</a></li>
          <li><a href="#sec-2-flowchart" class="toc-link">2. Decision Flowchart</a></li>
          <li><a href="#sec-3-prerequisites" class="toc-link">3. Required Tools & Bench</a></li>
          <li><a href="#sec-4-preservation" class="toc-link">4. Partition Preservation</a></li>
          <li><a href="#sec-5-tiers" class="toc-link">5. Five Recovery Tiers</a></li>
          <li><a href="#sec-6-device-notes" class="toc-link">6. Device-Specific Notes</a></li>
          <li><a href="#sec-7-verification" class="toc-link">7. Success Verification</a></li>
          <li><a href="#sec-8-troubleshooting" class="toc-link">8. Troubleshooting Table</a></li>
          <li><a href="#sec-9-safety" class="toc-link">9. Electrical Safety Rules</a></li>
          <li><a href="#sec-10-references" class="toc-link">10. Primary Citations</a></li>
        </ul>
      </aside>

      <!-- Main Documentation Content -->
      <article class="docs-content">
        <!-- Section 1 -->
        <section id="sec-1-diagnosis" class="card" style="margin-bottom: 2rem;">
          <h2 style="color: var(--text-heading); font-size: 1.35rem; margin-bottom: 0.75rem;">1. Initial Diagnosis & Fault Matrix</h2>
          <p style="font-size: 0.92rem; color: var(--text); line-height: 1.6; margin-bottom: 1rem;">
            Before connecting hardware probes or flashing recovery images, systematically classify the router's hardware failure mode:
          </p>

          <div class="table-container">
            <table class="spec-table">
              <thead>
                <tr>
                  <th>Observable Symptom</th>
                  <th>Hardware Subsystem Status</th>
                  <th>Suspected Root Cause</th>
                  <th>Recommended Tier</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>Solid Red / Dark LED</strong></td>
                  <td>Bootloader BL2 not executing</td>
                  <td>Corrupted SPI-NAND partition table or damaged BL2 header</td>
                  <td><span class="badge badge-danger">Tier 4 / Tier 5</span></td>
                </tr>
                <tr>
                  <td><strong>Flashing Rapid Pulse (Heartbeat)</strong></td>
                  <td>Linux Kernel booting; LuCI offline</td>
                  <td>Firewall misconfiguration or <code>uhttpd</code> service crash</td>
                  <td><span class="badge badge-success">Tier 1 (Failsafe)</span></td>
                </tr>
                <tr>
                  <td><strong>Link Flapping (5-8s cycle)</strong></td>
                  <td>U-Boot watchdog resetting kernel</td>
                  <td>Kernel panic during rootfs mount (UBI corrupted)</td>
                  <td><span class="badge badge-info">Tier 2 / Tier 3</span></td>
                </tr>
                <tr>
                  <td><strong>No Ping to 192.168.1.1</strong></td>
                  <td>Network stack uninitialized or subnet mismatch</td>
                  <td>Host adapter IP configured on wrong subnet (e.g. 192.168.0.x)</td>
                  <td><span class="badge badge-warning">Tier 1 / Static IP</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Section 2 -->
        <section id="sec-2-flowchart" class="card" style="margin-bottom: 2rem;">
          <h2 style="color: var(--text-heading); font-size: 1.35rem; margin-bottom: 0.75rem;">2. Recovery Decision Flowchart</h2>
          <p style="font-size: 0.92rem; color: var(--text); margin-bottom: 1rem;">Follow this non-destructive escalation tree to recover device functionality:</p>

          <div class="decision-diagram" style="background: #090d16; border: 1px solid var(--border); border-radius: var(--radius-md); padding: 1.5rem; overflow-x: auto;">
            <svg viewBox="0 0 800 320" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg">
              <rect x="20" y="20" width="220" height="60" rx="8" fill="#1e293b" stroke="#06b6d4" stroke-width="2"/>
              <text x="130" y="45" fill="#ffffff" font-size="12" font-weight="700" text-anchor="middle">Power-on LED Pulse?</text>
              <text x="130" y="65" fill="#38bdf8" font-size="10" text-anchor="middle">Press Reset immediately</text>

              <path d="M 240 50 L 300 50" stroke="#10b981" stroke-width="2"/>
              <text x="270" y="42" fill="#10b981" font-size="10" text-anchor="middle">Yes</text>

              <rect x="300" y="20" width="220" height="60" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
              <text x="410" y="45" fill="#ffffff" font-size="12" font-weight="700" text-anchor="middle">Tier 1: Failsafe Mode</text>
              <text x="410" y="65" fill="#94a3b8" font-size="10" text-anchor="middle">SSH root@192.168.1.1</text>

              <path d="M 130 80 L 130 130" stroke="#f59e0b" stroke-width="2"/>
              <text x="145" y="110" fill="#f59e0b" font-size="10">No</text>

              <rect x="20" y="130" width="220" height="60" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
              <text x="130" y="155" fill="#ffffff" font-size="12" font-weight="700" text-anchor="middle">Hold Reset 10s on boot</text>
              <text x="130" y="175" fill="#f59e0b" font-size="10" text-anchor="middle">Check TFTP / Web daemon</text>

              <path d="M 240 160 L 300 160" stroke="#10b981" stroke-width="2"/>
              <text x="270" y="152" fill="#10b981" font-size="10" text-anchor="middle">Yes</text>

              <rect x="300" y="130" width="220" height="60" rx="8" fill="#1e293b" stroke="#06b6d4" stroke-width="2"/>
              <text x="410" y="155" fill="#ffffff" font-size="12" font-weight="700" text-anchor="middle">Tier 2/3: TFTP / Web Failsafe</text>
              <text x="410" y="175" fill="#94a3b8" font-size="10" text-anchor="middle">Push initramfs recovery</text>

              <path d="M 130 190 L 130 240" stroke="#ef4444" stroke-width="2"/>
              <text x="145" y="220" fill="#ef4444" font-size="10">No</text>

              <rect x="20" y="240" width="220" height="60" rx="8" fill="#1e293b" stroke="#ef4444" stroke-width="2"/>
              <text x="130" y="265" fill="#ffffff" font-size="12" font-weight="700" text-anchor="middle">Connect 3.3V UART Serial</text>
              <text x="130" y="285" fill="#ef4444" font-size="10" text-anchor="middle">GND, TX, RX (Never VCC!)</text>

              <path d="M 240 270 L 300 270" stroke="#10b981" stroke-width="2"/>
              <text x="270" y="262" fill="#10b981" font-size="10" text-anchor="middle">U-Boot OK</text>

              <rect x="300" y="240" width="220" height="60" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
              <text x="410" y="265" fill="#ffffff" font-size="12" font-weight="700" text-anchor="middle">Tier 4: UART CLI Recovery</text>
              <text x="410" y="285" fill="#94a3b8" font-size="10" text-anchor="middle">tftpboot into RAM</text>

              <path d="M 520 270 L 580 270" stroke="#ef4444" stroke-width="2"/>
              <text x="550" y="262" fill="#ef4444" font-size="10">No output</text>

              <rect x="580" y="240" width="190" height="60" rx="8" fill="#1e293b" stroke="#ef4444" stroke-width="2"/>
              <text x="675" y="265" fill="#ffffff" font-size="12" font-weight="700" text-anchor="middle">Tier 5: External SPI</text>
              <text x="675" y="285" fill="#ef4444" font-size="10" text-anchor="middle">CH341A Flasher Clip</text>
            </svg>
          </div>
        </section>

        <!-- Section 3 -->
        <section id="sec-3-prerequisites" class="card" style="margin-bottom: 2rem;">
          <h2 style="color: var(--text-heading); font-size: 1.35rem; margin-bottom: 0.75rem;">3. Required Tools & Bench Prerequisites</h2>
          <div class="callout callout-warning" style="margin-top: 0; margin-bottom: 1.25rem;">
            <strong>LOGIC LEVEL SAFETY WARNING:</strong> Always verify that your USB-to-UART adapter is set to 3.3V TTL mode via physical jumper or switch. Standard 5V FTDI or RS-232 (+12V/-12V) adapters will overvoltage and permanently destroy the SoC GPIO silicon.
          </div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
            <div>
              <h3 style="font-size: 1.05rem; color: var(--text-heading); margin-bottom: 0.5rem;">Hardware Equipment</h3>
              <ul style="margin-left: 1.5rem; font-size: 0.88rem; color: var(--text); line-height: 1.7;">
                <li><strong>USB-UART Adapter:</strong> CP2102, FT232RL, or CH340G with physical 3.3V jumper set.</li>
                <li><strong>Dupont Jumper Wires:</strong> Female-to-female and female-to-male test leads.</li>
                <li><strong>Cat6 Ethernet Cables:</strong> Direct host-to-router connection (LAN1).</li>
                <li><strong>Uninterruptible Power Supply (UPS):</strong> Ensures stable voltage during flash operations.</li>
                <li><strong>Digital Multimeter:</strong> Verify 3.3V logic level between TX and GND before connecting.</li>
              </ul>
            </div>
            <div>
              <h3 style="font-size: 1.05rem; color: var(--text-heading); margin-bottom: 0.5rem;">Software Utilities</h3>
              <ul style="margin-left: 1.5rem; font-size: 0.88rem; color: var(--text); line-height: 1.7;">
                <li><strong>Serial Console:</strong> PuTTY (Windows) or <code>picocom</code> / <code>minicom</code> (Linux).</li>
                <li><strong>TFTP Server:</strong> Tftpd64 portable (Windows) or <code>tftpd-hpa</code> (Linux).</li>
                <li><strong>OpenSSH Client:</strong> Pre-installed on Windows PowerShell 10+ and Linux.</li>
                <li><strong>Recovery Kernel:</strong> Official OpenWrt <code>*-initramfs-recovery.bin</code> image.</li>
              </ul>
            </div>
          </div>
        </section>

        <!-- Section 4 -->
        <section id="sec-4-preservation" class="card" style="margin-bottom: 2rem;">
          <h2 style="color: var(--text-heading); font-size: 1.35rem; margin-bottom: 0.75rem;">4. Mandatory Partition Preservation Protocol</h2>
          <div class="callout callout-danger" style="margin-top: 0;">
            <strong>DO NOT OVERWRITE CALIBRATION PARTITIONS:</strong>
            The vendor <code>Factory</code> and <code>MFG</code> partitions contain cryptographically signed RF calibration values and physical MAC address labels tuned specifically to your device's RF front-end module. Erasing them causes irreversible Wi-Fi power degradation (dropping signal by up to 15 dBm).
          </div>
          <p style="font-size: 0.92rem; color: var(--text); margin-bottom: 0.75rem;">Whenever terminal access or failsafe shell is available, immediately archive all MTD partitions:</p>
          <pre><code># [Router Terminal]
cat /proc/mtd
dd if=/dev/mtd0 of=/tmp/mtd0_fullchip_backup.bin bs=128k
dd if=/dev/mtd3 of=/tmp/mtd3_Factory.bin
dd if=/dev/mtd7 of=/tmp/mtd7_MFG.bin</code></pre>
        </section>

        <!-- Section 5 -->
        <section id="sec-5-tiers" class="card" style="margin-bottom: 2rem;">
          <h2 style="color: var(--text-heading); font-size: 1.35rem; margin-bottom: 0.75rem;">5. The Five Recovery Tiers</h2>

          <!-- Tier 1 -->
          <div style="border-bottom: 1px solid var(--border); padding-bottom: 1.5rem; margin-bottom: 1.5rem;">
            <h3 style="color: var(--success); font-size: 1.15rem; margin-bottom: 0.5rem;">Tier 1: OpenWrt Failsafe Mode</h3>
            <p style="font-size: 0.9rem; color: var(--text); line-height: 1.6; margin-bottom: 0.75rem;">
              If OpenWrt boots but custom firewall rules or network settings lock out web/SSH access, enter failsafe mode:
            </p>
            <ol style="margin-left: 1.5rem; font-size: 0.88rem; color: var(--text); line-height: 1.7;">
              <li>Set PC Static IP: <code>192.168.1.2</code> (Subnet <code>255.255.255.0</code>). Connect cable to router LAN1.</li>
              <li>Power cycle router. When the front LED flashes rapidly, press the physical <strong>RESET</strong> button once.</li>
              <li>Open terminal and execute:</li>
            </ol>
            <pre><code>ssh -o StrictHostKeyChecking=no root@192.168.1.1
mount_root
firstboot -y
reboot -f</code></pre>
          </div>

          <!-- Tier 2 -->
          <div style="border-bottom: 1px solid var(--border); padding-bottom: 1.5rem; margin-bottom: 1.5rem;">
            <h3 style="color: var(--primary); font-size: 1.15rem; margin-bottom: 0.5rem;">Tier 2: OEM Web Failsafe Interface</h3>
            <p style="font-size: 0.9rem; color: var(--text); line-height: 1.6; margin-bottom: 0.75rem;">
              MediaTek Filogic and GL.iNet bootloaders feature an embedded HTTP server in U-Boot:
            </p>
            <ol style="margin-left: 1.5rem; font-size: 0.88rem; color: var(--text); line-height: 1.7;">
              <li>Set PC static IP to <code>192.168.1.2</code>. Connect to LAN1.</li>
              <li>Power on the router while holding down the <strong>RESET</strong> button for 8 to 10 seconds.</li>
              <li>Navigate to <code>http://192.168.1.1</code> in your web browser. Upload the official OpenWrt sysupgrade binary.</li>
            </ol>
          </div>

          <!-- Tier 3 -->
          <div style="border-bottom: 1px solid var(--border); padding-bottom: 1.5rem; margin-bottom: 1.5rem;">
            <h3 style="color: var(--info); font-size: 1.15rem; margin-bottom: 0.5rem;">Tier 3: Automated Bootloader TFTP Client Mode</h3>
            <p style="font-size: 0.9rem; color: var(--text); line-height: 1.6; margin-bottom: 0.75rem;">
              When rootfs cannot mount, the bootloader broadcasts TFTP requests to predefined IP addresses:
            </p>
            <div class="table-container">
              <table class="spec-table">
                <thead>
                  <tr>
                    <th>Platform / Vendor</th>
                    <th>Router Target IP</th>
                    <th>Host PC TFTP Server IP</th>
                    <th>Required Image Filename</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>MediaTek Filogic (U-Boot)</strong></td>
                    <td><code>192.168.1.1</code></td>
                    <td><code>192.168.1.254</code> (or <code>192.168.1.10</code>)</td>
                    <td><code>openwrt.bin</code> / <code>recovery.bin</code></td>
                  </tr>
                  <tr>
                    <td><strong>TP-Link MediaTek</strong></td>
                    <td><code>192.168.0.1</code></td>
                    <td><code>192.168.0.66</code></td>
                    <td><code>ArcherC6v3_tp_recovery.bin</code></td>
                  </tr>
                  <tr>
                    <td><strong>Xiaomi / Redmi</strong></td>
                    <td><code>192.168.31.1</code></td>
                    <td><code>192.168.31.100</code></td>
                    <td><code>test.bin</code></td>
                  </tr>
                  <tr>
                    <td><strong>Netgear WAX206</strong></td>
                    <td><code>192.168.1.1</code></td>
                    <td><code>192.168.1.10</code></td>
                    <td><code>wax206.img</code></td>
                  </tr>
                </tbody>
              </table>
            </div>
            <pre><code># Linux TFTP Server Setup
sudo apt install tftpd-hpa
sudo cp openwrt-*-initramfs.bin /var/lib/tftpboot/openwrt.bin
sudo systemctl restart tftpd-hpa</code></pre>
          </div>

          <!-- Tier 4 -->
          <div style="border-bottom: 1px solid var(--border); padding-bottom: 1.5rem; margin-bottom: 1.5rem;">
            <h3 style="color: var(--warning); font-size: 1.15rem; margin-bottom: 0.5rem;">Tier 4: Hardware 3.3V TTL Serial UART Console</h3>
            <div class="callout callout-danger" style="margin-top: 0;">
              <strong>CRITICAL ELECTRICAL RULE:</strong> Connect ONLY <code>GND</code>, <code>TX</code>, and <code>RX</code>. <strong>NEVER CONNECT THE VCC PIN</strong> from your USB-UART adapter. Doing so causes power back-feeding and can permanently destroy the SoC.
            </div>
            <pre><code>USB-UART Adapter                Router PCB Serial Header
[ GND ] ------------------------ [ GND ] (Ground reference)
[ RX  ] ------------------------ [ TX  ] (Crossover transmit)
[ TX  ] ------------------------ [ RX  ] (Crossover receive)
[ VCC ] (DISCONNECTED)           [ VCC ] (STRICTLY DISCONNECTED)</code></pre>
            <p style="font-size: 0.9rem; color: var(--text); line-height: 1.6; margin: 0.75rem 0;">
              Open PuTTY (Windows) or picocom (Linux) at <strong>115200 baud, 8 data bits, 1 stop bit, no parity (8N1)</strong>. Power cycle the router and repeatedly press <code>Space</code> or <code>Enter</code> to interrupt autoboot into the U-Boot console:
            </p>
            <pre><code># Configure network inside U-Boot
setenv ipaddr 192.168.1.1
setenv serverip 192.168.1.254
ping 192.168.1.254

# Load initramfs recovery kernel into DDR RAM
tftpboot 0x46000000 openwrt-initramfs.bin
fdt addr \\$(fdtcontroladdr)
fdt rm /signature
bootm 0x46000000</code></pre>
          </div>

          <!-- Tier 5 -->
          <div>
            <h3 style="color: var(--danger); font-size: 1.15rem; margin-bottom: 0.5rem;">Tier 5: External Hardware Flash Programmer</h3>
            <p style="font-size: 0.9rem; color: var(--text); line-height: 1.6; margin-bottom: 0.75rem;">
              When the SPI-NAND bootloader partitions (`BL2`, `FIP`) are completely erased or corrupted, attach a CH341A or T48 external hardware programmer with a SOIC8/WSON clip directly to the flash chip:
            </p>
            <pre><code># Flash raw fullchip dump to SPI chip
flashrom -p ch341a_spi -w mtd0_fullchip_backup.bin</code></pre>
          </div>
        </section>

        <!-- Section 6 -->
        <section id="sec-6-device-notes" class="card" style="margin-bottom: 2rem;">
          <h2 style="color: var(--text-heading); font-size: 1.35rem; margin-bottom: 0.75rem;">6. Device-Specific Recovery Notes</h2>
          <div class="table-container">
            <table class="spec-table">
              <thead>
                <tr>
                  <th>Device Model</th>
                  <th>Primary Recovery Path</th>
                  <th>UART Pinout & Details</th>
                  <th>Verification Status</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>Jio JIDU6101</strong></td>
                  <td>Dual-slot U-Boot rollback (<code>fw_setenv dual_boot.slot_*_invalid 0</code>)</td>
                  <td>Unpopulated 4-pin header near SoC shield: VCC (leave open), TX, RX, GND (115200 8N1)</td>
                  <td><span class="badge badge-success">Verified</span></td>
                </tr>
                <tr>
                  <td><strong>Jio JIDU6201</strong></td>
                  <td>Dual-boot slot recovery</td>
                  <td>3.3V TTL header adjacent to SoC shield (115200 8N1)</td>
                  <td><span class="badge badge-warning">Community Verified</span></td>
                </tr>
                <tr>
                  <td><strong>GL.iNet GL-MT6000</strong></td>
                  <td>U-Boot Web Failsafe at <code>192.168.1.1</code> (hold reset 8s)</td>
                  <td>Internal 4-pin UART pads (115200 8N1)</td>
                  <td><span class="badge badge-success">Verified</span></td>
                </tr>
                <tr>
                  <td><strong>Banana Pi BPI-R3</strong></td>
                  <td>Hardware boot DIP switch (switch to MicroSD boot)</td>
                  <td>Dedicated 3-pin UART debug header (115200 8N1)</td>
                  <td><span class="badge badge-success">Verified</span></td>
                </tr>
                <tr>
                  <td><strong>FriendlyElec R5S</strong></td>
                  <td>Rockchip Maskrom mode via Type-C USB (<code>rkdeveloptool</code>)</td>
                  <td>Dedicated debug UART header (1500000 baud)</td>
                  <td><span class="badge badge-success">Verified</span></td>
                </tr>
                <tr>
                  <td><strong>Netgear WAX206</strong></td>
                  <td>TFTP client push to server <code>192.168.1.10</code></td>
                  <td>Internal 4-pin UART header (115200 8N1)</td>
                  <td><span class="badge badge-success">Verified</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Section 7 -->
        <section id="sec-7-verification" class="card" style="margin-bottom: 2rem;">
          <h2 style="color: var(--text-heading); font-size: 1.35rem; margin-bottom: 0.75rem;">7. Success Verification Protocol</h2>
          <p style="font-size: 0.92rem; color: var(--text); line-height: 1.6; margin-bottom: 1rem;">
            After executing recovery procedures, verify operational health in this exact sequence:
          </p>
          <ul style="margin-left: 1.5rem; font-size: 0.88rem; color: var(--text); line-height: 1.8;">
            <li><strong>ICMP Echo Response:</strong> <code>ping 192.168.1.1</code> responds consistently with round-trip times &lt; 1.0 ms and 0% packet loss.</li>
            <li><strong>LuCI Web Interface:</strong> Open <code>http://192.168.1.1</code> in an incognito browser window and confirm OpenWrt login banner renders.</li>
            <li><strong>SSH Authentication:</strong> <code>ssh root@192.168.1.1</code> connects cleanly without Dropbear host key errors.</li>
            <li><strong>Kernel dmesg Audit:</strong> Run <code>dmesg | grep -iE "fail|error|panic"</code> to ensure no persistent hardware driver crashes.</li>
          </ul>
        </section>

        <!-- Section 8 -->
        <section id="sec-8-troubleshooting" class="card" style="margin-bottom: 2rem;">
          <h2 style="color: var(--text-heading); font-size: 1.35rem; margin-bottom: 0.75rem;">8. Common Recovery Failures & Resolutions</h2>
          <div class="table-container">
            <table class="spec-table">
              <thead>
                <tr>
                  <th>Symptom</th>
                  <th>Root Cause</th>
                  <th>Corrective Action</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>TFTP server log shows no file requests</td>
                  <td>Host PC static IP configured on wrong network or firewall blocking UDP port 69</td>
                  <td>Disable Windows Defender Firewall temporarily; verify Ethernet cable is plugged into LAN1</td>
                </tr>
                <tr>
                  <td>Serial terminal outputs garbled ASCII characters</td>
                  <td>Baud rate mismatch or missing ground connection</td>
                  <td>Confirm baud rate is 115200 (or 1500000 for RK3568); confirm adapter GND is firmly bonded to router PCB GND</td>
                </tr>
                <tr>
                  <td>Router loops repeatedly after TFTP transfer</td>
                  <td>Kernel image is incompatible or missing initramfs ramdisk payload</td>
                  <td>Ensure you are flashing the <code>initramfs-recovery.bin</code> image, NOT a standard squashfs sysupgrade image</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Section 9 -->
        <section id="sec-9-safety" class="card" style="margin-bottom: 2rem;">
          <h2 style="color: var(--text-heading); font-size: 1.35rem; margin-bottom: 0.75rem;">9. Electrical Safety & Risk Protocol</h2>
          <div class="callout callout-warning" style="margin-top: 0; margin-bottom: 1.25rem;">
            <strong>ESD & GROUNDING ADVISORY:</strong> Work on a static-dissipative ESD mat with a wrist strap attached to ground before touching exposed router circuitry. High ESD potentials can latch up sensitive transceiver silicon.
          </div>
          <ul style="margin-left: 1.5rem; font-size: 0.88rem; color: var(--text); line-height: 1.8;">
            <li><strong>Voltage Rail Verification:</strong> Router serial logic is strictly <strong>3.3V TTL</strong>. Never connect 5V TTL or RS-232 (+12V/-12V).</li>
            <li><strong>VCC Prohibition:</strong> The VCC pin from your serial adapter must remain completely disconnected. Power the router solely from its own DC power adapter.</li>
            <li><strong>Electrostatic Discharge (ESD):</strong> Work on an anti-static mat and touch a grounded metal chassis before handling open router PCBs.</li>
            <li><strong>Capacitor Discharge:</strong> Wait a minimum of 10 seconds after unplugging the router before attaching or removing serial probes.</li>
          </ul>
        </section>

        <!-- Section 10 -->
        <section id="sec-10-references" class="card">
          <h2 style="color: var(--text-heading); font-size: 1.35rem; margin-bottom: 0.75rem;">10. Primary Citations & Upstream Evidence</h2>
          <ul style="margin-left: 1.5rem; font-size: 0.85rem; color: var(--text-muted); line-height: 1.7;">
            <li>OpenWrt Official Documentation: <a href="https://openwrt.org/docs/guide-user/troubleshooting/generic.flashing.tftp" target="_blank" rel="noopener">Generic TFTP Flashing & Recovery</a></li>
            <li>OpenWrt Upstream Source: <a href="https://git.openwrt.org/?p=openwrt/openwrt.git;a=tree;f=target/linux/mediatek/filogic" target="_blank" rel="noopener">target/linux/mediatek/filogic</a></li>
            <li>MediaTek ATF/FIP Bootloader Specifications: MT7986 / MT7981 Reference U-Boot Implementation</li>
          </ul>
        </section>

        <div class="guide-pagination">
          <a href="../installation/index.html" class="guide-nav-link">
            <span>&larr; Previous Guide</span>
            <strong>Two-Stage Installation</strong>
          </a>
          <a href="../multi-wan/index.html" class="guide-nav-link" style="text-align: right;">
            <span>Next Guide &rarr;</span>
            <strong>Dual-WAN Automatic Failover</strong>
          </a>
        </div>

        {get_contribution_panel("docs/recovery/tftp-and-uart-recovery.md", "Disaster Recovery Guide", rel_root="../..")}
      </article>
    </div>
    """
    desc = "Engineering unbricking guide for OpenWrt routers across 5 tiers: OpenWrt failsafe, OEM Web failsafe, automated TFTP, 3.3V UART serial console, and SPI flash programmers."
    return get_header("Disaster Recovery & Unbricking", rel_root="../..", current_nav="recovery", description=desc, canonical_path="guides/recovery/", json_ld=json_ld) + content + get_footer(rel_root="../..", goatcounter_code=GOATCOUNTER_CODE)

def generate_multiwan_guide():
    content = """
    <div class="breadcrumbs">
      <a href="../../index.html">Home</a> <span>/</span>
      <a href="../recovery/index.html">Guides</a> <span>/</span>
      <strong>Dual-WAN Automatic Failover</strong>
    </div>

    <div class="section-header">
      <div>
        <h1>Dual-WAN Automatic Failover Architecture</h1>
        <p>Wired broadband primary with automated mobile hotspot wireless backup.</p>
      </div>
    </div>

    <div class="callout callout-warning">
      <strong>VERIFICATION STATUS: <code>COMMUNITY_CONFIGURATION — REAL-WORLD VALIDATION PENDING</code></strong><br>
      This architecture and UCI configuration syntax represent a verified community blueprint based on upstream <code>mwan3</code> and <code>travelmate</code> packages. While the configuration logic is sound, full end-to-end real-world physical verification (including simulated fiber severance and AP+STA radio channel concurrency) remains open for community field validation.
    </div>

    <div class="card" style="margin-bottom: 2rem;">
      <h2 style="color: var(--text-heading); font-size: 1.3rem; margin-bottom: 1rem;">Architectural Blueprint</h2>
      <ul style="margin: 0.5rem 0 1rem 1.5rem; font-size: 0.9rem; color: var(--text); line-height: 1.7;">
        <li><strong>Primary WAN (<code>wan</code>)</strong>: Cat6 Ethernet to ISP ONT (Priority 1, metric 10).</li>
        <li><strong>Backup WAN (<code>wwan</code>)</strong>: 5 GHz wireless client station connecting to a smartphone hotspot (Priority 2, metric 20).</li>
        <li><strong>Health Monitor (<code>mwan3</code>)</strong>: Proactive ICMP pings to <code>1.1.1.1</code> and <code>8.8.8.8</code> every 3 seconds.</li>
        <li><strong>Automatic Failover</strong>: 3 missed pings triggers full reroute through wireless hotspot backup.</li>
        <li><strong>Hysteresis Recovery</strong>: 5 consecutive successful pings on primary WAN automatically restores primary routing.</li>
      </ul>
    </div>

    <div class="guide-pagination">
      <a href="../recovery/index.html" class="guide-nav-link">
        <span>&larr; Previous Guide</span>
        <strong>Disaster Recovery & Unbricking</strong>
      </a>
      <a href="../../methodology/index.html" class="guide-nav-link" style="text-align: right;">
        <span>Next Section &rarr;</span>
        <strong>Research Methodology</strong>
      </a>
    </div>

    {get_contribution_panel("docs/networking/multi-wan-failover.md", "Dual-WAN Failover Guide", rel_root="../..")}
    """
    desc = "Dual-WAN automatic failover reference blueprint on OpenWrt with mwan3, travelmate, and hardware status LED automation."
    return get_header("Dual-WAN Automatic Failover", rel_root="../..", current_nav="multi-wan", description=desc, canonical_path="guides/multi-wan/") + content + get_footer(rel_root="../..")

def generate_methodology_page():
    content = """
    <div class="breadcrumbs">
      <a href="../index.html">Home</a> <span>/</span>
      <strong>Research Methodology</strong>
    </div>

    <div class="section-header">
      <div>
        <h1>Hardware Research & Verification Methodology</h1>
        <p>The evidentiary standards and verification taxonomy governing all repository records.</p>
      </div>
    </div>

    <div class="card" style="margin-bottom: 2rem;">
      <h2 style="color: var(--text-heading); font-size: 1.3rem; margin-bottom: 1rem;">Primary Evidentiary Hierarchy</h2>
      <p style="font-size: 0.92rem; color: var(--text); margin-bottom: 1rem;">No device record, chipset specification, or recovery procedure is published without corroboration from primary sources:</p>
      <ol style="margin-left: 1.5rem; font-size: 0.9rem; color: var(--text); line-height: 1.8;">
        <li><strong>Upstream OpenWrt Git Repository:</strong> Device tree DTS files, image makefiles, and Git commit logs.</li>
        <li><strong>Official FCC ID Filings:</strong> Internal teardown photography, RF shielding inspection, and component silkscreen decoding.</li>
        <li><strong>Physical UART Boot Captures:</strong> Reproducible U-Boot console logs, dmesg outputs, and MTD partition tables.</li>
        <li><strong>Vendor GPL Source Tarballs:</strong> Bootloader configurations, kernel trees, and hardware revision errata.</li>
      </ol>
    </div>

    <div class="card">
      <h2 style="color: var(--text-heading); font-size: 1.3rem; margin-bottom: 1rem;">Strict Status Taxonomy</h2>
      <div class="table-container">
        <table class="spec-table">
          <thead>
            <tr><th>Status</th><th>Definition & Evidence Requirement</th></tr>
          </thead>
          <tbody>
            <tr><td><span class="badge badge-success">OFFICIALLY_SUPPORTED</span></td><td>Device is formally merged in upstream OpenWrt Git master or stable releases. Official firmware selector download link exists.</td></tr>
            <tr><td><span class="badge badge-warning">COMMUNITY_VERIFIED</span></td><td>Device boots and runs OpenWrt via functional community build with reproducible boot logs and physical hardware confirmation.</td></tr>
            <tr><td><span class="badge badge-info">PARTIALLY_VERIFIED</span></td><td>Device boots OpenWrt, but major subsystems (e.g. proprietary Broadcom Wi-Fi transceivers) are non-functional due to driver constraints.</td></tr>
            <tr><td><span class="badge badge-danger">UNSUPPORTED</span></td><td>Hardware cannot run OpenWrt due to BootROM signature locks, proprietary bootloader encryption, or missing architecture support.</td></tr>
          </tbody>
        </table>
      </div>
    </div>

    {get_contribution_panel("docs/research-methodology.md", "Research Methodology", rel_root="..")}
    """
    desc = "Primary evidentiary standards and hardware verification taxonomy governing the Global OpenWrt Router Hardware Knowledge Base."
    return get_header("Research Methodology", rel_root="..", current_nav="methodology", description=desc, canonical_path="methodology/") + content + get_footer(rel_root="..")

def generate_about_page():
    content = """
    <div class="breadcrumbs">
      <a href="../index.html">Home</a> <span>/</span>
      <strong>About Project</strong>
    </div>

    <div class="section-header">
      <div>
        <h1>About the OpenWrt Hardware Knowledge Base</h1>
        <p>An independent, global, evidence-based technical reference project.</p>
      </div>
    </div>

    <div class="card" style="margin-bottom: 2rem;">
      <h2 style="color: var(--text-heading); font-size: 1.3rem; margin-bottom: 1rem;">Project Mission</h2>
      <p style="font-size: 0.92rem; color: var(--text); line-height: 1.7; margin-bottom: 1rem;">
        The OpenWrt Router Hardware Knowledge Base was created to provide network engineers, developers, and privacy advocates worldwide with an authoritative, transparent, and machine-readable reference for open-source router hardware.
      </p>
      <p style="font-size: 0.92rem; color: var(--text); line-height: 1.7;">
        Maintained by <strong>Rny0007</strong> and open to international contributions, the project bridges low-level silicon datasheets with production-grade OpenWrt deployment blueprints.
      </p>
    </div>

    <div class="card">
      <h2 style="color: var(--text-heading); font-size: 1.3rem; margin-bottom: 1rem;">Repository Architecture (Dual Repo Pattern)</h2>
      <p style="font-size: 0.92rem; color: var(--text); margin-bottom: 1rem;">
        This project maintains a strict separation of concerns between full source and public website:
      </p>
      <ul style="margin-left: 1.5rem; font-size: 0.9rem; color: var(--text); line-height: 1.8;">
        <li><strong>Repository A (Full Source):</strong> <a href="https://github.com/Rny0007/mt7986-openwrt-router-guide" target="_blank" rel="noopener">Rny0007/mt7986-openwrt-router-guide</a> — The authoritative single source of truth containing raw JSON schemas, device database, chipset profiles, comprehensive documentation, tests, and CI workflows.</li>
        <li><strong>Repository B (Website Only):</strong> <a href="https://github.com/Rny0007/openwrt-router-hardware-explorer" target="_blank" rel="noopener">Rny0007/openwrt-router-hardware-explorer</a> — The deployable, zero-dependency static website compiled automatically by GitHub Actions.</li>
      </ul>
    </div>

    {get_contribution_panel("AGENT.md", "About & Project Governance", rel_root="..")}
    """
    desc = "About the Global OpenWrt Router Hardware Knowledge Base, project stewardship, and dual-repository architecture."
    return get_header("About Project", rel_root="..", current_nav="about", description=desc, canonical_path="about/") + content + get_footer(rel_root="..")

def generate_licensing_page():
    content = """
    <div class="breadcrumbs">
      <a href="../index.html">Home</a> <span>/</span>
      <strong>Licensing & Attribution</strong>
    </div>

    <div class="section-header">
      <div>
        <h1>Licensing, Attributions & Trademarks</h1>
        <p>Open-source licensing terms, third-party disclosures, and trademark policies.</p>
      </div>
    </div>

    <div class="card" style="margin-bottom: 2rem;">
      <h2 style="color: var(--text-heading); font-size: 1.3rem; margin-bottom: 1rem;">Dual-License Framework</h2>
      <div class="table-container">
        <table class="spec-table">
          <thead>
            <tr><th>Asset Type</th><th>License</th><th>Terms</th></tr>
          </thead>
          <tbody>
            <tr><td>Documentation, Schemas & Research Data</td><td><a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener">Creative Commons Attribution 4.0 International (CC BY 4.0)</a></td><td>Free to share, adapt, and build upon with appropriate attribution.</td></tr>
            <tr><td>Code, Build Scripts, Explorer UI & Tools</td><td><a href="https://opensource.org/licenses/MIT" target="_blank" rel="noopener">MIT License</a></td><td>Permissive open-source software license.</td></tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="card">
      <h2 style="color: var(--text-heading); font-size: 1.3rem; margin-bottom: 1rem;">Trademark Notices</h2>
      <p style="font-size: 0.9rem; color: var(--text-muted); line-height: 1.7;">
        All trademarks, product names, logos, and brands cited on this website (including OpenWrt, MediaTek, Filogic, Qualcomm, Broadcom, Realtek, Rockchip, Jio, Arcadyan, ASUS, GL.iNet, TP-Link, Xiaomi, and Ubiquiti) are the property of their respective owners. Their citation is strictly for technical identification, compatibility analysis, and educational reference, and does not imply endorsement or affiliation.
      </p>
    </div>

    {get_contribution_panel("ATTRIBUTION.md", "Licensing & Attribution", rel_root="..")}
    """
    desc = "Licensing policies, Creative Commons attribution, MIT code licenses, and third-party trademark notices for OpenWrt Hardware KB."
    return get_header("Licensing & Attribution", rel_root="..", current_nav="about", description=desc, canonical_path="licensing/") + content + get_footer(rel_root="..")

def generate_contributing_page():
    content = """
    <div class="breadcrumbs">
      <a href="../index.html">Home</a> <span>/</span>
      <strong>Contributor Handbook</strong>
    </div>

    <div class="section-header">
      <div>
        <h1>Contributor Handbook & Submission Guide</h1>
        <p>How to submit new router profiles, verify hardware revisions, and report test outcomes.</p>
      </div>
    </div>

    <div class="card" style="margin-bottom: 2rem;">
      <h2 style="color: var(--text-heading); font-size: 1.3rem; margin-bottom: 1rem;">How to Submit a New Device</h2>
      <ol style="margin-left: 1.5rem; font-size: 0.9rem; color: var(--text); line-height: 1.8;">
        <li>Fork the source repository: <a href="https://github.com/Rny0007/mt7986-openwrt-router-guide" target="_blank" rel="noopener">Rny0007/mt7986-openwrt-router-guide</a>.</li>
        <li>Create a new JSON record under <code>data/devices/&lt;vendor&gt;/&lt;device-slug&gt;.json</code>.</li>
        <li>Ensure all fields validate against <code>data/schemas/device.schema.json</code>.</li>
        <li>Run the local validation suite: <code>python scripts/build-index.py && python tests/run_tests.py</code>.</li>
        <li>Open a pull request citing your primary upstream source URL (OpenWrt commit, ToH link, or FCC ID).</li>
      </ol>
    </div>

    <div class="card">
      <h2 style="color: var(--text-heading); font-size: 1.3rem; margin-bottom: 1rem;">Structured GitHub Issue Templates</h2>
      <p style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 1rem;">You can also submit hardware data directly through our 10 structured issue templates without writing JSON:</p>
      <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
        <a href="https://github.com/Rny0007/mt7986-openwrt-router-guide/issues/new?template=01_new_device_submission.yml" target="_blank" rel="noopener" class="btn btn-sm btn-outline">Submit Device Profile</a>
        <a href="https://github.com/Rny0007/mt7986-openwrt-router-guide/issues/new?template=02_hardware_revision_verification.yml" target="_blank" rel="noopener" class="btn btn-sm btn-outline">Verify Hardware Revision</a>
        <a href="https://github.com/Rny0007/mt7986-openwrt-router-guide/issues/new?template=05_recovery_unbrick_report.yml" target="_blank" rel="noopener" class="btn btn-sm btn-outline">Submit Unbrick Tutorial</a>
      </div>
    </div>

    {get_contribution_panel("docs/contributor-handbook.md", "Contributor Handbook", rel_root="..")}
    """
    desc = "Contributor handbook, JSON schema validation rules, and structured GitHub issue submission guides for OpenWrt hardware."
    return get_header("Contributor Guide", rel_root="..", current_nav="about", description=desc, canonical_path="contributing/") + content + get_footer(rel_root="..")

def generate_404_page():
    content = """
    <div style="text-align: center; padding: 5rem 0;">
      <h1 style="font-size: 4rem; color: var(--primary); font-weight: 800; margin-bottom: 1rem;">404</h1>
      <h2 style="color: var(--text-heading); margin-bottom: 1rem;">Hardware Record Not Found</h2>
      <p style="color: var(--text-muted); max-width: 500px; margin: 0 auto 2rem;">The requested router profile, diagram, or guide may have been moved or updated in our evidentiary taxonomy.</p>
      <div style="display: flex; justify-content: center; gap: 1rem;">
        <a href="index.html" class="btn btn-primary">Return to Homepage</a>
        <a href="explorer/index.html" class="btn btn-outline">Open Hardware Explorer</a>
      </div>
    </div>
    """
    desc = "404 page not found - OpenWrt Router Hardware Knowledge Base"
    return get_header("404 Not Found", description=desc, canonical_path="404.html") + content + get_footer()

def generate_sitemap(devices, chipsets):
    urls = [
        f"{BASE_URL}/",
        f"{BASE_URL}/explorer/",
        f"{BASE_URL}/devices/",
        f"{BASE_URL}/chipsets/",
        f"{BASE_URL}/diagrams/",
        f"{BASE_URL}/guides/installation/",
        f"{BASE_URL}/guides/recovery/",
        f"{BASE_URL}/guides/multi-wan/",
        f"{BASE_URL}/methodology/",
        f"{BASE_URL}/contributing/",
        f"{BASE_URL}/about/",
        f"{BASE_URL}/licensing/"
    ]
    for d in devices:
        urls.append(f"{BASE_URL}/devices/{d['id']}/")
        urls.append(f"{BASE_URL}/guides/install/{d['id']}/")
        urls.append(f"{BASE_URL}/guides/recovery/{d['id']}/")
    for c in chipsets:
        urls.append(f"{BASE_URL}/chipsets/{c['id']}/")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    for u in urls:
        xml_lines.append(f'  <url><loc>{u}</loc><lastmod>{now}</lastmod><changefreq>weekly</changefreq></url>')
    xml_lines.append('</urlset>')
    return "\n".join(xml_lines)

def build_all():
    print(f"Building Global OpenWrt Hardware Knowledge Base Website...")
    devices, chipsets = load_data()
    print(f"Loaded {len(devices)} devices and {len(chipsets)} chipsets.")

    if os.path.exists(SITE_DIR):
        shutil.rmtree(SITE_DIR)
    os.makedirs(SITE_DIR, exist_ok=True)
    os.makedirs(os.path.join(SITE_DIR, "assets", "css"), exist_ok=True)
    os.makedirs(os.path.join(SITE_DIR, "assets", "js"), exist_ok=True)
    os.makedirs(os.path.join(SITE_DIR, "devices"), exist_ok=True)
    os.makedirs(os.path.join(SITE_DIR, "chipsets"), exist_ok=True)
    os.makedirs(os.path.join(SITE_DIR, "explorer"), exist_ok=True)
    os.makedirs(os.path.join(SITE_DIR, "diagrams"), exist_ok=True)
    os.makedirs(os.path.join(SITE_DIR, "guides", "install"), exist_ok=True)
    os.makedirs(os.path.join(SITE_DIR, "guides", "installation"), exist_ok=True)
    os.makedirs(os.path.join(SITE_DIR, "guides", "recovery"), exist_ok=True)
    os.makedirs(os.path.join(SITE_DIR, "guides", "multi-wan"), exist_ok=True)
    os.makedirs(os.path.join(SITE_DIR, "methodology"), exist_ok=True)
    os.makedirs(os.path.join(SITE_DIR, "contributing"), exist_ok=True)
    os.makedirs(os.path.join(SITE_DIR, "about"), exist_ok=True)
    os.makedirs(os.path.join(SITE_DIR, "licensing"), exist_ok=True)

    # Assets
    with open(os.path.join(SITE_DIR, "assets", "css", "style.css"), "w", encoding="utf-8") as fp:
        fp.write(build_css())
    with open(os.path.join(SITE_DIR, "assets", "js", "main.js"), "w", encoding="utf-8") as fp:
        fp.write(build_js())
    with open(os.path.join(SITE_DIR, "assets", "favicon.svg"), "w", encoding="utf-8") as fp:
        fp.write(build_favicon())
    with open(os.path.join(SITE_DIR, "favicon.svg"), "w", encoding="utf-8") as fp:
        fp.write(build_favicon())
    with open(os.path.join(SITE_DIR, "robots.txt"), "w", encoding="utf-8") as fp:
        fp.write(build_robots())
    with open(os.path.join(SITE_DIR, "manifest.webmanifest"), "w", encoding="utf-8") as fp:
        fp.write(build_manifest())
    with open(os.path.join(SITE_DIR, "sitemap.xml"), "w", encoding="utf-8") as fp:
        fp.write(generate_sitemap(devices, chipsets))

    # Copy data index for explorer
    os.makedirs(os.path.join(SITE_DIR, "data"), exist_ok=True)
    shutil.copy2(os.path.join(DATA_DIR, "index.json"), os.path.join(SITE_DIR, "data", "index.json"))

    # Copy explorer with embedded data fallback
    src_explorer = os.path.join(REPO_ROOT, "explorer", "index.html")
    if os.path.exists(src_explorer):
        with open(src_explorer, "r", encoding="utf-8") as fp:
            exp_content = fp.read()
        with open(os.path.join(DATA_DIR, "index.json"), "r", encoding="utf-8") as fp:
            index_json = fp.read()
        embedded_tag = f'<script id="embedded-data" type="application/json">\n{index_json}\n</script>\n  <script>'
        exp_content = exp_content.replace("<script>", embedded_tag, 1)
        with open(os.path.join(SITE_DIR, "explorer", "index.html"), "w", encoding="utf-8") as fp:
            fp.write(exp_content)

    # Core Pages
    with open(os.path.join(SITE_DIR, "index.html"), "w", encoding="utf-8") as fp:
        fp.write(generate_homepage(devices, chipsets))
    with open(os.path.join(SITE_DIR, "devices", "index.html"), "w", encoding="utf-8") as fp:
        fp.write(generate_device_directory(devices))
    with open(os.path.join(SITE_DIR, "chipsets", "index.html"), "w", encoding="utf-8") as fp:
        fp.write(generate_chipset_directory(chipsets))
    with open(os.path.join(SITE_DIR, "diagrams", "index.html"), "w", encoding="utf-8") as fp:
        fp.write(generate_diagrams_page())
    with open(os.path.join(SITE_DIR, "guides", "installation", "index.html"), "w", encoding="utf-8") as fp:
        fp.write(generate_installation_guide())
    with open(os.path.join(SITE_DIR, "guides", "recovery", "index.html"), "w", encoding="utf-8") as fp:
        fp.write(generate_recovery_guide())
    with open(os.path.join(SITE_DIR, "guides", "multi-wan", "index.html"), "w", encoding="utf-8") as fp:
        fp.write(generate_multiwan_guide())
    with open(os.path.join(SITE_DIR, "methodology", "index.html"), "w", encoding="utf-8") as fp:
        fp.write(generate_methodology_page())
    with open(os.path.join(SITE_DIR, "contributing", "index.html"), "w", encoding="utf-8") as fp:
        fp.write(generate_contributing_page())
    with open(os.path.join(SITE_DIR, "about", "index.html"), "w", encoding="utf-8") as fp:
        fp.write(generate_about_page())
    with open(os.path.join(SITE_DIR, "licensing", "index.html"), "w", encoding="utf-8") as fp:
        fp.write(generate_licensing_page())
    with open(os.path.join(SITE_DIR, "404.html"), "w", encoding="utf-8") as fp:
        fp.write(generate_404_page())

    # Static Device Pages & Dedicated Installation and Recovery Guides
    for d in devices:
        dev_id = d["id"]
        dev_dir = os.path.join(SITE_DIR, "devices", dev_id)
        os.makedirs(dev_dir, exist_ok=True)
        with open(os.path.join(dev_dir, "index.html"), "w", encoding="utf-8") as fp:
            fp.write(generate_device_page(d))

        # Device Installation Guide (/guides/install/<dev_id>/)
        inst_dir = os.path.join(SITE_DIR, "guides", "install", dev_id)
        os.makedirs(inst_dir, exist_ok=True)
        with open(os.path.join(inst_dir, "index.html"), "w", encoding="utf-8") as fp:
            fp.write(generate_device_install_guide(d))

        # Device Recovery Guide (/guides/recovery/<dev_id>/)
        rec_dir = os.path.join(SITE_DIR, "guides", "recovery", dev_id)
        os.makedirs(rec_dir, exist_ok=True)
        with open(os.path.join(rec_dir, "index.html"), "w", encoding="utf-8") as fp:
            fp.write(generate_device_recovery_guide(d))

    # Static Chipset Pages
    for c in chipsets:
        chip_dir = os.path.join(SITE_DIR, "chipsets", c["id"])
        os.makedirs(chip_dir, exist_ok=True)
        with open(os.path.join(chip_dir, "index.html"), "w", encoding="utf-8") as fp:
            fp.write(generate_chipset_page(c, devices))

    # Create Repo B README in site/
    repo_b_readme = """# OpenWrt Router Hardware Explorer (Live Website)

This repository hosts the live, public website deployment for the **Global OpenWrt Router Hardware Knowledge Base**:

🌐 **Live Website:** https://rny0007.github.io/openwrt-router-hardware-explorer/

---

## Authoritative Source Code & Hardware Database

This repository contains **compiled static production website output only**.

The complete authoritative source code, raw JSON hardware records, JSON schemas, documentation, and continuous integration test suites are maintained in **Repository A**:

👉 **Source Repository:** [Rny0007/mt7986-openwrt-router-guide](https://github.com/Rny0007/mt7986-openwrt-router-guide)

Please submit all pull requests, hardware submissions, bug reports, and corrections to the source repository.

---

## Licensing
- Documentation & Data: [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
- Web Code & Explorer: [MIT License](https://opensource.org/licenses/MIT)
"""
    with open(os.path.join(SITE_DIR, "README.md"), "w", encoding="utf-8") as fp:
        fp.write(repo_b_readme)

    print(f"[SUCCESS] Website build complete! Generated {len(devices)} device profiles, {len(devices)} install guides, {len(devices)} recovery guides, {len(chipsets)} chipset pages, and full sitemap in site/")

if __name__ == "__main__":
    build_all()
