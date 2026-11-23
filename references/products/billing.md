# Billing — plans, subscriptions & payment for your account

> Account management, not a build product. Manage plans, subscriptions, payment methods,
> invoices, and usage-based spend for a Cloudflare account — via the dashboard or the
> Billing API. No Worker bindings.

## Contents
- When to use (and when not)
- Billing model (how charges work)
- Spending limits & email alerts (Workers, Durable Objects)
- Roles & permissions
- API / programmatic access
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- Query or manage **account billing**: view/download invoices, pay outstanding balances, change
  domain plans, cancel subscriptions, add/update payment methods, monitor usage-based spend, cap Workers/DO spend (spending limits).
- Programmatically read plan/subscription/usage data via the **Billing API** (Account → Billing
  permission). Use for cost dashboards, automated invoice retrieval, spend reporting.
- **Not** a deployable product — there are no bindings and nothing to wire into a Worker.
- For per-product cost numbers (Workers, R2, etc.), see that product's own pricing page; this
  reference covers the account-level billing mechanics only.

## Billing model (how charges work)
- **Billing cycle:** every 30 days (monthly plans) or 365 days (annual). First paid purchase sets
  the monthly billing date; annual subs follow their own cycle. All dates are **UTC**.
- **Three charge types on an invoice:**
  - *Plan charges* — flat-rate, billed **in advance**, **per domain** (Free/Pro/Business/Enterprise).
  - *Subscription / add-on charges* — flat-rate, billed in advance (Load Balancing, Argo, etc.).
  - *Usage-based charges* — metered, billed **in arrears** for the period that just ended.
- **Usage-based (metered) products:** Workers, R2, Argo Smart Routing, Cache Reserve, Load
  Balancing, Stream, Images, Spectrum, Rate Limiting, Log Explorer, Zero Trust, Vectorize,
  Analytics Engine. Most include a free tier; you pay only for overage.
- **Upgrades** apply immediately (prorated charge + credit for unused lower plan). **Downgrades /
  cancellations** apply at end of the billing period — no refund for remaining time.
- **Failed payment:** 5-day grace period, up to 5 automatic retries; while unpaid you cannot buy or
  modify subscriptions. Unresolved → account downgraded to Free (sites stay up; paid features lost).

## Spending limits & email alerts (Workers, Durable Objects) — changelog 2026-11-13
Only **Workers** and **Durable Objects** today ("more products coming soon"). API name: **spend policy**.
- **Limit** (`--action usage_block`): at the threshold Cloudflare blocks the product's supported operations until the next
  billing period or until you change it. **Email alert** (`--action notification`): emails at 80% and 100%; product keeps running.
  Several alerts allowed (also beside a limit); **one enabled limit per product** (else `409`).
- Scope = whole account, per product: cannot target one Worker, DO namespace or metric. A Workers limit does not cover DO, Workers AI, KV, R2.
  A test Worker hitting the shared limit can take down a production Worker.
- Counted: estimated usage charges this billing period, after included usage, USD. Workers = requests + CPU time; DO = requests, duration,
  SQLite rows read/written, KV-storage ops. Excluded: Workers Paid fee, other products, DO stored data.
- Dashboard: Billing → **Spend Management** → Workers/DO row → **Edit the spending limit** → **Monthly limit (USD)** > 0, 2 decimals; saving turns it on.
  Dashboard-created limits have **no email recipient** — add `notification_email` via update. Needs permission to edit billing settings.
- **cf CLI** (`cf billing spend-policies` (subcommands `create`, `list`, `get`, `update`, `delete`, `activity`, `audit`)): required `--name` (≤200 bytes), `--product-id` (`workers` or `durable_objects`),
  `--enabled`, `--threshold-cents` (positive int; 5000 = $50), `--action`; optional `--notification-email` (required for alerts); `--dry-run` previews.
  Update replaces the whole policy and needs `--if-match <version>` (stale → `412`, missing → `428`). Token: Account → Billing → Read (inspect) / Edit (change).
- Not a hard cap: metering delay, in-flight operations and enforcement failures can overshoot. Saving a limit below current spend can pause at once.
- Lift: raise above current spend, turn **Off**, or **Remove limit** (a few minutes; toggling doesn't reset spend). Block expires at the next
  subscription billing period (renewal date, not calendar month); an enabled limit stays configured.
- History: dashboard Audit log panel + account Audit Logs; `activity` (config changes), `audit` (80%/100% events `approaching_limit`/`limit_reached`; no pagination, gone after delete; `--limit` max 100).
- Budget alerts are separate and never block. AI Gateway has its own per-user/model spend limits (`ai-gateway.md`). Docs state no plan requirement.

## Roles & permissions
Dashboard access depends on account role:
- **Super Administrator** — full billing control (pay, payment methods, subscriptions, plans, members).
- **Administrator** — view invoices/usage, set budget alerts, change/cancel subscriptions & plans;
  **cannot** manage payment methods or pay balances.
- **Billing** — view & pay (invoices, payment methods, balances, budget alerts); **cannot** change
  subscriptions or plans.
> No single non-Super role can both manage subscriptions *and* handle payments.

## API / programmatic access
There is no Worker binding. Use the **Cloudflare REST API** with an API token scoped to
**Account → Billing → Read** (or **Edit**):
- Create token: My Profile → API Tokens → Custom token → Account → Billing → Read/Edit.
- Endpoints live under the account/user billing namespace in the API reference
  (`developers.cloudflare.com/api/` — billing profile, subscriptions, plan/usage data).
- Same operations are available in the dashboard under **Manage Account → Billing**, organized as
  four tabs: **Invoices and documents**, **Billable Usage**, **Payment**, **Subscriptions**.

## Gotchas
- **No refunds.** Cancelling mid-period bills the full period; there's a minimum one-month obligation.
- **Per-domain plan billing** — 20 domains on Pro = 20× the plan fee on one line item.
- **Zero-amount line items are normal** — each billable dimension (e.g. R2 storage / Class A / Class B)
  shows even at $0.00; it confirms the product is active.
- **Make plan changes ≥24h before the billing date** (UTC) to avoid timing issues.
- **"Cannot remove payment method"** while it's linked to active subscriptions or has a pending
  transaction (e.g. Registrar renewal within 24h) — cancel subs or add a replacement first.
- **Outstanding balance locks the account** — no new purchases or subscription edits until paid.
- **Budget alerts** track **account-wide dollar spend**; **usage notifications** track a single
  product metric (bytes/requests/minutes) — use the right one. Budget alerts are **Pay-as-you-go
  only** (not Enterprise contract accounts) and are informational — they never pause or cap usage (to block, use a Workers/DO spending limit above).

## Pricing & limits
> ⚠️ Billing has no fee of its own. Per-product rates change — verify on the live pricing page
> (`developers.cloudflare.com/<product>/pricing/` or `cloudflare.com/plans/`) before quoting.
- **Cost drivers** are per-product (requests, GB stored/egressed, operations, minutes, seats…) — see
  each product's reference. Account-level: domain **plan fees** (per domain) + add-on subscriptions.
- **Payment methods:** Visa, Mastercard, Amex, Discover, UnionPay; PayPal; Apple Pay, Google Pay,
  Stripe Link; Instant Bank Payments via Link (US self-serve); stablecoin (where available).
- **Grace period:** 5 days / 5 retries on failed payment before downgrade to Free.

## Going deeper
- No official `cloudflare` skill ref for billing. Source: `developers.cloudflare.com/billing/`
  (`understand/how-billing-works`, `understand/billing-permissions`, `understand/usage-based-billing`,
  `manage/budget-alerts`, `manage/spend-management/` (+`cli/`), `troubleshoot/error-reference`).
- Billing API: `developers.cloudflare.com/api/` → Account → Billing.
- Sales tax, billing policy/refunds, and per-product cost optimization live under
  `billing/understand/` and `billing/manage/optimize-costs/`.
