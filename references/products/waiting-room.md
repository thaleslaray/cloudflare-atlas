# Waiting Room — virtual queue for peak traffic

> Route excess visitors to a customizable virtual waiting room during traffic surges, so you
> protect your origin and preserve UX during launches, sales, drops, and ticket on-sales.
> Configured per host/path on a zone — no code at the origin required.

## Contents
- When to use (and when not)
- How it works
- Config (API parameters)
- Custom pages
- Queueing methods & events
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- **Protect origin during predictable spikes**: product launches, flash sales, limited-stock drops,
  ticket on-sales, registration windows. Queues users instead of letting the origin 5xx.
- You want a graceful, branded holding page with **live estimated wait times** instead of error pages.
- **Not** for: rate-limiting abusive/bot traffic (→ WAF Rate Limiting, Bot Management); DDoS (→ automatic
  DDoS protection); generic caching (→ Cache). Waiting Room queues *legitimate* users, it is not a security filter.
- Requires Cloudflare CDN + a **proxied (orange-cloud) DNS record or load balancer** on the covered hostname,
  and visitors must accept cookies.

## How it works
- Runs on Workers at the closest data center; decides queue-vs-pass with **no added latency** — safe to leave on always.
- Decision uses admin thresholds (`total_active_users`, `new_users_per_minute`) + a Waiting Room *state*
  snapshot maintained per data center and propagated globally every few seconds via Durable Objects.
- Each visitor gets a `__cfwaitingroom` cookie; while queued, the page **auto-refreshes every 20s** with an
  updated estimated wait time. Default order is **FIFO** by cookie timestamp.
- `session_duration` = how long a user stays "active" after their last request; lets them leave and re-enter
  without re-queuing, and drives dynamic outflow (slots free up as sessions expire).

## Config (API parameters)
Created per zone via dashboard (**Traffic → Waiting Room**) or API (`POST /zones/{zone_id}/waiting_rooms`).
```bash
curl "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/waiting_rooms" \
  --request POST --header "Authorization: Bearer $CF_API_TOKEN" \
  --json '{
    "name": "shop_waiting_room", "host": "shop.example.com", "path": "/shop",
    "total_active_users": 300, "new_users_per_minute": 200,
    "session_duration": 5, "queueing_method": "fifo",
    "queueing_status_code": 200, "json_response_enabled": false
  }'
```
Key parameters:
- **`total_active_users`** (required, >200): max simultaneous active sessions on the host/path. Best practice: set to **~75% of origin capacity**.
- **`new_users_per_minute`** (required, >200, ≤ total_active_users): threshold for influx rate — **not** the number admitted per minute. Set to **~100% of expected peak** so users queue only when needed.
- **`session_duration`** (1–30 min, default 5): re-entry / active window.
- **`host`** (required, no wildcards/scheme), **`path`** (case-sensitive; applies to all subpaths).
- **`additional_routes`** + **`cookie_suffix`** (Enterprise advanced): cover multiple host/path combos in one room; cookie_suffix is required when using additional_routes.
- **`json_response_enabled`**: return JSON (on `Accept: application/json`) for native mobile/non-browser clients.
- **`queueing_status_code`** (default 200): HTTP status while queuing (e.g. 202).
- **`turnstile_mode`** / **`turnstile_action`** (advanced): bot challenge in the queue; `infinite_queue` traps failures.
- **`disable_session_renewal`** (Enterprise): cap total browsing time to `session_duration`.

## Custom pages
- **Default**: unbranded page with estimated wait time; pick from ~15 built-in languages (EN, PT-BR, ES, FR, DE, JA, etc.).
- **Custom** (Enterprise advanced add-on): full HTML/CSS via `custom_page_html`, **Mustache**-templated. Limit **1 MB**.
  - Variables: `{{waitTime}}`, `{{waitTimeKnown}}`, `{{waitTimeFormatted}}`, `{{queueIsFull}}`, etc. Keep the
    time-remaining block to show wait times. Use triple braces `{{{turnstile}}}` to place the Turnstile widget (raw HTML).
  - Preview without deploying: `POST /zones/{zone_id}/waiting_rooms/preview` with `custom_html` → returns a
    `waitingrooms.dev/preview/...` URL (add `?force_queue` to preview the queued state).
- Note the field mismatch: preview uses **`custom_html`**, the room config uses **`custom_page_html`**.

## Queueing methods & events
- **FIFO** (default, all plans): first-in, first-out by cookie timestamp.
- **Random / Reject / Passthrough** (Enterprise advanced): random fair admission; reject (static page, for
  maintenance/event-only); passthrough (all traffic to origin but still gather `total_active_users` /
  `new_users_per_minute` analytics — great for sizing thresholds before going live).
- **Queue-all**: force every new visitor into the queue (overrides all other settings, incl. events). Active sessions are unaffected until they expire.
- **Scheduled events** (advanced): temporarily override settings for a window; supports **pre-queueing** and "shuffle at event start". Max **5 events per room**; use separate rooms for overlapping events.
- **Waiting Room rules** (advanced): `bypass_waiting_room` action via expressions (subpaths, IP lists, asset extensions).

## Gotchas
- **Subpaths are included**: a path applies to every subpath — you may queue more than intended. Most-specific subpath wins when rooms overlap.
- **Don't host queue-page assets on the covered hostname** — those requests get queued too. Serve images/CSS from a different host.
- **Rate limiting must allow ≥1 request / 20s** or the auto-refresh breaks. Keep this in mind with WAF rate-limit rules.
- **Bots clog the queue**: bots that drop cookies count as many one-shot inactive users, wasting slots. Use Bot Management / Turnstile infinite-queue.
- **Cookies required**: visitors without cookies never exit an actively-queuing room.
- **Overshoot on sharp spikes**: rising several thousand users/min, global state takes ~2 min to propagate — temporary overshoot of thresholds can occur.
- Changing FIFO↔Random mid-queue shifts displayed wait times; FIFO→Random→FIFO preserves original entry order.
- A DNS record is **not** auto-created for the room's hostname — you must have a proxied record/LB.

## Pricing & limits
> ⚠️ Plan-gated, not metered. Verify on the live pricing/plans page
> (`developers.cloudflare.com/waiting-room/plans/` and `cloudflare.com/plans/`) before quoting.
- **Availability**: **Business and Enterprise** plans only (also Project Fair Shot qualifiers). Free/Pro: not available.
- **Business**: **1** basic room, FIFO only, invisible Turnstile, no custom templates, customizable queue status code, SEO crawler bypass.
- **Enterprise**: 1 room default; purchase **Waiting Room Advanced** to unlock multiple/custom rooms, custom templates, Random/Reject/Passthrough, scheduled events, rules, multi-host coverage, session revocation/disable-renewal, JSON response, full Turnstile modes.
- Enterprise can preview as a non-contract service (full access, no metered fees).
- **Limits**: `total_active_users` and `new_users_per_minute` must be **> 200**; `new_users_per_minute` ≤ `total_active_users`; `session_duration` 1–30 min; **5 events/room**; custom HTML **≤ 1 MB**; one room per page; one plan per zone.

## Going deeper
- Full API (create/update/events/rules/status/preview, response variables): `developers.cloudflare.com/api/resources/waiting_rooms/`.
- Architecture deep-dive: `blog.cloudflare.com/how-waiting-room-queues`.
- Analytics (GraphQL `waitingRoomAnalyticsAdaptiveGroups`): `developers.cloudflare.com/waiting-room/waiting-room-analytics/`.
- No official `cloudflare` skill `references/` entry exists for this product — this file is the primary reference.
