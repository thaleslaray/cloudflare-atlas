# Web Analytics — privacy-first RUM (no cookies)

> Free, privacy-first web analytics (real-user monitoring) collected by a JS **beacon** — page
> views, visits, referrers, Core Web Vitals — with **no cookies, no fingerprinting, no PII**.
> Works on any site (no DNS change or Cloudflare proxy required).

## Contents
- When to use (and when not)
- Setup (the beacon)
- What it measures
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- **Client-side / RUM analytics** for a website: page views, visits, referrers, top paths,
  device/browser/country, and **Core Web Vitals** (LCP, INP, CLS — TTFB/FCP also reported, but they
  are not Core Web Vitals) as real visitors see them.
- You want it **free**, cookie-free, and GDPR-friendly — no consent banner needed for it alone.
- Works on **any host** (Pages, Vercel, your own server) — no DNS change or proxy required.
- **Not** for: custom/business events or arbitrary metrics → use **Analytics Engine** (write
  data points from a Worker) or **Workers Analytics / GraphQL API**. No custom events here.
- **Not** for: real-time data, user-level tracking, funnels, or session replay.
- **Not** for **campaign attribution**: query strings are deliberately never logged, so **UTM
  parameters do not exist here** (Cloudflare says "not yet"). Paid-traffic reporting has to come from
  GA4 or the ad platform — this is the single reason it cannot replace GA4 for a traffic operation.

**Site management _is_ scriptable** (13 REST operations, below); it is the *metric data* that has no
REST export — read that through the GraphQL Analytics API (`rum*` datasets, honour `sampleInterval`).

## Setup (the beacon)
There is no `wrangler.jsonc` binding — it's a `<script>` tag, not a Worker resource.

1. Dashboard → **Web Analytics** → **Add a site** → enter hostname → copy the JS snippet.
2. Paste it **before `</body>`** on every HTML page you want measured:
```html
<script type="module" defer src="https://static.cloudflareinsights.com/beacon.min.js"
        data-cf-beacon='{"token": "YOUR_SITE_TOKEN", "spa": true}'></script>
```
- **`spa: true`** is critical for React/Vue/Next.js — client-side route changes ("soft
  navigations") are counted. Default-on; set `false` to disable. Since **2026-08-21** the beacon
  prefers Chrome's **Soft Navigation API** (the only path that yields **LCP** on soft navigations)
  and falls back to the **Navigation API / History API** on Safari, Firefox and older Chromium
  (`navigationType` = `soft-navigation` vs `routing-apis`; the fallback has no LCP, other CWV present).
  **Hash routers (`#/path`) are not supported** — use `BrowserRouter`, not `HashRouter`.
- **Tag managers (GTM):** pass options via query string instead of `data-cf-beacon`, e.g.
  `beacon.min.js?token=$TOKEN&spa=false`. Manual embeds should carry `type="module"` (auto-injection
  adds it) so the script is skipped by long-EOL browsers such as IE11 (changelog 2026-07-13).
- **Proxied sites (orange-cloud):** enable **automatic setup** in the dashboard — Cloudflare injects
  the beacon on every page; no code change. Reports to your own `/cdn-cgi/rum`. **Pages** projects
  get one-click enable under **Metrics** (injected on next deploy).
- **Same apex = same token:** one token covers all subdomains of the same apex (postfix match).

## Site & rule API (`/accounts/{account_id}/rum/…`)
```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/rum/site_info" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" -H "Content-Type: application/json" \
  -d '{ "host": "exemplo.com.br", "auto_install": true }'   # → returns the site_tag for the snippet
```
- `POST|GET|PUT|DELETE /rum/site_info[/{site_id}]` — CRUD a tracked site.
- `GET /rum/site_info/list` · `/rum/site_info/site_tag/list` · `/rum/site_info/zone_tag/list` — enumerate.
- `GET /rum/site_info/validate/{hostname}` — validate a hostname before adding it.
- `GET|POST /rum/v2/{ruleset_id}/rules` · `POST|PUT|DELETE /rum/v2/{ruleset_id}/rule[/{rule_id}]` —
  which paths get the beacon (paid plans only — see the rules limit below).

## What it measures
- **High-level:** Visits (referer host ≠ your hostname), Page views (HTML 200s), Page load time.
- **Core Web Vitals** (Google UX metrics), reported when the tab first becomes hidden after load.
  Docs: "currently only supported in Chromium browsers, with Safari and Firefox coming soon".
- **Dimensions** to filter/group: Country, Host, Path, Referer, Device type, Browser, OS, Site,
  Navigation type, Exclude Bots. Data from the browser `performance` Navigation Timing API.

## Gotchas
- **Ad-blockers block the beacon** (Brave, uBlock, DuckDuckGo…) → JS-based counts undercount. Edge
  analytics (proxied traffic, Pro+) can't be blocked — use those for unblockable numbers.
- **CSP:** allow `script-src https://static.cloudflareinsights.com` and the beacon endpoint in
  `connect-src` (`'self'` for auto-injection, `cloudflareinsights.com` for manual embedding).
- **Auto-injection silently fails** if origin sends `Cache-Control: public, no-transform` (proxy
  can't rewrite the body) — install the beacon manually instead.
- **One beacon per page** — "since only one JS snippet can be rendered and used per page, you cannot
  have multiple snippets on the same page"; the extra one does not render (fix of 2021-05-28).
- **CORS error** = dashboard hostname ≠ actual hostname; matched by postfix (`example.com` allows
  `www.example.com`, not `example.com.br`). A `Referer`/`Origin` header is required.
- **No data?** Wait a few minutes (docs: "may take a few minutes"; no exact delay is published),
  verify token, check `beacon.min.js` isn't blocked.
- **Not for Workers subrequests** — RUM runs only on the initial client request.
- **Sampling:** unsampled for 7 days, then aggregated to ~10%; queries apply dynamic ABR sampling.

## Pricing & limits
> ⚠️ Pricing/limits change — verify on the live docs before quoting.

- **Free** on **all plans**, no per-event cost. The Limits page caps only **sites** and **rules** —
  no page-view limit is published. (Advanced edge HTTP analytics need Pro/Business/Enterprise.)
- **Data retention:** "you can access data for the previous six months". Not real-time; the docs
  publish no ingestion-delay figure (the earlier "~5–10 min" had no source).
- **Site limits:** non-proxied **10 sites** (soft, raisable via support); proxied **no limit**.
  The dashboard aggregates at most **1,000 sites in parallel** — beyond that, filter or use GraphQL.
- **Rules** (proxied only, control which paths get the snippet): Free **0**, Pro **5**,
  Business **20**, Enterprise **100**.

## Going deeper
- Covered by the official `cloudflare` skill (`references/web-analytics/`) — use it for
  framework-specific beacon snippets (React/Next/Vue/Nuxt/Gatsby), CSP/GDPR patterns, and
  troubleshooting. This file is the lean overview.
- Custom metrics instead of page views → see `products/analytics.md` (GraphQL Analytics API +
  Workers Analytics Engine).
- Exact endpoints with required parameters: `references/api/web-analytics.md` (13 operations, sliced
  from the OpenAPI spec — they live under the `rum` root, which is why no slice claimed them before
  2026-08-17). Request/response **bodies** are still not mirrored: verify shapes against
  `/api/resources/rum`.
