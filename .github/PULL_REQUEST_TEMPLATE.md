## Pull Request Description

### Type of Change
- [ ] New device profile (`data/devices/`)
- [ ] Chipset profile update (`data/chipsets/`)
- [ ] Hardware specification correction
- [ ] Installation / recovery documentation
- [ ] GitHub Actions / tooling improvement
- [ ] Bug fix / typo correction

---

### Verification & Quality Checklist

Before submitting, please confirm:
- [ ] All new device/chipset JSON files validate against their respective schemas.
- [ ] Ran `python scripts/build-index.py` locally and verified that `data/index.json` and `data/validation-report.json` built cleanly with zero errors.
- [ ] Added verifiable upstream source citations for any new claims or specifications.
- [ ] Checked for and confirmed NO duplicate device IDs.
- [ ] Sanitized all logs, command outputs, and configuration snippets (NO private keys, Wi-Fi passwords, personal MACs, or public IPs).
- [ ] Followed the [Documentation Style Guide](docs/documentation-style-guide.md).
