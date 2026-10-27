# Speed — measure & improve website/web-app performance

> Zone-level toolkit to **assess** page performance (Observatory: synthetic + real-user tests,
> Lighthouse, Core Web Vitals) and **improve** it via one-click optimizations (image, content/JS,
> protocol). Available on all plans. This is a dashboard/zone feature, not a Worker binding.

## Contents
- When to use (and when not)
- Observatory (measure)
- Optimizations (improve)
- Config & API
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- You have a **website/zone proxied through Cloudflare** and want to measure + improve page load.
- Measure Core Web Vitals (LCP, INP, CLS) and Lighthouse scores — synthetic *and* real-user.
- Get **recommendations**: Observatory maps Lighthouse audits to specific Cloudflare features.
- One-click wins: image optimization (Polish), JS deferral (Rocket Loader), compression, HTTP/3,
  prefetching (Speed Brain), Early Hints.
- **Not** for: code-level Worker profiling (→ Workers observability/tail), backend latency tuning
  (→ Argo Smart Routing, Tiered Cache), or apps not behind Cloudflare's proxy.

## Observatory (measure) — beta
Two data sources feed performance metrics and recommendations:
- **Synthetic tests** (servers simulate a user; consistent, repeatable, any URL in the zone):
  - **Browser test** — loads page in a headless browser, runs Google Lighthouse → score + tips.
  - **Network test** — detailed network/back-end breakdown (wait/load/connect/TLS time, TTFB).
    Two completed network tests can be **compared** side-by-side as histograms.
- **Real User Monitoring (RUM)** — lightweight JS beacon captures real visitor metrics (no cookies/
  `localStorage`). Only RUM yields **INP** (and historically FID). Free plans: RUM on by default
  with **EU traffic excluded**; can opt out. Other plans enable as needed.
- **Recommendations** tab maps audit findings to Cloudflare features + shows estimated savings.
- **Trend / History report** per tested URL tracks metrics over time.

**Metrics:** synthetic + RUM share TTFB, FCP, LCP, CLS. Synthetic-only: TTI, TBT, Speed Index.
RUM-only: INP (requires real interaction).

## Optimizations (improve)
Toggle from **Speed → Settings** (a.k.a. Optimization). Grouped:
- **Image**: **Polish** (lossy/lossless recompress, auto WebP/AVIF; Pro+ — not on Free). Mirage was
  **deprecated on 2025-09-15 and is no longer available** — docs point to native lazy loading +
  responsive images instead. Image Resizing/Transformations live under `images/`.
- **Content / JS**: **Rocket Loader** (defers all JS until after render — async load, preserves
  execution order, improves first-paint; all plans), content **compression** (Gzip/Brotli/Zstandard —
  default *by plan*: Free = Zstandard, Pro/Business = Brotli, Enterprise = Gzip; override with
  Compression Rules), **Cloudflare Fonts** (rewrites Google Fonts to be served from your own zone —
  Google Fonts only), **Early Hints** (all plans; only over HTTP/2 and HTTP/3), **Prefetch URLs**
  (**Enterprise only**), **Speed Brain** (prefetches the likely next navigation via the Speculation
  Rules API; **enabled by default on Free**), Automatic Platform Optimization (APO — WordPress, needs
  the Cloudflare for WordPress plugin), **Shared dictionaries** (RFC 9842, *beta on all plans*,
  **passthrough only**: your origin produces the `dcb`/`dcz` deltas, Cloudflare just forwards and
  varies cache; needs Chrome/Edge ≥130).
- **Protocol**: HTTP/2, **HTTP/3 (QUIC)**, Enhanced HTTP/2 Prioritization, 0-RTT Connection
  Resumption, HTTP/2 to Origin.

**Origin Analytics** (separate Speed tab): edge-derived view of origin response time (p50/p95/p99
vs your timeout), status codes, slow endpoints — agentless. Surfaces whether a problem is origin,
network, or Cloudflare. Reads higher than origin-side tools (it includes DNS/TCP/TLS/round-trip).
**Aggregated Internet Measurement (AIM)**: assess your Internet connection quality.

## Config & API
No `wrangler.jsonc` binding — Speed is configured per **zone** in the dashboard or via the zone
**settings** REST API. Example (toggle Speed Brain):
```bash
curl "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/speed_brain" \
  --request PATCH \
  --header "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  --json '{ "value": "on" }'   # "off" to disable
```
Most toggles map to a `settings/<name>` endpoint (needs `Zone Settings Write`) and the
`cloudflare_zone_settings_override` Terraform resource.

**Observatory is also scriptable** — 10 operations under `/zones/{zone_id}/speed_api/…`, so tests and
schedules do not have to be driven from the dashboard. The URL is a **path parameter**: URL-encode it.
- `GET /speed_api/availabilities` — **remaining quota** + permitted regions/frequencies. Call this
  first; quota is what silently blocks a schedule.
- `GET /speed_api/pages` · `GET|POST|DELETE /speed_api/pages/{url}/tests` · `GET …/tests/{test_id}` —
  tested pages, history, start a test, wipe history, one result.
- `GET /speed_api/pages/{url}/trend` — **Core Web Vitals over time**; this is the endpoint behind a
  "we took it from X to Y" report for a client.
- `GET|POST|DELETE /speed_api/schedule/{url}` — the recurring test.

## Gotchas
- **Rocket Loader can break JS/jQuery** and needs CSP updates; disable + retest if scripts misbehave.
  It also emits non-standard tags that fail strict W3C HTML validation (harmless to visitors).
  **On an ad-traffic site, treat it as hostile to measurement**: it defers and reorders script
  execution, which is exactly what a pixel, a GTM container or a consent script cannot tolerate. If
  conversions start under-reporting after a "performance pass", check this first. Route third-party
  tags through `zaraz.md` and leave Rocket Loader off.
- **Speed Brain** only prefetches **cache-eligible** pages, **never** routes that run a Worker, and
  **never reaches origin** (cache-only) — these are safety guards against unsafe prefetch (e.g. a
  prefetched sign-out URL mutating state). Needs Chromium ≥121; breaks under CSP `strict-dynamic`/
  `nonce-*`; not compatible with `pages.dev`.
- **RUM excludes EU traffic by default** on Free — your RUM sample may under-represent EU users.
- **Observatory test IPs/UAs**: tests come from specific ASNs (15169/132892 for IPv6, 396982 for
  IPv4) with a `CloudflareObservatory` user-agent — allowlist them if you gate by UA/IP.
- **Auto Minify no longer exists** — deprecated 2024-08-05; the only remaining doc is
  "Turn off Auto Minify via API" for zones still carrying the stale setting. Never recommend it;
  minify at build time instead.
- Compression only applies to whitelisted content types + status `200` (and `403`/`404` errors).
  Minimum response size: 48 bytes for Gzip, 50 bytes for Brotli/Zstandard.
- Origin Analytics times look *higher* than Grafana/Datadog — it's the full upstream round trip,
  not just server processing.

## Pricing & limits
> ⚠️ Verify on the live pricing/plans page before quoting — availability is plan-gated and changes.
- **Speed dashboard, Observatory, Origin Analytics, AIM, Rocket Loader, Speed Brain, compression,
  HTTP/2-3**: included on **all plans** (no separate Speed charge). Some optimizations are richer on
  higher plans; **Polish** and **Enhanced HTTP/2 Prioritization** are **Pro+**, **Prefetch URLs** is
  **Enterprise-only**. Mirage no longer exists (removed 2025-09-15).
- **Observatory test quotas (per month):** Pro = 50 one-off + 5 recurring (daily); Business = 100 +
  10; Enterprise = 150 + 15. Recurring cadence and limits may change.
- **The quota table starts at Pro — Free is not listed** (checked 2026-08-17). Do not promise
  scheduled/recurring testing on a free zone without reading `GET /speed_api/availabilities` first.
- Synthetic tests run from **21 regions** (counted 2026-08-17), including **São Paulo** — the one that
  matters for a Brazilian audience, since most free tools test from Virginia. URL must belong to the
  zone under test.

## Going deeper
- No dedicated official `cloudflare` skill ref for `speed` — this file is the primary reference.
- Related skill refs: `images/` (Polish, Transformations), `cache-reserve/`, `argo-smart-routing/`,
  `smart-placement/`, `web-analytics/` (RUM), `observability/` (Worker-level perf).
- For hands-on Core Web Vitals profiling, see the `cloudflare:web-perf` skill (Chrome DevTools MCP).
- Live docs: `developers.cloudflare.com/speed/` · index `…/speed/llms.txt`.
