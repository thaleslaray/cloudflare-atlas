# Rules — edge request/response logic, no code

> Zone-level rules that **modify requests, transform headers/URLs, redirect, override origin, and
> tweak Cloudflare settings** at the edge — declaratively, without a Worker. Transform Rules,
> Redirects, Origin Rules, Configuration Rules, Compression Rules, Snippets, and (legacy) Page Rules.

## Contents
- When to use (and when not)
- The rule types (pick the right one)
- Config & deployment
- Execution order & matching
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- You need edge logic but **don't want to write/deploy a Worker**: URL rewrites, redirects, header
  add/remove, host/port override, cache control, per-path Cloudflare settings.
- Requires **proxied (orange-cloud) DNS** — traffic must pass through Cloudflare. Rules never run on
  grey-clouded / DNS-only hostnames.
- Reach for the *most specific* product: a redirect → Redirects, a header tweak → Transform Rules.
  Only escalate to **Snippets** (JS) when built-in rule actions can't express the logic, and to
  **Workers** when you need state, bindings, KV/D1/DO, AI, cron, or heavy compute.
- **Not** for: stateful apps, DB/KV access, AI inference, anything needing bindings → use Workers.

## The rule types (pick the right one)
- **Transform Rules** — rewrite URI path/query; set/remove **request & response headers**. Plus
  **Managed Transforms** (one-click common header adjustments, e.g. add visitor location headers).
- **Redirects** — **Single Redirects** (zone-level, dynamic, wildcard/regex source→target) and
  **Bulk Redirects** (account-level, static, list-based, scales to millions of URLs).
- **Origin Rules** — override **Host header, SNI, resolved DNS hostname, destination port** per
  match (route to a different backend). Host/SNI/DNS overrides are **Enterprise-only**; the
  destination port override is available on **all plans**.
- **Configuration Rules** — override Cloudflare **settings** for matching requests (SSL mode,
  security level, cache level, Polish, etc.) instead of applying them zone-wide.
- **Compression Rules** — choose response compression (gzip/brotli/zstd) by content type / extension.
- **Snippets** — short **JavaScript** for logic beyond built-in actions (JWT validation, complex
  redirects, multi-origin retry). The bridge between Rules and Workers; runs in the Workers runtime
  but with tight limits (see below).
- **Custom Errors** — serve custom content for origin/Cloudflare/Worker error responses.
- **Cloud Connector** — route matching traffic to a public cloud bucket/service (AWS/GCP/Azure).
  Currently in **beta** (available on all plans).
- **Page Rules** — **deprecated/legacy** URL-pattern actions. Use the modern rule products above for
  new work; migrate existing Page Rules where possible.

> **Cache Rules** are part of Rules conceptually but live under **Cache** (`cache/how-to/cache-rules/`),
> not the `rules/` product. Use them for cache TTL/eligibility/key control — not Page Rules.

## Config & deployment
- **No Worker binding / `wrangler.jsonc`** — Rules are zone (or account) configuration, not code you
  bind. Manage them via:
  - **Dashboard** → *Rules* (Templates gallery covers common cases).
  - **API / Terraform** — built on the **Ruleset Engine**; rules are entries in a ruleset attached to
    a zone phase. Match conditions use the **Rules language** (the same field/operator expression
    syntax as WAF custom rules, e.g. `http.request.uri.path`, `http.host`, `ip.geoip.country`).
- Snippets *do* have code + a single "snippet rule" (filter expression) each; deploy via dashboard or
  API. A snippet with no rule shows as an **Unused Snippet**.

## Execution order & matching
Rules across products run in a **fixed phase order** (not the order you create them). High level:
Single Redirects → URL Rewrite → Configuration Rules → Origin Rules → Bulk Redirects →
Managed Transforms → Request Header Transforms → Cache Rules → Snippets → Cloud Connector.
All of these take **precedence over Page Rules**.
- **Terminating actions** (Block, Redirect, Challenge) stop evaluation immediately — first match wins.
- **Non-terminating** changes in the same phase: **last write wins** (later rules overwrite earlier).
- Use **Cloudflare Trace** (`rules/trace-request/`) to see which rules fire for a given URL.
- **Expression language, 2026-10** (`ruleset-engine/rules-language/`):
  - **Dynamic comparisons** — `eq`/`ne`/`lt`/`le`/`gt`/`ge` accept a field or function result on the
    right side (same scalar type both sides): `http.request.uri.path ne raw.http.request.uri.path`.
  - **`coalesce(a, b, …)`** — first non-nil argument (≥2, same type); fallback for missing values.
  - **`hash_in_range(min, max, seed…)`** — all HTTP products, all plans. Range `[min, max)`, literal
    bounds, seeds must be fields; e.g. ~10% sample: `hash_in_range(0, 100, cf.random_seed) < 10`.
  - **`cf.appsec.request.failed_detections`** (2026-10-09) also works in zone Request Header Transform Rules (→ `waf.md`).

## Gotchas
- **Proxied DNS required** — the #1 reason a rule "doesn't fire" is a grey-clouded record. Even
  placeholder hostnames need a proxied record (use a reserved IP like `192.0.2.1`).
- **Regex needs a plan** — Transform/Single Redirect regex matching is **Business+** (Free/Pro get
  wildcards only). The **Origin Rules** Host/SNI/DNS overrides are **Enterprise-only** (port is not).
- **Challenge loops** — combining Cloudflare challenges with Rules can loop; see Rules troubleshooting.
- **Snippets are not Workers**: 5 ms max execution time, 2 MB memory, 32 KB package, limited subrequests, **no
  bindings / env vars / observability / cron / Durable Objects / D1**. Hit a wall → move to Workers.
- **Bulk vs Single Redirects**: Bulk is static (no string replacement/regex) but huge scale; Single is
  dynamic but capped at a few hundred rules. If both match a redirect, Single Redirects wins.
- **Page Rules deprecated** — don't build new logic on them.
- **Stream stalls behind the proxy** — features that inspect `text/html`/`text/plain` bodies (Rocket
  Loader, Email Obfuscation, Automatic HTTPS Rewrites, challenges, Web Analytics beacon, Markdown for
  Agents, AI Labyrinth…) can hold part of a response and raise TTFB. Fix the `Content-Type` first;
  `Cache-Control: no-transform` stops *changes* but not read-only inspection; last resort is a path-scoped
  Configuration Rule with **Response Body Buffering = None** (disables those features there).

## Pricing & limits
> ⚠️ Pricing/limits change — verify on the live pages (`developers.cloudflare.com/rules/`) before quoting.

**Cost model:** most Rules features are **included in all plans at no extra cost** — you pay via your
**plan tier** (Free/Pro/Business/Enterprise), which gates quotas and features rather than per-request
billing. Snippets are free on all **paid** plans. (Workers, by contrast, are usage-based.)

**Representative quotas (per zone unless noted), verified against the live docs 2026-08-25:**
- **Single Redirects:** 10 (Free) / 25 (Pro) / 50 (Biz) / 300 (Ent). Regex: Business+.
- **Page Rules (legacy):** 3 / 20 / 50 / 125.
- **Snippets:** 0 (Free) / 25 / 50 / 300; subrequests 0 / 2 / 3 / 5. Limits (all plans):
  **5 ms max execution time, 2 MB memory, 32 KB total package size**.
- **Bulk Redirects (per account):** 15 rules / 5 lists / 10k URLs (Free) up to 50 rules / 25 lists /
  1M+ URLs (Ent).
- **Origin Rules:** 10 / 25 / 50 / 300 rules. Host/SNI/DNS overrides: **Enterprise-only**;
  destination port override: **all plans**.
- **Custom Errors:** paid plans only — 0 (Free) / 25 / 50 / 300 rules and assets; Origin Error
  Pages are Enterprise-only.
- **Configuration / Compression / Transform / Cache Rules, Cloud Connector:** 10 / 25 / 50 / 300.
Transform Rules, Configuration Rules, Compression Rules: available all plans (regex Business+).

## Going deeper
- **No dedicated official `cloudflare` skill ref** for Rules — this file is the primary summary.
- Expression syntax (fields/operators) → **Ruleset Engine / Rules language**
  (`developers.cloudflare.com/ruleset-engine/rules-language/`). Phase order →
  `ruleset-engine/reference/phases-list/`.
- Snippets vs Workers decision guide → `rules/snippets/when-to-use/`. For Workers itself, see the
  official `cloudflare` skill `references/workers/` and `references/snippets/`.
- Examples gallery → `rules/examples/`. Debug with Cloudflare Trace → `rules/trace-request/`.
