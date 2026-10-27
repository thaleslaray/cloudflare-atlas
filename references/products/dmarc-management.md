# DMARC Management — stop email spoofing, monitor DMARC reports

> Track every source sending email from your domain and review aggregate DMARC reports to see whether
> messages pass SPF, DKIM, and DMARC — so you can spot unauthorized senders and stop impersonation.
> Dashboard-driven, free on all plans, requires Cloudflare DNS. **Currently beta.**

## Contents
- When to use (and when not)
- The three records (SPF / DKIM / DMARC)
- How it works
- Setup (dashboard)
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- You want to **set up SPF / DKIM / DMARC** records for a domain and have Cloudflare guide the config.
- You want Cloudflare to **collect and parse aggregate DMARC (`rua`) reports** for you and show pass/fail
  stats per sending source — instead of manually reading raw XML DMARC reports.
- You're hardening a domain against **spoofing / phishing / brand impersonation**.
- **Not** for: scanning/filtering inbound email for threats → that's **Email Security** (Cloudflare One).
  DMARC Management is about *outbound authentication* of mail claiming to be from your domain.
- **Not** for: forensic (`ruf`) per-message failure reports — this handles **aggregate** (`rua`) data.
- **Requires**: the domain uses **Cloudflare DNS** and is an **apex domain** (`example.com`, not
  `blog.example.com`); subdomain-setup zones are not supported.

## The three records (all DNS TXT records)
- **SPF** (Sender Policy Framework) — lists the IPs/domains authorized to send mail for your domain.
- **DKIM** (DomainKeys Identified Mail) — cryptographic signature authenticating the sender domain and
  proving the message wasn't altered in transit.
- **DMARC** — ties SPF + DKIM together and tells receiving servers what to do on failure (`p=none` /
  `quarantine` / `reject`), and where to send aggregate reports (the `rua` tag).

## How it works
On enable, Cloudflare adds a **`rua` entry pointing at a Cloudflare email address** to your DMARC TXT
record (or creates a DMARC record if none exists). Receiving mail servers send aggregate reports to that
address; Cloudflare ingests and parses them, then surfaces per-source pass/fail stats in the dashboard.
- `rua` = "Reporting URI for Aggregate data" — the destination for aggregate DMARC reports.
- First report can take **up to 24 hours** to appear after enabling.

## Setup (dashboard — no Worker binding / API config)
This is a dashboard product; there is no `wrangler.jsonc` binding.
1. Dashboard → select account + domain → **Email** → **DMARC Management**.
2. **Enable DMARC Management.** Cloudflare scans for a DMARC record:
   - none found → it offers to add one (**Add**);
   - found → it appends its `rua` entry (**Next**).
3. To manage records: **Email record overview** → **View records** → set up SPF / DKIM / DMARC.
4. View results under **DMARC Management**: volume graph (up to 30-day window), **View reports** by date,
   **Top 10 sources**, and **View all** to list/filter every sending source and drill into each.

## Gotchas
- **Apex only.** Won't work on subdomains or subdomain-setup zones.
- **Requires Cloudflare DNS** for the zone.
- **SPF + external CNAME:** if a CNAME in your zone points to an external domain, DMARC Management
  **won't modify the SPF record** — changing it could invalidate your policy since Cloudflare can't
  update the external DNS. Manage those SPF updates at the external provider.
- **SPF 10-lookup limit (RFC 7208):** each `include:` / `mx` reference costs a DNS lookup; >10 makes
  receivers treat SPF as a permanent error and may reject/flag mail. DMARC Management warns when an SPF
  record exceeds the limit (Edit the SPF record to see it) — flatten/remove entries to fix.
- **Roll out DMARC gradually:** start at `p=none` (monitor only), watch reports, then move to
  `quarantine` / `reject` once legitimate senders pass — going straight to `reject` can drop real mail.
- **Beta:** feature is labeled beta; expect changes.

## Pricing & limits
> ⚠️ Verify on the live pricing page before quoting — pricing/availability can change.
- **Free** — available on **all plans** to any customer using Cloudflare DNS. No per-report/usage cost
  stated in the docs.
- **Limits:** apex domains only · aggregate (`rua`) reports only · report graph window **up to 30 days**
  · **Top 10** sources highlighted (full list via **View all**) · first report up to **24h** to appear ·
  SPF capped at **10 DNS lookups** per check (RFC 7208).

## Going deeper
- No official `cloudflare` skill reference for this product — this file is the primary reference.
- Official docs: `developers.cloudflare.com/dmarc-management/` (overview, enable, security-records,
  dns-lookup-limits, statistics).
- Record concepts: Cloudflare Learning Center pages for SPF / DKIM / DMARC records.
- Inbound threat scanning is a different product → **Email Security** under Cloudflare One.
