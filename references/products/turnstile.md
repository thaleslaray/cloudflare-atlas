# Turnstile — smart CAPTCHA alternative

> Verify visitors are human with a CAPTCHA-free, privacy-preserving challenge. A widget on the
> client gets a token; your server validates it via **siteverify**. Works on any site — no need to
> proxy traffic through Cloudflare.

## Contents
- When to use (and when not)
- Config (no Worker binding)
- Widget (client) + siteverify (server) flow
- Spin — assisted setup + `wrangler turnstile`
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- Bot protection on **forms, logins, signups, password resets** without CAPTCHA friction.
- You want a drop-in challenge that runs invisibly (no image puzzles) and is WCAG 2.2 AA compliant.
- **Works off Cloudflare** — embed on any host; traffic doesn't have to go through Cloudflare's CDN.
- Pairs with: Workers (siteverify backend), WAF/Bots (deeper edge mitigation), Pages (Turnstile plugin).
- **Not** for: rate-limiting (→ WAF rate limiting), authn/authz (it proves "human", not "who"),
  blocking automated API clients that never load a browser (→ Bots / WAF).

## Config (no Worker binding)
Turnstile has **no `wrangler.jsonc` binding** — it's two keys from the dashboard (one widget = one pair):
- **Site key** — public, goes in client HTML (`data-sitekey`). Safe to expose.
- **Secret key** — server-only. Store as a Worker secret, never in client code or `vars`:
  ```sh
  echo "$SECRET" | npx wrangler secret put TURNSTILE_SECRET_KEY
  ```
**Widget types:** `managed` (default, shows checkbox only when risk warrants) · `non-interactive`
(invisible, auto) · `invisible` (hidden, triggered via `execute`). Free plan: up to 20 widgets,
10 hostnames each.

**Test keys** (work on localhost + any domain; never ship to prod): site `1x00000000000000000000AA`
(always passes), `2x00000000000000000000AB` (always blocks); secret `1x0000000000000000000000000000000AA`.

## Widget (client) + siteverify (server) flow
1. **Client** loads `https://challenges.cloudflare.com/turnstile/v0/api.js` and renders a widget
   (implicit `<div class="cf-turnstile" data-sitekey="...">` inside the form, or explicit
   `turnstile.render(el, { sitekey, callback })`). On success it injects a hidden field
   `cf-turnstile-response` (the token).
2. **Server** reads that token and POSTs it to siteverify with the **secret**:
   ```js
   const r = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify({
       secret: env.TURNSTILE_SECRET_KEY,
       response: token,                                  // cf-turnstile-response
       remoteip: request.headers.get('CF-Connecting-IP') // optional but recommended
     })
   });
   const { success } = await r.json();   // also: challenge_ts, hostname, action, cdata, error-codes
   if (!success) return new Response('Verification failed', { status: 403 });
   ```
Client API: `render` → widget id; `reset` / `remove` / `getResponse(id)` / `isExpired(id)` / `execute`.

## Spin — assisted setup + `wrangler turnstile`
<!-- GA date removed: absent from the docs and the changelog; Spin page last updated 2026-07-23 -->
Spin creates the widget for you and hands back sitekey, secret, and a prompt that wires the widget +
canonical siteverify into the backend you already have. **It deploys no infrastructure** and uses the
same siteverify endpoint as a hand-rolled setup — the three paths differ only in where the create
call runs, and produce an identical widget:
- **Dashboard** — Turnstile → *Set up with Spin*. First domain chip is pre-filled from your first
  active zone; `localhost`/`127.0.0.1` are added automatically. The returned agent prompt contains
  the **sitekey but never the secret**.
- **Wrangler CLI** — full widget CRUD, no agent needed. This is the part worth remembering:
  ```sh
  wrangler turnstile widget create "myproject" --domain example.com --domain localhost --mode managed
  wrangler turnstile widget list | get <sitekey> | update <sitekey> --domain <d> | delete <sitekey> [-y]
  ```
  All accept `--json`; `--domain` takes comma-separated values or repeated flags.
- **AI coding agent** — paste the prompt pointing at `turnstile/spin/prompt.md`, or install it as a
  local skill. Locally the `cloudflare:turnstile-spin` skill does the same.

⚠️ **`wrangler turnstile widget get <sitekey> --json` prints the widget secret.** Treat that output as
a credential: never echo it, never pass it as a command argument, never let it reach logs, temp files
or chat. Automated flows are expected to set `WRANGLER_WRITE_LOGS=false`, `WRANGLER_LOG=log`,
`WRANGLER_LOG_SANITIZE=true`, and to confirm account/sitekey/destination before retrieval.
⚠️ Spin adds `localhost`/`127.0.0.1` for convenience — **your backend must still validate the hostname
returned by siteverify**, and production must not accept local hostnames.

## Gotchas
- **The server-side validation gotcha (the whole point):** the client token proves nothing on its
  own — a `success` widget callback is trivially forged. You MUST call **siteverify on your server**
  with the secret. Never trust the client, never call siteverify from the browser (CORS + it would
  expose the secret).
- **Tokens are single-use and expire in 5 min.** Re-validating a token → `timeout-or-duplicate`.
  Generate a fresh token per submission; on any submit error call `turnstile.reset(widgetId)`.
- **Field name is exactly `cf-turnstile-response`** — wrong name → `missing-input-response`.
- **Secret never client-side.** Wrong/missing secret → `invalid-input-secret` / `missing-input-secret`.
- **CSP** must allow `challenges.cloudflare.com` for both `script-src` and `frame-src`, or the widget
  won't render.
- **SPA/React:** control the widget lifecycle with a ref and clean up with `turnstile.remove` on
  unmount; StrictMode double-render and SSR (`window.turnstile` undefined) bite otherwise.
- **Behind a proxy**, send the real client IP (`CF-Connecting-IP`, or first `X-Forwarded-For`).

## Pricing & limits
> ⚠️ Pricing/plans change — verify on the live page (`developers.cloudflare.com/turnstile/plans/`)
> before quoting.

**Free** for essentially all use cases — **unlimited challenges / verification requests**, all widget
types, pre-clearance, WCAG 2.2 AA. Cost driver on Free is none; the cap is **20 widgets per account**
and **10 hostnames per widget**, **7-day** analytics lookback.

**Enterprise** (Contact Sales) adds: unlimited widgets, 200 hostnames/widget, any-hostname widgets,
30-day analytics, ephemeral IDs, device fingerprinting, off-label (remove Cloudflare branding).

**Key constraints:** token validity **5 min** · token use **single** · widget size 300×65 (normal), 150×140 (compact),
flexível 100% com mínimo de 300px. siteverify error codes: `missing/invalid-input-secret`, `missing/invalid-input-response`,
`timeout-or-duplicate`, `internal-error`, `bad-request`.

## Going deeper
- Covered by the official `cloudflare` skill (`references/turnstile/`) — use it for the full client
  API, configuration options, framework patterns (React/Next/Vue), and the complete error table.
- Pages sites: use the Pages Turnstile plugin instead of a standalone Worker.
