# Bots / Bot Management — detect & manage automated traffic

> Detect and act on bot traffic (scraping, credential stuffing, inventory hoarding, AI crawlers).
> Three tiers: **Bot Fight Mode** (Free toggle) → **Super Bot Fight Mode** (Pro/Biz, per-category
> actions) → **Bot Management for Enterprise** (granular 1–99 **bot score** usable in WAF/Workers).

## Contents
- When to use (and which tier)
- Bot score & key fields
- Detection engines
- Config & access patterns
- Gotchas
- Pricing & plan-gating
- Going deeper

## When to use (and which tier)
- **Bot Fight Mode (Free)** — one toggle; challenges definite bots (cloud-hosted, headless) across
  the whole domain. No rules, no score, no targeting. Add-ons: Block AI bots, AI Labyrinth, managed `robots.txt`.
- **Super Bot Fight Mode (Pro/Business, and Enterprise without the add-on)** — choose allow/block/challenge
  per bot *category*, protect static resources + WAF custom rule exceptions. Still **no per-request score**,
  no per-endpoint scoring. **Pro only gets "Definitely automated" (score 1)**; **"Likely automated" (2–29) is
  Business/Enterprise**. Analytics: Pro = limited "Bot Report"; Business = dedicated Bot Analytics.
- **Bot Management for Enterprise** — granular **1–99 bot score** in WAF/Workers, per-path/IP rules,
  JA3/JA4 fingerprints, full Bot Analytics. For ecommerce, banking, login/checkout protection. Enable via account team.
- **Not** for: CAPTCHA-style human checks on a form (→ turnstile); generic vuln/rule filtering (→ waf);
  DDoS (→ ddos-protection); API-specific abuse (→ api-shield).

## Bot score & key fields
A **bot score** is `1`–`99`: **1 = almost certainly a bot**, **99 = almost certainly human**. `0` = *not
computed* (request not evaluated — internal CF, or handled by Redirect Rules etc. **before** BM; not "safe").
Granular scores are **Enterprise-only**; Pro/Biz see only **groupings** in Bot Analytics.

**Groupings:** `0` Not computed · `1` Automated · `2–29` Likely automated · `30–99` Likely human · Verified bot.
Common threshold: treat **`score < 30`** (and not verified) as bot.

WAF / Ruleset Engine fields (and Workers `request.cf.botManagement.*`):
- `cf.bot_management.score` — int 1–99 (`.score`)
- `cf.bot_management.verified_bot` — allowlisted good bot, e.g. Googlebot (`.verifiedBot`)
- `cf.bot_management.static_resource` — matches static-asset extensions (`.staticResource`)
- `cf.bot_management.ja3_hash` / `cf.bot_management.ja4` — TLS client fingerprint (HTTPS only)
- `cf.bot_management.detection_ids` — heuristic detection IDs (`.detectionIds`)
- `cf.bot_management.signed_agent` (Web Bot Auth), `cf.verified_bot_category`, `cf.bot_management.corporate_proxy`
- JSD result: `cf.bot_management.js_detection.passed` (Workers: `request.cf.botManagement.jsDetection.passed`)

```txt
# WAF: block definite bots but never verified/static
(cf.bot_management.score eq 1 and not cf.bot_management.verified_bot)
# Protect sensitive endpoints
(cf.bot_management.score lt 30 and not cf.bot_management.verified_bot
  and http.request.uri.path in {"/login" "/checkout"})
```
```ts
// Workers
const s = request.cf?.botManagement?.score;
if (s && s < 30 && !request.cf?.botManagement?.verifiedBot)
  return new Response("Bot detected", { status: 403 });
```

## Detection engines (Enterprise)
- **Heuristics** — pattern-match known malicious fingerprints; deterministic, sets **score = 1** (occasionally 29).
- **Machine Learning** — majority of detections; supervised model over billions of daily requests → score 2–99.
- **JavaScript Detections (JSD)** — invisible JS injection to catch headless browsers; on by default, optional.
- **Anomaly Detection** — *deprecated* (no new onboarding); per-domain baseline outlier detection.
- The `__cf_bm` cookie smooths scores across a user's session to cut false positives.

## Config & access patterns
- **No `wrangler.jsonc` binding.** Bot data arrives automatically on `request.cf.botManagement` in any Worker
  on the zone; in WAF/Rate-limiting/Custom rules via the `cf.bot_management.*` fields above.
- Configure in dashboard: **Security → Bots** (modes, JSD toggle, per-category actions, analytics).
- Enforcement is done in **WAF custom rules** keyed on score — BM scores requests; *you* decide the action.
- Log fields once enabled: `BotScore`, `BotScoreSrc`, `BotTags`, `BotDetectionIDs` (Logpush/Logpull).
- **AI traffic controls (2026-07, all plans):** manage AI crawlers by behavior — **Search / Agent / Training** —
  with per-category actions (Block all pages / Block on pages with ads / Allow). The new defaults (Training +
  Agent blocked on ad-displaying pages, Search allowed) apply **only to new domains from 2026-09-15**; the
  legacy "Block AI bots" toggle is deprecated on that date. Enterprise
  BM adds **BotBase** (searchable directory of tracked bots/agents + detection IDs) and **Attribution
  Business Insights** (site-wide & per-operator crawl-to-referral ratios).

## Gotchas
- **Score = 0 ≠ human.** Means BM didn't run (internal request, Worker/Orange-to-Orange routing, or a
  feature ran before BM). Don't allow on `score == 0`.
- **Always exclude** `verified_bot` and `static_resource` from block rules, or you'll break Googlebot,
  email image pixels, etc.
- **JSD needs a CSP allowance:** `script-src ... /cdn-cgi/challenge-platform/;`, an HTML page first, and a
  **Managed Challenge** action (not Block) — otherwise `jsDetection.passed` stays false.
- **JA3/JA4 are HTTPS-only** and **not user-unique** (same browser/lib version → same hash) — profiling, not identity.
- Tune false positives with a **Skip** rule on the affected path/IP — skip covers **Super Bot Fight Mode** rules,
  but **Bot Fight Mode (Free) cannot be skipped**; false negatives → raise
  threshold (30 → 50), enable JSD, add fingerprint rules.

## Pricing & plan-gating
> ⚠️ Pricing/packaging change — verify on `developers.cloudflare.com/bots/plans/` before quoting.

Not usage-metered — gated by **plan**:
- **Free** → Bot Fight Mode (challenge only, whole domain). **Pro/Business** → Super Bot Fight Mode
  (allow/block/challenge per category; Business adds many sophisticated bots).
- **Enterprise add-on** → Bot Management: granular **1–99 score**, JA3/JA4, per-path/IP rules, Advanced
  Bot Analytics; sold by the account team. Enterprise can **preview** it free of metered fees as a non-contract service.
- WAF custom rules per zone: **5** (Free) / **20** (Pro) / **100** (Business) / **1,000** (Ent).
  Bot Analytics: data up to **30 days** old (window: 72h at a time on Pro, 1 week on Business/Ent).

## Going deeper
- Covered by the official `cloudflare` skill (`references/bot-management/`) — use it for full
  Workers API (`api.md`), WAF rule templates (`patterns.md`), setup (`configuration.md`), and debugging (`gotchas.md`).
- Field reference: `developers.cloudflare.com/bots/reference/bot-management-variables/`.
- Scores/groupings detail: `developers.cloudflare.com/bots/concepts/bot-score/`.
