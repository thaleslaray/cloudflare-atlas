# Automatic Platform Optimization (APO) — edge-cache a whole WordPress site

> Serve your **entire WordPress site** (including dynamic HTML) from Cloudflare's edge network for
> fast, consistent TTFB. A dashboard/plugin feature — **no Workers binding or code**. WordPress-specific.

## Contents
- When to use (and when not)
- How it works
- Setup
- Verify it's working
- Controlling the cache (Page/Cache Rules, query params, cookies)
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- You run a **WordPress** site and want full-page edge caching of HTML (not just static assets),
  driven by the official **Cloudflare for WordPress** plugin.
- You want automatic invalidation: edit a post in WP → Cloudflare purges the edge within ~30s, so
  visitors never see stale content. Logged-in/admin users automatically bypass the cache.
- Also caches third-party scripts and proxies Google Fonts to cut origin round-trips.
- **Not** for: non-WordPress sites (use [Cache Rules](https://developers.cloudflare.com/cache/) /
  `Cache Everything` directly), **multisite** WordPress (unsupported), or fine-grained edge logic
  (→ build your own caching in Workers).

## How it works
APO is built on Cloudflare Workers internally: it intelligently caches dynamic HTML at the edge so
the whole page is served from cache instead of the origin. Default behavior once enabled:
- HTML cached for **30 days**, invalidated within **~30 seconds** on content change (via the plugin).
- `stale-if-error` behavior is built in (you don't need the directive).
- Requests with cookies prefixed `wp-`, `wordpress`, `comment_`, `woocommerce_`, `edd_`, etc.
  bypass cache (logged-in / cart / commerce sessions stay dynamic).

## Setup
APO is **enabled from the Cloudflare for WordPress plugin**, not `wrangler`. There is no binding/config.
1. Point your domain's **nameservers** at Cloudflare and confirm DNS records resolve.
2. **Free plan:** Dashboard → **Speed → Settings** → **Content Optimization** → *Automatic Platform
   Optimization for WordPress* → **Purchase**. **Pro plan or higher:** APO is included.
3. In WordPress, install + activate the **Cloudflare** plugin (Plugins → Add new → search "Cloudflare").
4. Create an API token in Cloudflare (use the **WordPress** token template), paste it into the plugin's
   Settings, **Apply Recommended Cloudflare Settings**, then toggle **Automatic Platform Optimization** On.

> Use plugin **v4.4.0+** for current features (cache-by-device-type, subdomain support). Older versions
> (< 3.8.2) may go undetected on the dashboard.

## Verify it's working
Three response headers must be present on the homepage (send `accept: text/html`):
```
curl -svo /dev/null -A "CF" 'https://example.com/' -H 'accept: text/html' 2>&1 \
  | grep -i 'cf-cache-status\|cf-edge-cache\|cf-apo-via'
# cf-cache-status: HIT
# cf-apo-via: cache            (tcache once warm / plugin-integrated)
# cf-edge-cache: cache, platform=wordpress
```
`cf-edge-cache: cache,platform=wordpress` confirms the WP plugin is installed and enabled.

## Controlling the cache
- **Cache Rules** (preferred over Page Rules) — use *Bypass cache* to exclude non-WordPress paths.
- **Page Rules** still work: `Bypass` (→ `cf-apo-via: origin,page-rules`), `Edge Cache TTL`
  (override the 30-day default — useful for pages issuing CAPTCHAs/nonces), `Browser Cache TTL`,
  `Cache Everything` (caches *all* query strings — but auto-purge then won't clean query-string URLs).
- **`CDN-Cache-Control` / `Cloudflare-CDN-Cache-Control`** headers give per-response TTL control without rules.
- **Query parameters:** any query string bypasses cache by default, *except* a fixed marketing allowlist
  (`ref`, `utm_*`, `fbclid`, `gclid`, `_ga`, `mc_cid`, `mkt_tok`, …) which are still served from cache.
  Adding a param to the allowlist requires a Cloudflare Community request.
- **Cache by device type:** opt-in; sends `CF-Device-Type: mobile|tablet|desktop` to the origin and
  caches a variant per device (matches `User-Agent`). Toggling it invalidates the cache.
- **Subdomain / subdirectory:** APO runs on the apex by default; v4.4.0+ supports subdomains (enabling a
  subdomain auto-disables the apex unless you re-enable it). To run APO on only part of a site, bypass
  the rest with response header **`cf-edge-cache: no-cache`** (set via a Worker) — preferred over a
  Bypass Cache Rule, which also disables static-asset caching.

## Gotchas
- **WordPress only**, and **not** multisite installs.
- **Don't stack caching plugins.** Disable WP Rocket / W3 Total Cache / similar when first enabling APO,
  clear their server cache, then re-test — combining them often causes stale or unexpected results.
- **Stale content?** Purge the Cloudflare cache after enabling APO.
- **`cf-cache-status: BYPASS`/`DYNAMIC` in tools but `HIT` in browser** is normal: DevTools sends
  `Cache-Control: no-cache`, and cURL must include `accept: text/html` to get a HIT.
- **Origin Cache-Control is ignored** for edge caching (but passed through to the client).
- **Font URL transform** is skipped if a `Content-Security-Policy` header lacks `unsafe-inline`
  (style-src/default-src) and `self` (font-src/default-src).
- **Cloudflare Fonts does not operate while APO is enabled** — APO already optimizes Google Fonts in a similar way.
- Worker subrequests from APO may show up in zone logs (e.g. Logpush) — expected.
- **Not compatible** with Enterprise subdomain setups where `www` is in a different zone than the apex.

## Pricing & limits
> ⚠️ Pricing changes — verify on the live page before quoting.

- **Pro, Business, Enterprise plans:** APO is **included**.
- **Free plan:** APO is a **paid add-on** — purchase it from Speed → Settings → Content Optimization (a small flat monthly
  fee historically ~$5/month; **confirm the current price in-dashboard before quoting**).
- **Limits:** WordPress only; **no multisite**; default edge TTL 30 days / ~30s invalidation;
  `Bypass Cache on Cookie` page rule is **Business/Enterprise only**.

## Going deeper
- **No dedicated official `cloudflare` skill ref** for APO — this file is the primary reference.
- Full docs: `developers.cloudflare.com/automatic-platform-optimization/` (rendered copy under
  `raw/docs-oficiais/pages/automatic-platform-optimization/`).
- Related: general Cache / Cache Rules (`references/products/` cache docs), Workers (for the
  `cf-edge-cache: no-cache` bypass snippet).
