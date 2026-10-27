# Email Service — send transactional email natively (Cloudflare RES)

> **Cloudflare CAN send email.** Email Service is Cloudflare's native transactional **sending**
> product (welcome mails, password resets, magic links, receipts, alerts). Reach for THIS, not
> Resend/SES/SendGrid/Postmark, when building on Cloudflare. Send from a Worker binding, a REST
> API, or authenticated SMTP. **Sending is in Beta** (Workers Paid).

## Contents
- When to use (and vs Email Routing / Email Workers)
- Binding & config (Workers)
- Send API (binding / REST / SMTP)
- Domain onboarding (required before you send)
- Key concepts
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- **Outbound transactional email** from a Cloudflare app: signup/welcome, password reset, email
  verification, magic links, 2FA codes, order/receipt confirmations, notifications, alerts.
- Agents that act over email (e.g. "email creates a ticket").
- Pairs with: Workers (compute), Queues (async/retry send pipelines), GraphQL Analytics API (metrics).
- **Don't** confuse with siblings under the same product:
  - **Email Routing** = *receiving/forwarding* inbound mail (`support@` → your inbox or a Worker).
    Free on all plans. The inbound counterpart — not for sending.
  - **Email Workers** = the inbound `email(message, env, ctx)` handler that runs a Worker on
    received mail (`message.forward()`, `message.reply()`, `message.setReject()`). Inbound only.
  - **Email Service Sending (this doc)** = *outbound* via the `send_email` binding / REST / SMTP.
- A Worker can do both: handle inbound in `email()` AND send outbound via `env.EMAIL.send()`.

## Binding & config (`wrangler.jsonc`)
```jsonc
{
  // Outbound sending — this is the one that SENDS email
  "send_email": [
    { "name": "EMAIL" },                                    // any verified destination
    { "name": "NOTIFY", "destination_address": "ops@you.com" }, // locked single recipient
    { "name": "TEAM", "allowed_destination_addresses": ["a@you.com","b@you.com"] },
    { "name": "RESTRICTED", "allowed_sender_addresses": ["noreply@you.com"] }
  ]
}
```
No restriction attr → may send to any verified destination. Restriction attrs limit senders/
recipients per binding. The `from` domain must always be a domain you onboarded (see below).
`destination_address` binding: `to` may be `null`/`undefined` → the configured address is used.

## Send API
**Workers binding (recommended, lowest friction):**
```ts
interface Env { EMAIL: SendEmail; }
const res = await env.EMAIL.send({
  to: "user@example.com",          // string | EmailAddress | array; combined to+cc+bcc ≤ 50
  from: "welcome@yourdomain.com",  // must be on an onboarded domain
  subject: "Welcome!",
  html: "<h1>Welcome!</h1>", text: "Welcome!",   // provide both for deliverability
  cc, bcc, replyTo,
  attachments: [{ content: "<base64>", filename: "invoice.pdf",
                  type: "application/pdf", disposition: "attachment" }],
  headers: { "List-Unsubscribe": "<https://you.com/unsub>" },
});
res.messageId; // unique id. Errors throw Error with .code (see Gotchas).
```
**REST API (any backend/serverless/CI — no Worker needed):**
`POST https://api.cloudflare.com/client/v4/accounts/{account_id}/email/sending/send`
with `Authorization: Bearer <API_TOKEN>` (token needs the **Email Sending: Edit** permission) and the same JSON
body (`to`/`from`/`subject`/`html`/`text`/`attachments`/`headers`) — but REST spells it `reply_to`
where Workers uses `replyTo`. Official SDKs: Node, Python, Go.

**SMTP** (any SMTP-capable app/client): `smtps://smtp.mx.cloudflare.net:465`, user
`api_token`, password = API token with **Email Sending: Edit** (implicit TLS/SMTPS, port 465 only;
587/STARTTLS and 25 are not supported for submission).

Legacy `EmailMessage` API (raw RFC 5322 MIME via `cloudflare:email` + `mimetext`, which needs the
`nodejs_compat` flag) still works for backward compat — prefer the structured `send()` for new code.

## Domain onboarding (required before you send)
You **cannot send from an unverified domain.** Dash → **Compute → Email Service → Email Sending →
Onboard Domain**. Cloudflare auto-adds DNS for auth on a **`cf-bounce.` subdomain**: MX (bounce
routing), SPF (`v=spf1 include:_spf.mx.cloudflare.net ~all`), DKIM (`cf-bounce._domainkey`), and
DMARC on `_dmarc`. Propagation usually 5–15 min on Cloudflare DNS. Sending records are **locked**
(managed by Email Service for the domain's lifetime). Note: sending uses the `cf-bounce` subdomain
and its own DKIM selector — **distinct from Email Routing's** root-domain records / `cf2024-1`
selector, so both can coexist on one domain.

## Key concepts
- **Verified destination addresses:** before onboarding a sending domain you can only send to
  destination addresses verified in your account (these sends are always **free**, don't count
  toward quota/limits, and allow up to 25 MiB). After onboarding a domain you can send to anyone.
- **Suppression list:** auto entries — `complaint` (no expiry), `hard_bounce` (7 days, or none if the
  mailbox/domain doesn't exist), `soft_bounce` (24 h default); plus `manual` (your expiry or none).
  Each has a **scope**: `account` (all sending domains) or `sending_domain` (that exact domain only —
  `mail.myappexample.com` ≠ `myappexample.com`). Suppressed sends show as **Rejected** in sending logs.
- **Observability:** sending metrics, logs, and audit logs in the dash; metrics also via the
  GraphQL Analytics API (`emailSendingAdaptive`/`...Groups`), retained 31 days. These are
  **zone-level** datasets — filter by `zoneTag` (zone ID, not account ID).

## Gotchas
- **Errors throw** — wrap in try/catch and branch on `error.code`. Key codes: `E_SENDER_NOT_VERIFIED`,
  `E_SENDER_DOMAIN_NOT_AVAILABLE` (domain not onboarded), `E_RECIPIENT_NOT_ALLOWED` (binding
  allowlist), `E_RECIPIENT_SUPPRESSED`, `E_RATE_LIMIT_EXCEEDED`, `E_DAILY_LIMIT_EXCEEDED`,
  `E_TOO_MANY_RECIPIENTS` (>50), `E_CONTENT_TOO_LARGE` (>5 MiB).
- **Worker-sent mail shows as "dropped" in the Email Routing summary even when delivered.** Track
  real send success via Email *sending* metrics/logs, not the Routing dashboard.
- **`From` and other platform headers can't be set via `headers`** (`E_HEADER_USE_API_FIELD`); use
  the dedicated `from` field. Only allowlisted/`X-` custom headers are accepted.
- `List-Unsubscribe` must be `<https://…>`/`<mailto:…>` (plain HTTP rejected); compliance is on you.
- **Since 2026-09-25 bounces/complaints suppress per `sending_domain`**, not account-wide (a complaint
  falls back to `account` if the domain can't be identified). Manual entries and API calls that omit
  `scope` default to `account`. Managing them needs **Email Sending: Edit**.
- **One suppressed recipient fails the whole send** unless the domain's **Drop suppressed recipients**
  setting (off by default) is on: REST `400`, binding throws `E_RECIPIENT_SUPPRESSED`, SMTP rejects.
  On, suppressed recipients are removed and the rest delivered.
- **Check `read_only` to know whether a suppression can be changed — never infer it from `reason`.**
  Cloudflare-managed `policy` entries can come back read-only; complaint entries are deletable when
  `read_only` is `false` (do it only after the recipient opts in again).

## Pricing & limits
> ⚠️ Beta — pricing/limits are still moving. Verify live: `developers.cloudflare.com/email-service/platform/pricing/`.

**Status:** Email **Sending = Beta** (`Workers Paid` only); Email **Routing** on Free and Paid (`email-service/platform/pricing/`).
**Cost drivers** (outbound sending, as of 2026-06):
- Workers Free: sending **not available**. Workers Paid: **3,000 emails/month included**, then
  **$0.35 / 1,000 emails**. Quota is per-account, per billing cycle.
- Accepted + hard-bounced emails count toward quota; API-rejected/suppressed sends and sends to
  **verified destination addresses** are **free** and don't count.
- Inbound (Email Routing): **unlimited/free**; Email Workers billed under normal Workers pricing.

**Key limits:** recipients (to+cc+bcc) **50/email** · total message **5 MiB** (25 MiB to verified
destinations) · subject **998 chars** · custom headers **16 KB** total, ≤20 non-`X-` headers,
attachments ≤32 · domains/zone **30** · suppression API: `per_page` ≤1,000, import ≤1,000 items,
10 imports/min · daily quota starts low, auto-scales (request increases via
the [Limit Increase form](https://forms.gle/eX6pXvit1wBv77Yw5)). Verify on
`developers.cloudflare.com/email-service/platform/limits/`.

## Going deeper
- Official `cloudflare` skill ships `cloudflare-email-service` — use it for full API/patterns.
- Examples: magic-link, signup flow, attachments, recipients → `email-service/examples/email-sending/`.
- REST OpenAPI: `developers.cloudflare.com/api/resources/email_sending/methods/send/`.
- Concepts: deliverability, email-authentication, suppression triggers/expiry under
  `email-service/concepts/`. Managing the list (dashboard, CSV/JSON/TXT import, API) lives at
  `email-service/configuration/suppressions/`.
