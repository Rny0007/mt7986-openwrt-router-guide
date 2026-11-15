# First-Time Contributors Guide: Welcome to the Global Router Knowledge Base!

Thank you for your interest in contributing to the **Global OpenWrt Router Hardware Knowledge Base**! This project is maintained by and for open-source networking enthusiasts, system administrators, and embedded Linux engineers worldwide.

Whether you have verified an obscure regional router variant, corrected a typo in a configuration file, or want to contribute a complete hardware teardown, **your help is welcomed and recognized.**

---

## 1. Fast Ways to Contribute (No Coding Required!)

You do not need to be a C developer or Linux kernel maintainer to make high-impact contributions:

- **Verify a Router You Own**: Compare your router's hardware label and OpenWrt version against `data/devices/`. If your hardware matches, submit a [Hardware Verification Report](.github/ISSUE_TEMPLATE/02_hardware_revision_verification.yml).
- **Submit a Missing Device Profile**: Have a working OpenWrt router not listed in our database? Use our [New Device Submission Form](.github/ISSUE_TEMPLATE/01_new_device_submission.yml).
- **Document an Unbrick / Recovery Experience**: If you recovered a soft-bricked router using TFTP or UART, document the exact steps in an [Unbrick Report](.github/ISSUE_TEMPLATE/05_recovery_unbrick_report.yml).
- **Improve Clarity & Documentation**: Fix broken links, clarify ambiguous installation instructions, or suggest diagram improvements via a pull request.
- **Translate Guides**: Help translate our getting-started guides into your native language while preserving technical identifier integrity.

---

## 2. Your First Contribution in 5 Simple Steps

### Step 1: Find an Issue or Task
Look for issues labeled:
- `good-first-issue`: Small, self-contained tasks perfect for beginners.
- `help-wanted`: Hardware profiles or documentation needing community testing.
- `documentation`: Writing, formatting, and markdown link updates.

### Step 2: Fork and Clone the Repository
```sh
# Clone your personal fork
git clone https://github.com/<your-username>/mt7986-openwrt-router-guide.git
cd mt7986-openwrt-router-guide

# Create a focused topic branch
git checkout -b doc/fix-archer-c6-recovery-link
```

### Step 3: Make Your Edits
Follow our [Documentation Style Guide](docs/documentation-style-guide.md):
- Keep filenames in lowercase kebab-case (e.g. `cudy-wr3000-v1.json`).
- If editing device data, make sure every new claim includes an upstream source URL.
- Never include private credentials, Wi-Fi keys, or personal IP addresses.

### Step 4: Validate Your Work Locally
Run our validation script before committing:
```sh
python scripts/build-index.py
```
If all schemas pass, it will output:
`[SUCCESS] All schemas, unique IDs, and source requirements validated successfully!`

### Step 5: Submit Your Pull Request
Push your branch to GitHub and open a Pull Request. Fill out the provided [Pull Request Template](.github/PULL_REQUEST_TEMPLATE.md). Our automated GitHub Actions will automatically check your links, validate your JSON schemas, and ensure everything is clean.

---

## 3. Contributor Recognition

Every contributor who submits a verified device profile, documentation improvement, or hardware test is permanently recognized in our release notes and contributor directory.

Thank you for helping liberate router hardware across the globe!
