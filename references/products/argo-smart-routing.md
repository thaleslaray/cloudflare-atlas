# Argo Smart Routing — fastest-path routing to origin

> Detects real-time network congestion/packet loss and routes proxied traffic over the most
> efficient path across Cloudflare's network. A one-click, usage-based **add-on** — no origin changes.

## Contents
- When to use (and when not)
- Enable (dashboard / API)
- How it works
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- Reduce **latency to origin** for dynamic/uncacheable traffic (APIs, real-time, logins, carts).
- Global audience far from your origin — benefits scale with distance and congestion.
- Pairs with **Tiered Cache**: Argo optimizes the Cloudflare↔origin path; Tiered Cache reduces how
  many requests reach origin. Use both for max gain.
- **Not** for: dev/staging (cost control), low-traffic or single-region sites (cost may exceed benefit),
  or purely cacheable/static content (the cache, not the route, is doing the work).
- For IP-layer products (Magic Transit, Cloudflare WAN, Cloudflare for Offices) the analogue is
  **Argo for Packets** — contact your account manager; not a self-serve toggle.

## Enable (dashboard / API)
A zone-level on/off toggle — **requires a billing profile first**.
- **Dashboard:** Traffic → **Argo Smart Routing** → toggle **On** → confirm billing.
- **API:** `PATCH /zones/{zone_id}/argo/smart_routing` with `{"value":"on"}` (or `"off"`).
  Token needs `Zone:Argo Smart Routing:Edit`. Check `GET .../argo/smart_routing` → `editable: true`
  before a PATCH; `editable:false` means billing/plan/permission blocks it.
- **SDK:** `client.argo.smartRouting.edit({ zone_id, value: 'on' })`.
- **Spectrum (TCP/UDP apps):** enable per-app via `argo_smart_routing: true` on the Spectrum app,
  independent of the zone HTTP toggle.

## How it works
- Continuously probes paths between Cloudflare data centers and your origin; picks fastest/most
  available route, failing over automatically when it detects issues.
- Only **proxied (orange-clouded)** traffic is routed and billed — grey-clouded DNS bypasses Argo.
- **Analytics:** Dashboard → Analytics → Performance. Shows Origin Response Time (TTFB with vs.
  without Argo) and a per-data-center Geography map. Detailed view needs **≥500 origin requests
  in 48h**; a negative geo value = that location wouldn't benefit and is routed directly.

## Gotchas
- **Now part of Smart Shield** — Argo Smart Routing is offered under Cloudflare's origin-safeguard
  product, Smart Shield. Existing config keeps working; watch the changelog for migration.
- **Usage-based bill can surprise you** — set up **Usage-Based Billing notifications** (Notifications
  page) before/after enabling.
- **Mitigated traffic is free** — DDoS-/WAF-blocked traffic is excluded from Argo charges.
- **`editable:false`** before PATCH → billing not configured, plan ineligible, or token missing the
  Edit scope. Don't blind-PATCH; it'll fail.
- Static/cached responses see little benefit — Argo helps the dynamic, origin-bound requests.

## Pricing & limits
> ⚠️ Pricing is volatile and shown in the dashboard (Traffic → pricing). **Verify on the live page
> before quoting.** Set billing notifications.

**Cost drivers:** usage-based, charged **per GB of proxied traffic** to/from origin
(historically ~**$0.10/GB** with a small monthly minimum ~$5). DDoS-/WAF-mitigated traffic is
**not** counted. Requires a billing profile to enable. Enterprise customers can **preview** it as a
non-contract service (full access, no metered fees/limits).

**Plan gating (via Smart Shield):** Argo Smart Routing is included in the **Smart Shield + Argo** and
**Smart Shield Advanced** packages. Free/Pro/Business can purchase Smart Shield and Smart Shield + Argo;
Smart Shield Advanced is Enterprise-only. Enterprise has access to all packages.
(`developers.cloudflare.com/smart-shield/` → Plans/Availability + `/smart-shield/configuration/argo/`.)

**Key limits:** analytics needs ≥500 origin requests / 48h · only proxied DNS records count ·
API rate limit ~1200 req / 5 min per token · analytics lag ~1–5 min.

## Going deeper
- Covered by the official `cloudflare` skill (`references/argo-smart-routing/`) — use it for the
  full API surface, SDK/Python examples, Terraform/IaC config, Spectrum patterns, and error handling
  (`api.md`, `configuration.md`, `patterns.md`, `gotchas.md`).
- Smart Shield: `developers.cloudflare.com/smart-shield/` · Tiered Cache:
  `developers.cloudflare.com/cache/how-to/tiered-cache/`.
