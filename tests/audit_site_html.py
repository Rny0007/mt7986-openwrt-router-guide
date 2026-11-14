import os
import re
from html.parser import HTMLParser

SITE_DIR = "C:\\Users\\mrrny\\Desktop\\mt7986-openwrt-router-guide\\site"

class PageAuditor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.titles = []
        self.meta_descriptions = []
        self.canonicals = []
        self.h1s = []
        self.links = []
        self.in_title = False
        self.in_h1 = False
        self.current_h1 = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            if attrs_dict.get("name") == "description":
                self.meta_descriptions.append(attrs_dict.get("content", ""))
        elif tag == "link":
            if attrs_dict.get("rel") == "canonical":
                self.canonicals.append(attrs_dict.get("href", ""))
        elif tag == "h1":
            self.in_h1 = True
            self.current_h1 = ""
        elif tag == "a":
            href = attrs_dict.get("href")
            if href:
                self.links.append(href)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "h1":
            self.in_h1 = False
            self.h1s.append(self.current_h1.strip())

    def handle_data(self, data):
        if self.in_title:
            self.titles.append(data.strip())
        elif self.in_h1:
            self.current_h1 += data

audit_data = {}
all_descriptions = {}

for root, _, files in os.walk(SITE_DIR):
    for f in files:
        if f.endswith(".html"):
            fpath = os.path.join(root, f)
            rel_path = os.path.relpath(fpath, SITE_DIR).replace("\\", "/")
            with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
                html = fp.read()
            auditor = PageAuditor()
            auditor.feed(html)
            
            desc = auditor.meta_descriptions[0] if auditor.meta_descriptions else ""
            if desc:
                all_descriptions.setdefault(desc, []).append(rel_path)

            audit_data[rel_path] = {
                "title": auditor.titles[0] if auditor.titles else "",
                "description": desc,
                "canonical": auditor.canonicals[0] if auditor.canonicals else "",
                "h1_count": len(auditor.h1s),
                "h1_text": auditor.h1s,
                "links": auditor.links
            }

# Identify Issues
issues = {
    "duplicate_descriptions": {d: pages for d, pages in all_descriptions.items() if len(pages) > 1},
    "missing_canonicals": [p for p, data in audit_data.items() if not data["canonical"]],
    "h1_issues": {p: data["h1_count"] for p, data in audit_data.items() if data["h1_count"] != 1},
    "mixed_url_types": []
}

# Check for mixed clean URLs and index.html in links
for p, data in audit_data.items():
    index_links = [l for l in data["links"] if "index.html" in l]
    clean_links = [l for l in data["links"] if l.endswith("/") or (not l.endswith(".html") and not l.startswith("http") and not l.startswith("#"))]
    if index_links and clean_links:
        issues["mixed_url_types"].append(p)

print("TOTAL HTML PAGES AUDITED:", len(audit_data))
print("MISSING CANONICALS:", len(issues["missing_canonicals"]))
print("PAGES WITH DUPLICATE DESCRIPTIONS:", sum(len(pages) for pages in issues["duplicate_descriptions"].values()))
print("H1 COUNT ISSUES (not exactly 1 H1):", len(issues["h1_issues"]))

import json
with open("C:\\Users\\mrrny\\Desktop\\mt7986-openwrt-router-guide\\tests\\site-wide-audit.json", "w", encoding="utf-8") as out:
    json.dump({
        "total_pages": len(audit_data),
        "issues": issues,
        "sample_pages": {k: audit_data[k] for k in list(audit_data.keys())[:5]}
    }, out, indent=2)
