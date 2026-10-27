# Health Checks — standalone origin/endpoint monitoring with alerts

> Monitor an IP address or hostname from Cloudflare's edge and get notified in near real-time
> when an origin goes unhealthy. The standalone uptime monitor — no load balancer required.
> Now offered as part of Cloudflare's origin safeguard, **Smart Shield**.

## Contents
- When to use (and when not)
- Configuration
- Notifications & analytics
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- **Standalone uptime monitoring** of a single origin / endpoint (IP or hostname) with email alerts —
  even when you have only one origin and don't (yet) need to balance traffic.
- You want edge-based, multi-region probing of response codes, latency, and body content, with
  analytics (uptime %, failure reason, RTT) to debug origin issues.
- **Not** for: traffic distribution or failover — that's [Load Balancing](https://developers.cloudflare.com/load-balancing/).
- **vs Load Balancing monitors:** standalone Health Checks are independent objects you create directly.
  Load Balancing **monitors** are tied to **pools** and drive routing/failover decisions. If you need
  failover, use LB monitors; if you only need "is it up? alert me," use standalone Health Checks.

## Configuration
Created via the dashboard (**Traffic → Health Checks → Create**) or the API. No Worker binding /
`wrangler.jsonc` — it's an account/zone-level service. Key fields:

- **Type / protocol** — HTTP, HTTPS, or TCP. **Path** targets a specific app on a multi-app origin.
- **Interval** — how often to probe. **Retries** — timeouts to retry before marking unhealthy.
- **Check regions** — choose **1 to 13** regions; Cloudflare probes from **3 data centers per region**.
  **All Regions** is Business/Enterprise only.
- **`expected_codes`** — HTTP status codes that count as healthy (mismatch → failure).
- **`expected_body`** — case-insensitive substring that must appear in the **first 10 KB** of the body.
- **`follow_redirect`** — set `true` if the origin redirects (e.g. HTTP→HTTPS 301/302/303).
- **`allow_insecure`** — set `true` to accept self-signed / untrusted TLS certs.
- **`header`** — Host header sent (also used as TLS ServerName; required for some TLS setups).

API base: `POST/GET/PUT/DELETE /client/v4/zones/{zone_id}/healthchecks`. Checks can be enabled,
disabled, edited, or deleted at any time.

## Notifications & analytics
- **Alerts** (Pro+): **Configure an alert** → name, description, notification email → select which
  health checks to include → choose a **trigger**: notify when origin becomes **unhealthy**,
  **healthy**, or **either**. Emails arrive within seconds and include the change time, status,
  reason, expected vs. received response code. Set up via Cloudflare Notifications.
- **Health Checks Analytics** (Pro+): uptime % per origin, failure-reason breakdown, latency (RTT),
  and an **Event Log** with per-record detail (RTT, failure reason, waterfall, status code). Entries
  are labeled per region or **Global** (aggregate of all enabled regions — not a configurable region).

## Gotchas
- **Notification quorum:** an alert fires only after a status change in the **majority** of selected
  regions — 2 of 3 data centers for one region; 7 of 13 with all 13 regions selected. A single flaky
  data center won't page you.
- **Body limit:** only the **first 10 KB** of the response is read. If `expected_body` isn't in that
  window, the check fails — keep the marker near the top.
- **HTTP→HTTPS redirects** cause "response code mismatch" (301/302/303). Use HTTPS or `follow_redirect: true`.
- **Self-signed / untrusted certs** → "TLS untrusted certificate." Use a public CA cert or `allow_insecure: true`.
- **TLS name / unrecognized-name errors** → set the **Host `header`** (drives the TLS ServerName).
- **No authenticated origin pull** (mTLS) support for standalone Health Checks.
- **Load on origin:** shorter **Interval** + more **Check regions** = more requests to your origin
  (3 data centers per region, each probing). Tune both together.
- **DNS Internal** failure: an origin hostname resolving to a **non-publicly-routable / restricted IP**
  (e.g. localhost) → no checks run. Different case: a hostname resolving to a **Cloudflare anycast IP**
  (proxied) still runs, but probes Cloudflare's edge, not your origin — use the origin IP or an
  unproxied hostname.
- **Zone Lockdown** blocks edge probes — bypass with a WAF custom rule matching the Health Checks
  user agent: `Mozilla/5.0 (compatible;Cloudflare-Healthchecks/1.0;+https://www.cloudflare.com/; healthcheck-id: XXX)`
  where `XXX` is the first 16 chars of the Health Check ID; action **Skip → Zone Lockdown**.

## Pricing & limits
> ⚠️ Pricing/plan gating changes — verify on the live page (`developers.cloudflare.com/health-checks/`
> and the Cloudflare plans page) before quoting.

**Plan gating** (not metered per-check; bundled by plan, as of 2026-06):

| Plan       | Available | Max checks | Analytics |
| ---------- | --------- | ---------- | --------- |
| Free       | No        | 0          | No        |
| Pro        | Yes       | 10         | Yes       |
| Business   | Yes       | 50         | Yes       |
| Enterprise | Yes       | 1,000      | Yes       |

- **Free plan has no Health Checks.** Notifications/alerts require **Pro or higher**.
- **Regions:** 1–13 selectable; **All Regions** is Business/Enterprise only.

## Going deeper
- No dedicated official `cloudflare` skill ref exists for this product — this file is the primary source.
- Full config reference & API: `developers.cloudflare.com/health-checks/` (get-started, analytics,
  concepts/regions, how-to/notifications, how-to/zone-lockdown).
- Error-code catalog (TCP/HTTP/TLS/DNS failures + fixes): Health Checks Analytics → "Common error codes".
- Need failover/traffic steering instead of just alerts → `load-balancing/monitors/`.
- Smart Shield (the umbrella product this now ships under): `developers.cloudflare.com/smart-shield/`.
