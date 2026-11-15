# Documentation Style Guide: Formatting, Syntax & Conventions

To ensure readability, accessibility, and consistency across all guides and hardware profiles, follow these guidelines:

---

## 1. Markdown Standards

- Use standard GitHub Flavored Markdown (GFM).
- Keep header hierarchy logical (`# H1` -> `## H2` -> `### H3`). Never skip header levels.
- Code blocks must declare their language explicitly (e.g. ````sh````, ````json````, ````uci````, ````text````).
- Use GitHub-style alerts (`> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, `> [!CAUTION]`) strategically to highlight safety-critical information.

---

## 2. File Naming Conventions

- All documentation and data files must use lowercase kebab-case (e.g. `hardware-identification-guide.md`, `gl-inet-gl-mt6000.json`).
- Never use spaces, underscores, or uppercase characters in documentation URLs.

---

## 3. Network Configuration & Technical Units

- Always use standard decimal prefixes for data rates (e.g. `1000 Mbps`, `2.5 Gbps`) and binary prefixes for storage/RAM (e.g. `512 MB`, `8 GB eMMC`).
- Standardize on OpenWrt UCI syntax for configuration snippets rather than raw `/etc/config` edits where possible.
- In tutorials, default router LAN IP is always `192.168.1.1` (or explicitly noted when using subnet isolation e.g. `192.168.10.1`).
