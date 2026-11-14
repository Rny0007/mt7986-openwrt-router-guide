# Contributor Handbook: Community Workflows, Standards & Roles

This handbook details the operational procedures, review standards, and governance roles for maintaining the Global OpenWrt Router Hardware Knowledge Base.

---

## 1. The Contributor Lifecycle

```text
Community Submission (Issue / PR)
  ↓
Automated CI Validation (JSON Schema, Link Check, ID Uniqueness)
  ↓
Maintainer / Peer Review (Verifying Upstream Source URLs & Sanitization)
  ↓
Merge to Main & Automated Index Rebuild
  ↓
Contributor Recognition & Release Notes Update
```

---

## 2. Standards for Adding New Hardware Records

When creating or modifying a device record in `data/devices/<vendor>/<device-id>.json`:

1. **Schema Compliance**: The record MUST validate against `data/schemas/device.schema.json`.
2. **Upstream Source Requirement**: At least one primary source URL must be included (e.g. OpenWrt Git commit, official firmware selector URL, or upstream device tree).
3. **Evidence-Based Support Status**:
   - Only devices merged into upstream OpenWrt master or release branches may use `OFFICIALLY_SUPPORTED`.
   - Third-party forks or custom builds must be labeled `COMMUNITY_VERIFIED` or `EXPERIMENTAL`.
4. **Sanitization Protocol**: Verify that no MAC addresses, serial numbers, private keys, or passwords appear in command output or documentation.

---

## 3. Reviewer Checklist for Pull Requests

Maintainers and peer reviewers verify:
- [ ] Automated schema check (`python scripts/build-index.py`) passes without errors.
- [ ] No duplicate `id` exists across the repository.
- [ ] Source URLs resolve and point to legitimate upstream technical resources.
- [ ] Markdown links follow relative file paths and anchor conventions.
- [ ] Risk levels and recovery methods are accurately described.
