# Security Center — unified security posture, ASM & threat intel

> Account-level dashboard that unifies your Cloudflare security products, attack-surface mapping,
> and global threat intelligence. Find misconfigurations, see what's exposed, and investigate any
> IP/domain/URL — all from one place. It's a console + APIs, **not** a Worker binding.

## Contents
- When to use (and when not)
- Surfaces (main features)
- Threat Intelligence APIs
- Access & roles
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- You want a **centralized security dashboard**: posture review, attack-surface management (ASM),
  threat intel / investigation across the whole account.
- **Security Insights** — automated scans of your Cloudflare config (DNS, SSL/TLS, WAF, Access) that
  flag misconfigurations/vulnerabilities by severity and link each finding to the setting to fix.
- **Investigate** — look up any IP, domain, hostname, URL, or ASN for category, country, passive
  DNS, and threat data (also surfaces WAF analytics for your zones).
- **Brand Protection** — catch typosquatting / homoglyph / service-concatenation impersonation
  domains (beta).
- Programmatic threat-intel lookups via the **Threat Intelligence (Intel) APIs**.
- **Not** for: enforcing security (that's WAF, Bots, Access, Gateway — Security Center points you
  there but doesn't block); it has no Workers binding and runs at the **account**, not zone, level.

## Surfaces (main features)
- **Security Insights** — config scanner; findings with severity + remediation links. Scans run
  automatically; on-demand scans available on all plans (see frequency below).
- **Infrastructure** — asset inventory: domains, IP addresses, DNS records Cloudflare detects.
  Filter, export PDF, and manage your `security.txt` file here.
- **Investigate** — threat-intel lookup for IP / domain / URL / ASN; passive DNS; URL scanner;
  each search returns an equivalent API `curl`.
- **Security Reports** (beta) — visibility into requests blocked or challenged by HTTP DDoS Protection,
  WAF, and Bot Management.
- **Brand Protection** (beta) — domain-search + logo-search queries for impersonation monitoring.
- **Threat Intelligence (Cloudforce One)** — separate section, not one of the Main features: Threat
  Events, Priority Intelligence Requirements (PIRs), Requests for Information (RFIs).
  **Requires a Cloudforce One subscription.**

## Threat Intelligence APIs
Account-scoped REST endpoints (all count against the monthly Intel quota — see limits). Use an API
token with the appropriate Intel/Cloudforce One **Edit** permission.
```
# Domain intelligence (category, resolves-to, content categories)
curl "https://api.cloudflare.com/client/v4/accounts/{account_id}/intel/domain?domain=example.com" \
  -H "Authorization: Bearer <API_TOKEN>"

# IP intelligence (geo, ASN, threat categories)
curl ".../accounts/{account_id}/intel/ip?ipv4=1.1.1.1"  -H "Authorization: Bearer <API_TOKEN>"
```
Other endpoints: ASN intelligence, Domain History, Passive DNS by IP, WHOIS, Phishing/URL info
(`brand-protection/url-info`), Miscategorization (request a category change), Custom Indicator
Feed download, Open Port Scanning (Magic Transit / BYOIP; closed beta), Threat Events, PIRs/RFIs.
**Custom Indicator Feeds** — partner/govt threat feeds (e.g. US Treasury Feed 14, UK NCSC Feed 24,
Cloudforce One Public Feed 34); provider/subscriber model, contact your account team to enable.

## Access & roles
- No `wrangler.jsonc` binding — Security Center is dashboard + REST API only.
- **Administrator Read Only** role **cannot** access Security Center at all.
- Investigate's advanced intel (IP/domain search, passive DNS) needs Super Admin, Administrator,
  Brand Protection, or Cloudforce One Admin role; basic URL scanning is open to all users.
- Starting/stopping scans and managing issues requires **Super Admin** with edit permissions.
- Brand Protection: Super Admin, Admin, Brand Protection (custom role), or Cloudforce One.

## Gotchas
- **Account-level, not zone-level** — covers all zones on the account; not configured per-zone.
- **Manual scans gated:** only accounts with ≥1 Business/Enterprise zone (or Teams Standard/
  Enterprise) can trigger a manual scan. Automatic scans run on all plans.
- **Quota is shared & sneaky:** Investigate, Brand Protection, and other products (e.g. client-side
  security) all consume the **same monthly Intel API quota** — 100 calls/month on Free–Business.
- **Several pieces are beta or gated:** Brand Protection & Security Reports are beta; Cloudforce One
  (Threat Events/PIRs/RFIs) and Custom Indicator Feeds need a subscription / account-team setup.
- Investigate ≠ enforcement: a "malicious" verdict doesn't block anything — wire it into WAF/Gateway.

## Pricing & limits
> ⚠️ Pricing/limits change — verify on the live docs (`developers.cloudflare.com/security-center/`)
> before quoting. Security Center itself is included on **all plans**; the volume gates are below.

**Cost drivers:** Security Center is bundled (no per-use charge for the dashboard/scans). Paid tiers
unlock higher **Intel API quotas** and **URL-scan limits**; Cloudforce One is a separate subscription.

**Scan frequency (Security Insights):** Free every 7 days · Pro/Business every 3 days · Enterprise
daily. On-demand available on all plans.

**Intel API calls / month:** Free/Pro/Business **100** · Enterprise **2,500** · Cloudforce One Core
**10,000** · Cloudforce One Premier **50,000**. (DDoS Botnet Threat Feed API is exempt.)

**URL scan limits (Investigate):** Free/Radar 5,000 public/mo, no unlisted, 1 scan/10s, last-50
history · Self-serve 5,000 public + 500 unlisted/mo, 30-day history · Enterprise 10,000 + 5,000,
12/s, 12-mo history · Cloudforce One 75,000 + 20,000, 12/s, unlimited history.

## Going deeper
- No official `cloudflare` skill ref exists for this product — this file is the primary reference.
- Full Intel API schemas: `developers.cloudflare.com/api/resources/intel/` (and `brand_protection`,
  `cloudforce_one`). Security Insights internals: `developers.cloudflare.com/security/security-insights/`.
- Enforcement lives elsewhere: see `waf.md`, `bots.md`, `cloudflare-one` (Gateway/Access) — Security
  Center finds the problem, those products fix it.
