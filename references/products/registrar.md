# Registrar — buy & manage domains at cost

> Register, transfer, and renew domains through Cloudflare at **wholesale price** — you pay only what
> the registry + ICANN charge, **no markup, no surprise fees**. Free WHOIS redaction and one-click DNSSEC.

## Contents
- When to use (and when not)
- Prerequisites & restrictions
- Core flows (register / transfer / renew)
- Registrar API (beta)
- Account management
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- You want to **register** a new domain, **transfer** an existing one into Cloudflare, or **renew** —
  at registry cost with no markup (the differentiator vs GoDaddy/Namecheap/etc.).
- You already use (or will use) **Cloudflare DNS** for the zone — Registrar requires it.
- You want free WHOIS redaction, one-click DNSSEC, and (Enterprise) registry-lock protection.
- **Not** for: changing nameservers to a third-party DNS provider (not allowed while registered here);
  internationalized/Unicode domain names (IDNs / `xn--` punycode) — unsupported; domains you only want
  to *use* on Cloudflare without moving the registration (just add the zone to DNS instead).

## Prerequisites & restrictions
- A Cloudflare account with a **verified registrant email** (ICANN requirement) + a valid payment method.
- Domain must use **Cloudflare authoritative DNS (full setup)** — you cannot point NS elsewhere.
- ICANN holds the domain (swaps to parking nameservers) if the registrant email is unverified/expired;
  nameservers auto-restore once verified.
- ASCII characters only for contact data; no IDNs.

## Core flows
- **Register** (Dash → *Register domains*): search → Purchase → pick term (1–10 yr, varies by TLD) →
  contacts (Registrant/Admin/Tech/Billing) → pay → Complete purchase. Auto-renew **on** by default in the dash.
- **Transfer in** (Dash): first add the domain to Cloudflare as an active zone, then enter the auth/EPP
  code. Active work ~30 min; typically 3–5 business days, total up to **10 days** (some TLDs like `.mx` at the top of
  that range). Most transfers add a **1-year extension** (not `.uk` / `.nz`, and not if the term is already 10 yr).
- **Renew**: auto-renew first attempt ~**30 days** before expiry, retried until the day before expiry;
  or manually renew up to 10 years anytime (Dash → *Manage domains* → Manage → Renew/Extend).

## Registrar API (beta)
Search / availability / registration are scriptable (and exposed via Cloudflare MCP). Needs an API token
with **Registrar write**, a billing profile, and a default registrant contact + accepted Domain Registration Agreement.
- `GET  /accounts/{account_id}/registrar/domain-search?q=...&limit=N` — fast, **cached**, discovery only.
- `POST /accounts/{account_id}/registrar/domain-check` — queries the registry live; real-time price +
  `registrable`; up to 20 domains/request. **Call this immediately before registering.** Non-registrable
  responses carry a `reason` (`domain_unavailable`, `domain_premium`, `extension_not_supported_via_api`,
  `extension_not_supported`, `extension_disallows_registration`) and a `tier` (`standard` | `premium`) —
  if `tier: premium`, do **not** call `POST /registrations`; premium isn't supported by the API.
- `POST /accounts/{account_id}/registrar/registrations` — body `{"domain_name":"..."}`; uses default
  contact + payment method. API defaults: `auto_renew=false`, `privacy_mode=redaction` (if TLD supports).
  **Billable and non-refundable** once it completes.
- **Registration is asynchronous** — poll `GET …/registrations/{domain_name}/registration-status`
  (and `…/update-status` after a `PATCH`) until it settles. Do not treat the `POST` response as done.
- `GET /accounts/{account_id}/registrar/extensions[/{extension}]` — which TLDs the **API** supports.
  This is a **subset of the dashboard's**: a domain Cloudflare sells on the site can still come back
  `extension_not_supported_via_api`. Check before building a purchase flow on it.
- **Beta gaps that bite later, not at first call:** no renewal, no transfer, no contact update, no
  premium domains through the API. Those stay dashboard-only, so an automated buying flow still needs
  a human for the lifecycle.

## Account management
- **WHOIS redaction** — free, on by default where the registry permits; redacts name/email/address.
  State/province + country stay public (ICANN). Cloudflare WHOIS/RDAP: `rdap.cloudflare.com`.
- **DNSSEC** — one-click activation (`get-started/enable-dnssec/`). Transferring in: disable DNSSEC/DS
  records at the *old* registrar **before** changing nameservers, or resolution fails
  (`get-started/transfer-domain-to-cloudflare/`).
- **Inter-account transfer** — move a registration between Cloudflare accounts (domain >10 days old, DNSSEC off,
  target confirms within 5 days); loses all zone config, transfer-locked 30 days after.
- **Transfer out** — unlock + get auth code (blocked within 60 days of registration/transfer/contact change).
- **Custom Domain Protection** — Enterprise only: registry lock, out-of-band auth, no dashboard interface
  (anti-hijacking for high-profile domains; contact your account team).

## Gotchas
- **No `.br` / `.com.br`.** Brazilian domains are registered exclusively through registro.br; no
  foreign registrar can sell them. For a Brazilian client the registration stays there and you only
  point the nameservers at Cloudflare — Registrar is for the `.com`/`.dev`/`.app` side of the estate.
- **DNS lock-in:** while registered with Cloudflare you must use Cloudflare nameservers — no third-party DNS.
- **60-day locks (ICANN):** can't transfer out within 60 days of registration/transfer, or after changing
  registrant name/org/email (even redacted — you can opt out via *Do not apply 60 day transfer lock* when
  approving the Change of Registrant, which applies to all TLDs including `.uk`). Transferring *in* requires
  the domain be ≥60 days old — that transfer rule does **not** apply to `.uk`.
- **API `auto_renew` defaults to `false`** (opposite of the dashboard, which defaults on) — set it explicitly.
- **Auto-renew is best-effort:** can fail (billing, registry downtime). Check your domains; you'll get email + 3 retries.
- **Disable auto-renew ≥30 days before expiry** if you want to drop a domain — and disable it before deleting.
- **Restore fee:** a lapsed/redemption domain (EPP `redemptionPeriod`, ~40–70 days past expiry) costs a restore
  fee (varies by TLD) **on top of** renewal; non-refundable. `.uk` has no redemption/restore — just renew, up to
  90 days after expiry, no restore fee.
- **Renewed then transferred?** A transfer within **45 days** of a renewal is charged but the registry adds **no**
  extra year (applies at every registrar) — wait 45 days, or claim a refund from the old registrar.
- **`.us` / `.uk`** have extra requirements — `.us` needs a US nexus and the registry **forbids WHOIS redaction**;
  `.uk` and `.nz` transfers have **no fee** and add **no** extra year.

## Pricing & limits
> ⚠️ Pricing is **at-cost and varies by TLD** — verify on the live page before quoting:
> `cloudflare.com/products/registrar/` and the real-time `domain-check` API.

**Model:** **no markup** — you pay exactly the registry + ICANN fee for registration and renewal. No
account/plan fee (available on all plans). Example real-time API prices (illustrative, USD): `.com` ≈ $8.57,
`.dev` ≈ $10.11, `.app` ≈ $11.00 — actual prices change; always read the `domain-check` response.
Restore (redemption) and some country-code TLDs have separate fees.

**Key limits:** 400+ supported TLDs (see `cloudflare.com/tld-policies/`) · term up to **10 years** (some TLDs
fewer) · no IDN/Unicode support · `domain-check` accepts ≤20 domains/request · registrations non-refundable.

## Going deeper
- No dedicated official `cloudflare` skill ref for Registrar — this file is the primary reference.
- Full REST API: Cloudflare API docs → `/api/resources/registrar` (Search / Check / Registrations).
- Rendered docs: `developers.cloudflare.com/registrar/` (get-started, account-options, troubleshooting, faq).
- Related: **DNS** (required authoritative provider) · **Fundamentals → Manage domains** (move between accounts for non-Registrar domains).
