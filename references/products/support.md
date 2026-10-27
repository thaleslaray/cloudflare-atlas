# Support — how to get help from Cloudflare

> Meta/process reference (NOT a build product): how to reach Cloudflare Support, what each plan
> gets, how to open a ticket, and SLAs. Use this to route a user to the right help channel.

## Contents
- When to use
- Support channels by plan
- Opening a support case
- SLAs & priority
- Gotchas
- Status & escalation

## When to use
- A user asks "how do I contact Cloudflare?", "what support does my plan include?", "site is down,
  how do I escalate?", or "how do I open a ticket / add a teammate to my case?".
- **Not** for product how-to or debugging — those live in the per-product references. Support here
  means the *help process itself*: channels, plans, ticketing, SLAs, status.

## Support channels by plan
| Channel | Free | Pro | Business | Enterprise |
| --- | --- | --- | --- | --- |
| Community forum + Discord | ✅ (recommended) | ✅ (recommended) | ✅ | ✅ |
| Support case (ticket) | billing/account/registrar only | ✅ | ✅ | ✅ |
| Live chat | ❌ | ❌ | ✅ | ✅ |
| Emergency phone | ❌ | ❌ | ❌ | ✅ |

- **Free**: self-serve — Community (`community.cloudflare.com`) + Discord (`discord.cloudflare.com`).
  Tickets only for billing/account/registrar.
- **Live chat** (Business/Enterprise): quick questions, no deep investigation. Support → **Chat with a human** tile.
- **Emergency phone** (Enterprise only): outages / active attacks. Requires identity verification
  (single-use dashboard token refreshing every 30s, or authenticator-app TOTP) + your **Unique Customer ID**.

## Opening a support case
All in the dashboard — there is **no public REST API for submitting tickets**. Go to
`dash.cloudflare.com/?to=/:account/support` → **Technical Support** (or **Billing** → **Create a Case**).
- Pick category/subcategory, affected domains, write a detailed summary.
- Include: **timestamp (UTC)**, Zone name/ID, frequency, repro steps, exact error messages, expected
  vs actual, HAR file, screenshots, origin logs, MTR/traceroute/dig/cURL output, priority + impact, CC'd collaborators.
- **My Cases** tile → view your + CC'd cases; add teammates via the `Case Participants` box.
- Attachments: png/jpg/gif/ico/tiff, mp4/avi/webm, har/txt/csv/eml/css/html/json/tf, pcap/pcapng/cap.
  Max **20 MB** (link to Drive for bigger). No ZIP/RAR, no DOCX/XLSX/PPTX.

## SLAs & priority
Priority is set by *you* on the case (P1 Urgent → P4 Low) and gated by plan. Cases are worked in order:
Premium Ent → Standard Ent → Business → Pro → Free.
- **Premium SLA**: P1 1h · P2 2h · P3 24h · P4 24h.
- **Enterprise SLA**: P1 2h · P2 4h · P3 48h · P4 48h.
- **Pro / Pay-as-you-go / Free**: no SLA — answered in arrival order; use Community for speed.
- Times are *initial response*, not resolution. State priority + production impact explicitly.

## Gotchas
- Support **cannot** make config/account changes for you, debug your code's logic, or discuss domains
  not tied to your account email. **Never share** passwords, card numbers, private keys, or API keys.
- Support is **English-only** across cases, chat, and phone (worldwide regions covered).
- Free-plan technical issues → Community, not tickets.
- Check the status page **before** filing — many "outages" are known incidents.

## Status & escalation
- Live status: `www.cloudflarestatus.com` — and a machine-readable **Status API** at
  `www.cloudflarestatus.com/api`. Incidents and maintenance are **separate feeds**, each in RSS and Atom:
  `/api/v3/incidents.rss|.atom` e `/api/v3/maintenance.rss|.atom`.
- Duas vias de notificação: **status page notifications** (email, webhook, Slack, Discord, Google Chat —
  entregues fora da infra da Cloudflare, disparam mesmo se a Cloudflare estiver fora) e **Cloudflare
  Notifications** na conta (**Incident Alerts** + **Maintenance Notification**, via email/Webhooks/PagerDuty).
- **Locations view** (`www.cloudflarestatus.com/locations`): cada data center como *Operational*,
  *Re-routed* or *Partially Re-routed* (a POP pulled for maintenance shows as *Re-routed*).
- Disruptive/scheduled maintenance is announced under `developers.cloudflare.com/support/disruptive-maintenance/`.
- Full source: `docs-oficiais/full/support.md`; troubleshooting how-tos under
  `pages/support/troubleshooting/` (HTTP status codes, 1xxx/5xx Cloudflare errors, restoring visitor IPs).
- ⚠️ Plan entitlements and SLA numbers change — verify on
  `developers.cloudflare.com/support/contacting-cloudflare-support/` before quoting.
