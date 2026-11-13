# Contributing to MT7986 OpenWrt Router Guide

We welcome independent contributions, hardware test verifications, and documentation enhancements from the open-source community.

## Contribution Guidelines

1. **Accuracy & Verification**:
   - Explicitly state the exact router model, hardware revision, bootloader type, and OpenWrt version tested.
   - Differentiate verified hardware findings from unverified or theoretical assumptions.

2. **Security & Privacy (Mandatory)**:
   - Never submit pull requests or issues containing real passwords, private keys, router serial numbers, personal MAC addresses, or ISP credentials.
   - Use generic placeholders (such as `<YOUR_WIFI_PASSWORD>` or `192.168.1.1`).

3. **Style & Structure**:
   - Write in clear, structured technical English.
   - Include copy-pasteable command snippets with the execution environment clearly identified (e.g. `Router SSH` vs `Local Terminal`).
   - Use standard GitHub Flavored Markdown and link to official upstream OpenWrt sources.

4. **Pull Request Process**:
   - Fork the repository and create a feature branch (`git checkout -b feat/device-profile`).
   - Ensure all documentation links are functional and relative.
   - Open a pull request against `main` describing your test methodology and hardware verification.
