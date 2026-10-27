# AI Crawl Control — see / allow / block / monetize AI crawlers

> Visibility into which AI services crawl your site, and controls to **allow, block, or charge**
> them. Formerly "AI Audit". Works on **all plans, zero config** for any zone proxied through
> Cloudflare. No official `cloudflare` skill ref — this file is the source.

## Contents
- What it is
- When to use
- How to configure (dashboard)
- Key concepts
- Pay per crawl (monetization)
- Gotchas
- Pricing, limits & availability

## What it is
A zone-level dashboard (**dash → AI Crawl Control**, tabs: Overview / Crawlers / Metrics /
Directives / Settings) that surfaces AI-crawler traffic and lets you act on it per crawler:
- **See** — which AI bots/operators (OpenAI, Anthropic, Google, Microsoft, ByteDance, Meta…) hit
  which paths, request volume/trend, status codes, and robots.txt violations.
- **Allow / Block** — per-crawler action. Blocking writes a **WAF custom rule** on the zone.
- **Charge** — pay per crawl (private/closed beta) — price per zone, Cloudflare is Merchant of Record.
- **Track robots.txt** — availability, Content Signals presence, and crawlers violating directives.

## When to use
- Publishers/content sites wanting visibility into AI scraping and to allow value-adding crawlers
  (citations, referrals) while blocking others.
- E-commerce / docs sites protecting pricing, inventory, or technical content from training scrape.
- You want to **monetize** AI access to content (pay per crawl, beta).
- **Not** a general bot mitigation tool → that's **Bots / Bot Management**. Not a firewall → **WAF**.
  AI Crawl Control is the AI-crawler-specific control plane layered on top of those.

## How to configure (dashboard)
Prereqs: domain on Cloudflare, **proxied** (orange-cloud / reverse proxy). No binding/Wrangler — UI only.
1. **Monitor** — Overview tab → snapshot; filter by date range, crawler, operator, hostname, path.
2. **Block a crawler** — Crawlers tab → **Action** column → **Block** (or **Allow**). Block auto-creates/updates
   one WAF custom rule on the zone.
3. **Configure block response** (Paid) — Settings → Block response → choose code (**403 Forbidden** or
   **402 Payment Required**) + custom body (e.g. licensing contact). Must have ≥1 crawler blocked first.
4. **Metrics** tab — breakdowns by crawler, operator, status, hostname, path.
5. **Directives** tab — robots.txt availability/health + violations; optionally enable **Managed robots.txt**.

**Programmatic analytics:** no config API; query traffic via the **GraphQL Analytics API**
(`httpRequestsAdaptiveGroups`, filter on `botDetectionIds_hasany:[...]` or `userAgent_like:"%GPTBot%"`).

## Key concepts
- **Detection tiers:** free plan → detection via **user-agent strings** (self-identifying bots only).
  **Enterprise plans with Bot Management** → **Bot Management detection ID** (far more robust, harder
  to spoof), configurable analytics timeframes, and the ability to charge via pay per crawl.
- **Categories:** crawlers tagged AI crawler / AI assistant / archiver / search (Verified Bot categories).
- **Order of precedence:** WAF custom rules (incl. AI Crawl Control blocks) → Bot solutions → **pay per crawl**.
  A WAF/Bot **block elsewhere overrides** pay-per-crawl "charge" (blocked = no access, no charge).
- **Managed robots.txt** (a Bots feature, **all plans**): Cloudflare **prepends** its managed
  `robots.txt` before your existing one (combined into a single response), with directives blocking
  common training crawlers + the **Content Signals** policy (`search=yes,ai-train=no`, `use=reference`).
- **AI Labyrinth** (Bots): traps crawlers that ignore robots.txt — complementary, not part of this product.
- **Bots defaults change 2026-09-15** (Bots, not this product): for **new domains**, bots classified
  **Training** or **Agent** get blocked on pages that display ads; **Search** stays allowed. Mixed-purpose
  Search+Training crawlers are blocked by every AI-training block config, incl. legacy "Block AI bots".
  All customers could opt out before Sept 15 in zone Security settings.

## Pay per crawl (monetization, closed beta)
- Site owner sets **one default price per zone** (min **$0.001 USD/crawl**); cannot price per crawler —
  only the Block/Charge/Allow *action* is per-crawler. **Dynamic pricing** (opt-in) lets the origin, or a
  Worker, return a `crawler-price` response header per request; Cloudflare then adds a `cf-pay-per-crawl`
  request header to origin requests (`pricing=zone-default | in-band | bypass`).
- Flow: crawler requests → server returns **`HTTP 402 Payment Required`** + `crawler-price: USD 0.01`.
  Crawler retries with `crawler-exact-price` or `crawler-max-price` header (must be in the **signed**
  `signature-input` Web Bot Auth components). Charge fires only on successful **HTTP 200** delivery.
- **Always-free paths:** `/robots.txt`, `/sitemap.xml`, `/security.txt`, `/.well-known/security.txt`,
  `/crawlers.json`. Error responses are never billed.
- **Payouts:** connect a dedicated **Stripe Connect** account (pre-existing Stripe accounts not
  compatible); **Administrator/Super Administrator** role required. Cloudflare aggregates charges → **monthly** payouts. Re-crawls bill again.

## Gotchas
- **Free plan caps:** Metrics tab shows **only last 24h**; analytics window is fixed. Detection is
  UA-only, so spoofed/unknown bots slip through — upgrade for detection-ID accuracy.
- **Robots.txt violations are retroactive:** computed against your *current* directives vs *past*
  requests. Adding a new `Disallow` flags historical requests as violations even if legal at the time.
- **Block response code:** if you hand-edit the underlying WAF rule to a code other than 403/402, the
  Settings dropdown goes blank and the chosen code won't enforce — keep it 403 or 402.
- **WAF rule budget:** blocking consumes one custom rule; "allow all" uses none. Plans cap custom-rule count.
- **Pay per crawl vs other rules:** a country/IP/bot block in WAF runs *before* pay-per-crawl and wins —
  the crawler is blocked even with valid payment headers. Audit existing WAF rules so they don't shadow AI crawlers.
- **Detection ID drift:** GraphQL `botDetectionIds` values (e.g. GPTBot `123815556`) can change; verify live.

## Pricing, limits & availability
> ⚠️ Verify on the live page (`developers.cloudflare.com/ai-crawl-control/`) before quoting —
> this product is evolving fast (renamed from AI Audit; pay per crawl in beta).
- **Core product (see/allow/block):** available on **all plans, free, zero config**.
- **Enterprise + Bot Management adds:** advanced detection ID, configurable analytics window, pay per crawl.
  **Custom block response** (403/402 + body) is a **paid-plan** feature.
- **Pay per crawl:** **closed/private beta** — sign up at `cloudflare.com/paypercrawl-signup/` or via
  Enterprise account exec. Min price **$0.001/crawl**; Stripe payouts (Merchant-of-Record wording not
  stated in current docs — verify before quoting).
- No published per-request pricing for the audit/control features themselves (bundled with the plan).
