# Security Audit & Anti-Scraping Architecture: "काम मिलेगा" (Kaam Milega)

This document details the cybersecurity controls, anti-scraping defenses, zero-PII leak proofs, and penetration resistance mechanisms implemented in the platform.

---

## 1. Zero-PII Leak Architecture

| Data Point | Public API Status | Internal Handling |
|---|---|---|
| Full Phone Number | **NEVER Exposed** in search or list endpoints | Obfuscated with Base64/Salt, revealed only upon rate-limited intent |
| Public ID | Random opaque hash (e.g. `w_8f3a91`) | Autoincrement integer primary keys remain internal only |
| Exact Address | Fuzzed to Village / Tehsil level | No live GPS or street addresses displayed |
| Aadhaar / Government ID | **Zero Collection** | Verification handled via local Panchayat / peer endorsements |

---

## 2. Anti-Scraping & Anti-Harvesting Defense

1. **Tokenized Contact Gateway**: Contact buttons generate single-use, 15-minute ephemeral tokens.
2. **Sliding-Window Rate Limiting**:
   - Max 5 contact reveals per 10 minutes per IP.
   - Max 6 OTP requests per 10 minutes per IP.
   - Exceeding the threshold triggers `HTTP 429 Too Many Requests`.
3. **Honeypot Trap Fields**: Hidden input traps (`website_url`, `bot_check`) detect headless scrapers and immediately flag or poison scraper data.
4. **Search Engine Shield**: Global `X-Robots-Tag: noindex, nofollow, noarchive, nosnippet` and `robots.txt` disallow crawlers from scraping worker profiles.

---

## 3. Hardened Security Headers

* **Content-Security-Policy (CSP)**: `default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self'; frame-ancestors 'none';`
* **X-Content-Type-Options**: `nosniff`
* **X-Frame-Options**: `DENY`
* **Strict-Transport-Security**: `max-age=31536000; includeSubDomains`
* **Referrer-Policy**: `no-referrer`
* **X-XSS-Protection**: `1; mode=block`
* **Permissions-Policy**: `geolocation=(self), microphone=(), camera=(self)`

---

## 4. Injection & Vulnerability Defenses

* **SQL Injection (SQLi)**: 100% prepared parameterized SQL queries using SQLite3 drivers. Zero dynamic string concatenation.
* **Cross-Site Scripting (XSS)**: Inputs sanitized and HTML-escaped using Python `html.escape()` and regex filters.
* **Insecure Direct Object References (IDOR)**: Profile modifications and deletions require session token validation.
* **Information Disclosure**: Generic error payloads prevent server stack traces or database schema disclosures.
