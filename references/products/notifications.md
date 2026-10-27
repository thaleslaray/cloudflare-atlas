# Notifications — account alerting (email, webhook, PagerDuty)

> Define **what** to be alerted about (DDoS, billing thresholds, cert expiry, health checks, security
> events...) and **how** it's delivered (email, webhook, or PagerDuty). Account-level config, not a
> Worker binding — manage in the dashboard or via the **Alerting v3 API**.

## Contents
- When to use (and when not)
- Delivery methods & plan gating
- Configuration (dashboard + API)
- Webhooks (the developer-relevant path)
- Notable alert types
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- Get alerted on Cloudflare-side events: DDoS mitigations, traffic/error-rate anomalies, origin
  unreachable, health-check status flips, cert validation/renewal/expiry, usage-based billing
  thresholds, security events (WAF), Pages deploy outcomes, tunnel health, abuse reports, etc.
- **Deliver into your own systems** via webhook (Slack, Discord, Teams, DataDog, Splunk, OpsGenie,
  ServiceNow, or a **generic webhook** you own — e.g. a Worker that fans out / transforms).
- **Not** for application-level events you emit yourself (use your own queue/Worker → Email/webhook),
  and **not** zone-scoped routing logic — this is account-wide alert *policy*, not WAF/rules.
- Only fires for **proxied** (orange-cloud) domains — Cloudflare needs to see the traffic to decide.

## Delivery methods & plan gating
- **Email** — all plans (incl. Free).
- **Webhooks** — account needs ≥1 zone on **Pro or higher** (then usable even from Free zones).
- **PagerDuty** — account needs ≥1 zone on **Business or higher** (connected service, OAuth).
- Availability of a *delivery method* is gated by the **highest** zone plan in the account; individual
  *alert types* are additionally gated by plan/product (many are Enterprise- or add-on-only).

## Configuration (dashboard + API)
Dashboard: **Notifications** page → **Add** → pick alert type → name it, add recipient email(s) and/or
attach webhook/PagerDuty destinations → set filters → **Create**. You can **Edit**, **Disable**
(toggle), **Delete**, **Test** (sends fake data), and **Mute** (temporary silence: 1h/12h/24h or
custom range; silenced alerts still appear in history, marked silenced).

API — the **Alerting v3** API under the account:
```
POST   accounts/{account_id}/alerting/v3/policies        # create a notification policy
GET    accounts/{account_id}/alerting/v3/policies         # list
GET    accounts/{account_id}/alerting/v3/history          # sent-notification log (paginated)
# destinations:
POST   accounts/{account_id}/alerting/v3/destinations/webhooks
# PagerDuty connect/list under .../destinations/pagerduty
```
- Permissions: dashboard needs **Super Administrator / Administrator** (or account-edit role); API
  token needs the **Notifications Read/Write** permission.
- A **policy** = alert type + filters + mechanisms (email addresses + webhook IDs + pagerduty IDs).

## Webhooks (the developer-relevant path)
- Create under **Destinations → Webhooks**: name + target **URL** + optional **secret**, then
  **Save and Test**. Destinations are reusable — attach to many policies.
- **Generic webhook auth:** Cloudflare sends your secret in the **`cf-webhook-auth`** header on every
  request. If the header is missing or wrong, **reject** it.
- **Payload:** JSON; test sends `{"text": "..."}`. Per-alert payload shape varies — see the webhook
  payload schema reference (below).
- **Egress restriction:** generic webhooks dispatch only to a **publicly resolvable IP on port 80/443**.
  For private IPs / other ports, relay through a **Worker** or a **Cloudflare Tunnel**.
- **Firewall:** requests come from **Cloudflare IP ranges** (`cloudflare.com/ips/`) — allowlist them;
  fetch the live list via the `cloudflare_ips` API as ranges change.
- Prebuilt integrations: Slack, Google Chat, Discord, Feishu, Teams (secret embedded in URL,
  auto-parsed); DataDog, Splunk, OpsGenie, ServiceNow (explicit secret/API key). Terraform-friendly:
  `cloudflare_notification_policy_webhooks` lets you set `secret` explicitly out of the URL.

## Notable alert types (non-exhaustive)
- **Billing:** Usage-Based Billing (per-product threshold; **Pro+**, pay-as-you-go accounts only).
- **DDoS:** HTTP / L3-4 attack alerts (all plans for HTTP); Advanced variants are configurable (rps/pps
  thresholds, hostnames, prefixes) on Enterprise + Advanced DDoS / Magic Transit / BYOIP.
- **Traffic Monitoring (Enterprise):** Origin Error Rate, Advanced Error Rate, Traffic Anomalies —
  spike/drop based, thresholds **not configurable** (SLO/Z-score driven).
- **Security:** WAF Security Events (Business/Enterprise; mandatory zone filter), Bot Detection (Ent),
  Brand Protection, Security Insights, Abuse report, Trust & Safety blocks.
- **SSL/TLS:** Universal/Advanced/SaaS cert alerts (validation, issuance, renewal, expiration — no fixed
  lead time documented) + AOP (hostname- and zone-level) and mTLS Certificate Store expiry, which fire
  **30 and 14 days** before expiry.
  **Certificate Transparency Monitoring** (GA 2026-08-13) is a *separate*, opt-in email alert with its
  own recipient list, configured under SSL/TLS → Edge Certificates, not here → `ssl.md`.
- **Reliability:** Health Checks status (Pro+), Load Balancing pool/health, Tunnel health, Secondary
  DNS, Magic Tunnel health, Logpush job failures (Ent).
- **Status:** Incident Alerts + Maintenance (all plans, filterable by impact/component/PoP).

## Gotchas
- **Removing a user does NOT remove their email from existing notifications** — edit each policy's
  recipients manually or they keep getting alerts.
- **Webhook test 400 Bad Request** often means you pointed a webhook at PagerDuty — PagerDuty must be a
  *connected service*, not a webhook destination.
- **Editing PagerDuty** = disconnect → change in PagerDuty → reconnect; disconnecting can leave a
  policy with no destination if it was the only one.
- **Editing webhooks** only allows renaming/deleting — to change the URL/secret, delete and recreate.
- Spike-based alerts (Traffic/WAF) fire on **threshold breach, not per-event**; can be noisy on
  high-traffic zones when grouping is enabled. Mean time to detection ~5 min for WAF events.
- Proxied-only: alerts won't fire for grey-clouded (DNS-only) records.

## Pricing & limits
> ⚠️ Verify on the live pricing/plans page (`cloudflare.com/plans/`) before quoting.

- **No separate charge for Notifications** — it's a platform feature; capability is gated by your zone
  **plan tier** (Free = email only; Pro = webhooks; Business = PagerDuty) and by per-alert product
  entitlements (many alerts require Enterprise or a specific add-on/subscription).
- **Notification History retention:** Free/Pro/Business = **30 days**; Enterprise = **90 days**
  (nothing before 2021-10-11). Retrieve via `GET .../alerting/v3/history`.
- Generic webhook delivery limited to public IP on port 80/443; Splunk has endpoint/SSL constraints.

## Going deeper
- No official `cloudflare` skill ref for this product — this file is the primary reference.
- Exact API (policies / destinations / available-alerts / history): Alerting v3 under
  `api.cloudflare.com/.../accounts/{account_id}/alerting/v3/` — exact endpoints sliced from the OpenAPI
  spec in `references/api/notifications.md` (verify shapes live).
- Webhook payload shapes per alert: `developers.cloudflare.com/notifications/reference/webhook-payload-schema/`.
- HTTP traffic alert internals: `developers.cloudflare.com/notifications/reference/traffic-alerts/`.
- Generic-webhook-via-Worker relay example: `github.com/cloudflare/cf-webhook-relay`.
