# Google tag gateway for advertisers — first-party serving of Google tags

> Serve Google measurement tags (Google Tag Manager / Analytics / Ads) from **your own domain**
> instead of a Google domain, so the tag and its measurement events traverse first-party context —
> recovering ad signal lost to third-party blocking and improving privacy. Free, dashboard-configured,
> for sites already using Cloudflare as CDN.

## Contents
- When to use (and when not)
- How it works
- Configuration
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- You run Google measurement (GTM, GA4, Google Ads conversion tags) and want to **recover signal**
  lost to ad/tracking blockers, ITP, and third-party-cookie restrictions by serving tags first-party.
- Your site is already proxied through Cloudflare (orange-cloud / CDN) — this is a per-zone feature.
- You want a near-zero-effort setup (a few clicks in the Google tag console or the Cloudflare dash),
  not a custom server-side tagging (sGTM) deployment.
- **Not** for: sites not on Cloudflare's CDN; non-Google analytics (this is Google-specific —
  for vendor-neutral tag loading see Cloudflare **Zaraz**); full server-side container logic
  (use Google server-side GTM). It does not replace consent management.

## How it works
Standard setup: the browser requests `gtm.js`/`gtag.js` from a Google domain and posts measurement
events to Google. With the gateway, the **tag loads from `https://your-domain/<measurement-path>/...`**
and measurement events are sent to **your domain**, where Cloudflare forwards them to Google. Because
the requests are first-party to your origin, they survive third-party blocking that would otherwise
drop them. You pick an unused **measurement path** on your site that serves GTM and all subsequent
measurement requests.

## Configuration
No Worker binding, no `wrangler.jsonc`, no public API — it is a **zone-level dashboard/console** toggle.

Two ways to enable:
- **Google Tag Manager** (fastest) — turn on the gateway from Google's tag UI (Google Help Center
  walks through it); it provisions the Cloudflare side.
- **Cloudflare dashboard** — Account → **Tag Management → Google Tag Gateway** → select domain →
  enable *"Turn on and configure Google tag gateway"* → enter your **Google tag ID** and the
  **measurement path** → **Save**.

Required role: Super Administrator, Administrator, or **Zaraz Admin** (account-scoped); or
**Domain Administrator** if using Domain Scoped Roles.

## Gotchas
- **Zone-level, all-or-nothing.** Enabling it on `example.com` applies to **every hostname and
  subdomain** (including custom hostnames). You cannot enable/disable per-subdomain, and
  **Configuration Rules cannot** scope or disable the tag injection.
- **Per-subdomain behavior must go through GTM triggers**, not Cloudflare — e.g. a *Page Hostname
  equals `shop.example.com`* trigger to fire a tag only on that subdomain. One zone-wide gateway
  config + GTM triggers for the per-host logic.
- **Overrides existing GTM.** If a GTM script is already on the page, this first-party tag overrides
  the existing script — verify your container still behaves as expected after enabling.
- **Pick a genuinely unused measurement path** — it is reserved on your site to load GTM and serve
  measurement requests; collisions with a real route will break.
- Requires the site to be served through Cloudflare's CDN; it does not work on grey-clouded/non-proxied hosts.

## Pricing & limits
> ⚠️ Pricing/limits change — verify on the live page (`developers.cloudflare.com/google-tag-gateway/`)
> before quoting.

- **Free.** No usage charge for the gateway.
- Requests routed through the gateway **do not count** toward usage or billing for other Cloudflare
  products (CDN, WAF, Bot Management).
- Configuration granularity is **per zone** (no per-subdomain control — see Gotchas).

## Going deeper
- Cloudflare docs: `developers.cloudflare.com/google-tag-gateway/` · blog: "Google tag gateway for
  advertisers" (the why/how).
- Google's own setup guides: Google Tag Platform "Set up Google tag gateway for advertisers" and the
  Google Help Center articles for GTM-with-Cloudflare and GA-with-Cloudflare.
- Related Cloudflare tooling: **Zaraz** (vendor-neutral third-party tag/loader manager) for
  non-Google or multi-vendor tag management.
