# Cache / CDN — cache content across Cloudflare's network

> Store copies of content in Cloudflare's global edge data centers, close to users, to cut origin
> load and latency. Default cache + **Cache Rules** + Tiered Cache + Cache Reserve + Workers Cache API.

## Contents
- When to use (and when not)
- Default cache behavior
- Cache Rules (the main control surface)
- Cache-Control & CDN-Cache-Control
- CF-Cache-Status values
- Tiered Cache & Cache Reserve
- Purge vs invalidate
- Workers Cache API
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- Cache static **and** dynamic content at the edge to reduce origin requests + latency. On all plans.
- **Cache Rules** — declaratively choose what's cacheable, edge/browser TTL, and the cache key.
- **Tiered Cache** — hierarchy of upper/lower tiers → higher hit ratio, fewer origin connections.
- **Cache Reserve** — persistent R2-backed storage for long-tail content (30-day retention).
- **Workers Cache API** — fine-grained per-request cache read/write from a Worker.
- **Not** for: app-managed key-value (→ kv), object storage (→ r2), DB queries (→ d1/hyperdrive).
  Range-request/video-seeking workloads don't benefit from Cache Reserve (no HTTP 206 support).

## Default cache behavior
- Cloudflare caches **by file extension, not MIME type**. HTML/JSON are **not** cached by default
  (robots.txt is). To cache them, write a Cache Rule ("cache everything").
- Does **not** cache when: `Cache-Control: private|no-store|no-cache|max-age=0`, a `Set-Cookie`
  header is present, or method ≠ `GET`. Caches when `public` + `max-age>0` or `Expires` in future.
- Default Edge TTL when no `Cache-Control`/`Expires`: 200/206/301 → 120m, 302/303 → 20m,
  404/410 → 3m; all other codes uncached.
- **Request collapsing**: concurrent misses for the same asset in one data center → only the first
  hits origin (cache lock), the rest wait and are served the same response.

## Cache Rules (the main control surface)
Live under **Caching → Cache Rules** (NOT under Rules). Built on the Ruleset Engine — match on fields
(`http.request.full_uri`, `http.host`, `http.request.uri.path.extension`, cookies, headers…) and set:
- **Cache eligibility**: Bypass cache, or Eligible for cache.
- **Edge TTL** (`edge_ttl`): `respect_origin` / `override_origin` / `bypass_by_default`, plus
  per-status-code TTL (`status_code_ttl`).
- **Browser TTL** (`browser_ttl`): respect / override / bypass — only modifies `Cache-Control`.
- **Cache Key**: custom key (query-string handling, headers, cookies, device type, cache deception
  armor) to control how entries are shared/separated across requests.
- **Vary** (2026-07): honor the origin `Vary` response header so one URL caches multiple versions — the
  listed request headers join the cache key. Per-header action: `normalize` / `passthrough` / `bypass`
  (`Vary: *` still bypasses cache).
- Other actions: Origin Cache Control (Enterprise), serve-stale, cache-tags.

Create via dashboard, **API**, or Terraform. Availability/plan caps: Free 10 · Pro 25 · Business 50 ·
Enterprise 300 rules. Requires the zone's DNS records to be **proxied** (orange-cloud). Use
**Cloudflare Trace** to see which rule fires for a URL.
```jsonc
// API action_parameters
{ "cache": true,
  "edge_ttl": { "mode": "respect_origin",
    "status_code_ttl": [ { "status_code_range": { "to": 299 }, "value": 86400 } ] },
  "browser_ttl": { "mode": "override_origin", "default": 1000 } }
```

## Cache-Control & CDN-Cache-Control
- **`Cache-Control`** (origin) directives drive default caching: cacheability (`public`/`private`/
  `no-store`), expiration (`max-age`, `s-maxage` — shared-cache only, browsers ignore), revalidation
  (`must-revalidate`, `stale-while-revalidate`, `stale-if-error`), `immutable`, `no-transform`.
- **`CDN-Cache-Control`** / **`Cloudflare-CDN-Cache-Control`** let the origin set CDN TTL separately
  from browser TTL. `Cloudflare-CDN-Cache-Control` is most specific (CF-only, not proxied downstream).
- A Cache Response Rule's `set_cache_control` action takes precedence over origin CDN-CC headers.
- `no-cache` ≠ `no-store`: `no-cache` = store but revalidate first; `no-store` = never store
  (disables BFCache). CF caches whichever TTL is higher: Browser Cache TTL or `max-age`.

## CF-Cache-Status values
`HIT` (from cache) · `MISS` (not cached, from origin) · `EXPIRED` · `STALE` (expired, origin
unreachable) · `REVALIDATED` (origin confirmed unchanged, synchronous path) · `UPDATING` (served
stale during async `stale-while-revalidate`) · `BYPASS` (origin/Origin-CC said don't cache) ·
`DYNAMIC` (not eligible, no rule says to cache) · `NONE/UNKNOWN` (Worker/WAF/redirect responded
before cache). `stale-while-revalidate` is now fully async → first request after expiry gets stale +
`UPDATING` and revalidation runs in the background.

## Tiered Cache & Cache Reserve
- **Tiered Cache**: lower-tier (near user) asks an upper-tier before going to origin; only upper-tier
  contacts origin. Smart Tiered Cache auto-picks the best upper tier (set a cloud region hint for
  AWS/GCP/Azure/Oracle origins). `cache.put` (Workers Cache API) is **not** compatible with tiered cache.
- **Cache Reserve**: persistent R2-backed ultimate upper tier; default 30-day retention extended on
  access. Requires a paid plan; **designed for use with** Tiered Cache (not a hard requirement — the
  dashboard warns, and without it storage-op costs are higher). **Eligibility (ALL):** cacheable, TTL ≥ 10h (36000s),
  `Content-Length` present, no `Set-Cookie`, `Vary` not `*`, not an image transformation variant,
  not a range request, not O2O. Since 2026-09-28 **every** purge type forces a Reserve miss (see below).

## Purge vs invalidate
- **Purge** (`purge_cache`): content removed → next request is a full origin fetch. Since 2026-09-28
  tag/hostname/prefix/everything purges also force a **Cache Reserve miss** (they used to revalidate):
  the re-write is a billed Class A op, and old objects keep billing storage until replaced/expired.
- **Invalidate** (`POST /zones/{zone_id}/invalidate_cache`, "soft purge", 2026-09-28): same selectors;
  marks stale → next request revalidates; an origin `304` reuses the copy. Needs origin `ETag` or
  `Last-Modified`; **Cache Purge** permission; counts toward purge rate limits. Can serve stale on origin
  `5xx`/unreachable even without `stale-if-error` (`stale-if-error=0` prevents). Not for Workers Cache.

## Workers Cache API
`caches.default` (single global cache obj) or `caches.open('name')`. `cache.match(req)` /
`cache.put(req, res)` / `cache.delete(req)`. Honors `Cache-Control`, `Cache-Tag`, `ETag`, `Expires`,
`Last-Modified` on the put response. `Set-Cookie` responses are never cached (strip it or set
`Cache-Control: private=Set-Cookie`). Cache contents are **per-data-center** (not replicated). Only
works on custom domains / Pages Functions — no effect in the dashboard editor or Playground.
`stale-while-revalidate` / `stale-if-error` are **not** supported via `cache.match`/`cache.put`.

## Gotchas
- `BYPASS`/`DYNAMIC` usually means `Set-Cookie`, a no-cache directive, or no rule made it eligible.
- A `Bypass cache` Cache Rule may report `DYNAMIC` (not an explicit bypass status) in the header.
- `s-maxage` disables `stale-while-revalidate` (RFC 9111 `proxy-revalidate` semantics).
- Always Online makes CF ignore `stale-while-revalidate` / `stale-if-error`.
- Cache Reserve fetches **uncompressed** from origin (no `Accept-Encoding: gzip`) → higher origin
  egress than the normal CDN; and silently skips `Vary: Accept` images.

## Pricing & limits
> ⚠️ Pricing changes — verify on the live page (`developers.cloudflare.com/cache/`,
> `.../advanced-configuration/cache-reserve/`) before quoting.

- **Cache + Cache Rules + Tiered Cache: free** on all plans (Tiered Cache now part of Smart Shield).
- **Cache Reserve** is usage-based (paid plan; `Smart Shield Advanced` includes 2 TB —
  developers.cloudflare.com/smart-shield/configuration/cache-reserve/):
  Storage **$0.015 / GB-month** · Class A ops (writes) **$4.50 / M** · Class B ops (reads)
  **$0.36 / M**. A miss ≈ 1 Class A + 1 Class B; a hit ≈ 1 Class B; assets >1 GB incur more ops.
- **Limits:** max cacheable file size **512 MB** (Free/Pro/Business), **5 GB** Enterprise (raisable).
  Cache Reserve file limits = R2 limits. (Cache Rules caps: see Cache Rules above.)

## Going deeper
- **Cache Reserve** is covered by the official `cloudflare` skill (`references/cache-reserve/`) —
  use it for full enable/config, API, SDK/Terraform, cost-optimization patterns, and gotchas.
- Cache Rules deep-dives: `pages/cache/how-to/cache-rules/` (settings, order, API, Terraform).
- Cache-Control semantics: `pages/cache/concepts/cache-control/` + `cdn-cache-control/`.
- Workers integration: `pages/workers/runtime-apis/cache/` + `reference/how-the-cache-works/`.
