# Smart Shield — one-click origin protection & performance bundle

> Opt-in bundle of origin-protection and caching features that **reduce requests and connections**
> reaching your origin. Enabled from the dashboard in a few clicks (Speed → Smart Shield). Packages
> bundle Smart Tiered Cache, connection reuse, Argo, Cache Reserve, and more by plan tier.

## Contents
- When to use (and when not)
- What's in each package
- Setup & config
- Key concepts
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- You want a **guided, one-click** way to shield your origin and cut its load — no rule-writing.
- Origin is a bottleneck: traffic spikes, connection exhaustion, high egress, or geographically
  distant visitors. Smart Shield reduces both origin **requests** (via tiered caching) and
  **connections** (via connection reuse).
- You'd otherwise enable Tiered Cache / Argo / Cache Reserve / Health Checks individually — Smart
  Shield packages them and surfaces results in **Observatory**.
- **Requires proxied DNS** (orange-cloud). DNS-only records bypass Cloudflare's proxy, so Smart
  Shield does not apply to them.
- **Not** a WAF/DDoS/bot product (→ `waf`, `ddos-protection`, `bots`) — it protects against origin *load* and
  exposure, not application-layer attacks. **Not** for non-proxied/TCP-only setups.

## What's in each package
Choose a package in the dashboard; availability depends on your plan.

| Feature | Smart Shield (base) | + Argo | Advanced |
|---|:--:|:--:|:--:|
| **Smart Tiered Cache** (auto upper-tier per origin) | ✓ | ✓ | ✓ |
| **Connection reuse** (batches requests onto shared conns, ~30% fewer) | ✓ | ✓ | ✓ |
| **Argo Smart Routing** (fastest network path → lower TTFB) | | ✓ | ✓ |
| **Regional Tiered Cache** (regional hub before upper-tier) | | | ✓ |
| **Cache Reserve** (persistent cache on R2, 2 TB incl.) | | | ✓ |

- **Base** and **+ Argo** are purchasable on Free / Pro / Business / Enterprise.
- **Advanced** is **Enterprise-only** (contact Enterprise Sales).
- **Health Checks** (origin availability monitoring) — available to **Pro/Business/Enterprise** on
  all packages.
- **Dedicated CDN Egress IPs** (formerly *Aegis*) — **Enterprise** add-on; reserved egress IPs so you
  can firewall your origin to a small allowlist. Contact your account team.
- **Regional Tiered Cache** is included with Enterprise plans regardless of package.

## Setup & config
Mostly dashboard-driven, no `wrangler` binding:
1. Dashboard → select domain → **Speed → Smart Shield**.
2. (Optional) review packages → **Get started for free** or pick a package → **Continue** (guided flow).
3. Monitor origin performance & cache effectiveness in **Observatory**.

**Dedicated CDN Egress IPs** (Enterprise) are configured via the Edit Zone Settings API using setting
ID `aegis` — allowlist the pool IPs on your origin *before* linking, or traffic will fail:
```bash
curl "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/aegis" \
  --request PATCH --header "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  --json '{"id":"aegis","value":{"enabled":true,"pool_id":"<EGRESS_POOL_ID>"}}'
```

## Key concepts
- **Smart Tiered Cache** — auto-selects the single lowest-latency upper-tier data center per origin;
  only upper-tiers contact your origin on a cache miss. No config. For cloud-hosted origins (AWS/GCP/
  Azure/Oracle) behind anycast, set a **cloud region hint** so it can locate your origin.
- **Connection reuse / coalescing** — multiple requests share one TCP connection (HTTP/2 coalescing
  even spans hostnames that resolve to the same IP and share a TLS cert). ~30% fewer origin connections.
- **Cache Reserve** — persistent cache layer on R2; serves as the ultimate upper-tier so assets stay
  cached far longer, shielding origin egress. Assets must be cacheable, TTL ≥ 10h, and have a
  `Content-Length` header.
- **Argo Smart Routing** — for dynamic (non-cacheable) traffic, routes around congestion; measured by
  origin TTFB improvement.

## Gotchas
- **Proxied DNS required** — DNS-only (grey-cloud) records are not routed through Smart Shield.
- **Changing origin IP/DNS with Smart Tiered Cache on** can reassign upper-tiers → temporary spike in
  cache `MISS` as cache refills. Switching origin behind anycast cripples it unless you set a region hint.
- **Cache Reserve eligibility is strict:** TTL ≥ 10h + `Content-Length`. Resized image-transformation
  variants are *not* eligible (only originals). Range requests, `Vary for images`, and zone-linked R2
  public buckets are not supported; bypassed under O2O (SaaS) setup.
- **Cache Reserve purge:** purge-by-URL purges instantly & free; purge by tag/host/prefix/everything
  only forces revalidation and assets keep incurring storage cost until TTL expires.
- **Dedicated CDN Egress IPs:** allowlist pool IPs *before* linking (else outage). Not in the China
  Network. Worker `connect()` (raw TCP) does **not** use them; `fetch()` to origin does. Each IP
  supports 40,000 concurrent connections *per origin IP:port*.

## Pricing & limits
> ⚠️ Smart Shield is a **bundle of existing paid features** with no standalone published price sheet;
> cost depends on the package tier and the underlying features. **Verify on the live pricing/plan
> pages and your account before quoting.**

**Cost drivers:**
- **Package tier** — base / +Argo / Advanced; +Argo and Advanced are paid upgrades.
- **Argo Smart Routing** — historically usage-based (per-GB) on top — confirm live.
- **Cache Reserve** — built on **R2**, so R2-style storage + Class A (write) / Class B (read)
  operations apply; **Advanced includes 2 TB** of Cache Reserve storage. Purges are free.
- **Dedicated CDN Egress IPs** — Enterprise add-on (account-team priced).
- A free base tier exists ("Get started for free"); Smart Tiered Cache + connection reuse are the
  no-extra-config core.

**Key limits:** Cache Reserve file limits = R2 limits (and standard CDN cache size limits still apply —
oversized assets re-fetch and incur Cache Reserve ops more often). Each Dedicated CDN Egress IP =
40,000 concurrent conns per origin IP:port. Health Checks require Pro+.

## Going deeper
- No dedicated official `cloudflare` skill ref for Smart Shield — this file is the primary summary.
- Underlying features have their own docs: Cache/Tiered Cache (`cache`), R2 (see `r2.md`, powers Cache
  Reserve), Argo, Health Checks, BYOIP.
- Live docs: `developers.cloudflare.com/smart-shield/` · network diagram & `get-started` for the
  package matrix · `llms.txt` index for full page list.
- Dedicated CDN Egress IPs = former **Aegis**; IPs-utilization via GraphQL schema
  `aegisIpUtilizationAdaptiveGroups`.
