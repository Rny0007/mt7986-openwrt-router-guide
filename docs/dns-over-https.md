# DNS-over-HTTPS (DoH) & Encrypted Resolvers

This guide details the security principles, provider options, and operational advantages of deploying DNS-over-HTTPS (DoH) on OpenWrt routers.

---

## 1. Why Plaintext DNS is a Privacy Risk

Standard DNS operates over unencrypted UDP on port 53. In an unencrypted architecture:
- **ISP Snooping**: Internet Service Providers and intermediary networks can log every domain requested by your devices.
- **DNS Spoofing & Manipulation**: Unauthenticated plaintext responses can be forged or redirected to malicious IP addresses.
- **SNI / Censorship Interception**: Network censors inspect plaintext queries to enforce domain-level blocking.

By encapsulating DNS lookups in standard HTTPS (port 443) with TLS encryption, DNS-over-HTTPS renders query payloads invisible to intermediate observers.

---

## 2. Recommended Encrypted DoH Endpoints

| Provider | Primary URL | Secondary URL | Privacy Policy & Features |
| :--- | :--- | :--- | :--- |
| **Cloudflare** | `https://1.1.1.1/dns-query` | `https://1.0.0.1/dns-query` | Ultra-low latency, globally distributed Anycast network, zero logging policy. |
| **Quad9** | `https://9.9.9.9/dns-query` | `https://149.112.112.112/dns-query` | Swiss-based non-profit, built-in threat intelligence blocking malware and phishing. |
| **Mullvad** | `https://dns.mullvad.net/dns-query` | — | Strict zero-logs audit, optional content filtering profiles. |

---

## 3. Fallback Upstream Configuration

In mission-critical networks, configure resilient multi-provider upstream resolvers. If one provider experiences transit degradation, AdGuard Home automatically routes queries through secondary encrypted endpoints:

```text
https://1.1.1.1/dns-query
https://1.0.0.1/dns-query
https://149.112.112.112/dns-query
```

Set **Upstream mode** in AdGuard Home to **Parallel requests** or **Fastest IP address** to minimize end-to-end lookup latency.

---

## 4. Verification & Leak Testing

From a connected client machine:
1. Visit [Cloudflare Security Check](https://one.one.one.one/help) or [DNSLeakTest.com](https://www.dnsleaktest.com).
2. Verify that **Using DNS over HTTPS (DoH)** is reported as **Yes**.
3. Verify that all detected DNS resolver IPs belong to your chosen privacy provider rather than your local ISP.
