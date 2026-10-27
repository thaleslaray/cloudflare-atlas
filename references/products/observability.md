# Cloudflare Observability — logs, traces, OTel export and one pricing model

> New top-level hub (`/observability/`, 2026-10) that unifies **Logs** (Workers, Containers, R2, AI
> Gateway, Issues, plus Log Explorer datasets), **Cloudflare Traces** (per-domain request tracing
> through Rules/Cache/Workers/origin), **OpenTelemetry export**, and a **single ingestion + storage
> pricing model from 2026-12-01**. Workers-specific setup still lives under `workers/observability/`.

## Contents
- What is genuinely new vs. a hub
- When to use (and when not)
- Workers config (`wrangler.jsonc`)
- Cloudflare Traces (domain-level)
- Logs & datasets
- OpenTelemetry export
- Workers Issues
- Gotchas
- Pricing & limits
- Going deeper

## What is genuinely new vs. a hub
- **New:** **Cloudflare Traces** — production traces of real requests on a *domain* (not just a
  Worker), with spans for rulesets, routing, cache, Workers and origin; **unified pricing** for all
  logs + traces; **account-level OTel destinations** shared by Cloudflare Traces and Workers; the
  **Logs** query UI over one dataset selector.
- **Hub (points elsewhere):** Workers Logs, Workers Traces, Workers Issues, OTel config for a Worker
  (`workers/observability/…` → `products/workers.md`), Analytics + Custom Dashboards
  (→ `products/analytics.md`), alerts (Notifications), Logpush and Log Explorer (→ `products/log-explorer.md`).
- **Renamed path:** the old Workers "exporting OpenTelemetry data" page now **301s to**
  `/observability/export/opentelemetry/` (measured 2026-10-03); the Worker-side config page is
  `workers/observability/opentelemetry-export/`.

## When to use
- "Why was this request slow/blocked/rewritten?" across WAF, Transform Rules, Snippets, cache and
  origin → **Cloudflare Traces** (filter on the Ray ID).
- Query structured events from Workers/Containers/R2/AI Gateway/Zero Trust in one place → **Logs**.
- Ship telemetry to Honeycomb/Grafana/Datadog/Sentry/etc. → **OpenTelemetry export**.
- Worker failures that recur, grouped and routed to a team or coding agent → **Workers Issues**.
- **Not** a simulation: **Cloudflare Trace** (`rules/trace-request/`) *simulates* how config would
  handle a request; **Cloudflare Traces** records actual production traffic.

## Workers config (`wrangler.jsonc`)
```jsonc
"observability": {
  "traces": { "enabled": true, "destinations": ["tracing-destination-name"], "head_sampling_rate": 0.05, "persist": false },
  "logs":   { "enabled": true, "destinations": ["logs-destination-name"],    "head_sampling_rate": 0.6,  "persist": false },
  "issues": { "enabled": true }   // Workers Issues — needs Wrangler 4.134.0+
}
```
- `destinations` must match names created in the dashboard (**Observability › Destinations**).
- `persist` defaults to **`true`** (export *and* store in Cloudflare). Set `false` to export only.
  Redeploy after changing; events can take several minutes to reach the destination.

## Cloudflare Traces (domain-level)
- **Enable per domain.** Settings: **Default sample rate (%)** (head sampling); **Trace rules**
  override it for matching requests — **first match wins**, so order matters (custom filter in the
  Rules language, or *All incoming requests*; *Save as Draft* vs *Deploy*).
- **Persist to Cloudflare** (view in dashboard) and/or **Export destinations** (OTel). Turn persist
  off to keep traces only in your external tool.
- **Trace context (W3C):** *Incoming trace context* defaults to **Reject**; if you accept it, treat
  the joined trace as untrusted (not verified). **Forward to origin** passes context so an
  instrumented origin can join the trace — it does not create origin spans by itself.
- **Spans:** root `cloudflare_request`; `response`, `workers_routing`, `page_rules`, `cache`,
  `dynamic` (uncached fetch incl. full body — not just origin think-time), `upstream` (**Tiered Cache**);
  ruleset phases such as `http_request_firewall_custom`, `http_request_transform`,
  `http_request_cache_settings`, `http_request_snippets`, `http_response_compression`. A skipped
  phase emits no span. Worker spans appear only if **Workers tracing** is enabled.

## Logs & datasets
- Query by field filters, the filter language or **SQL** against the selected dataset; charts
  (Stat → Sankey → Table), intervals 1 minute–1 day, anomaly drill-down, add to a custom dashboard.
- **Pooled-allowance datasets (7-day default retention):** `workers`, `containers`, `r2` (R2 Data
  Access Logs, on bucket), `ai-gateway`, `real-time-issues` (Issues).
- **Unsampled security datasets** (legacy Log Explorer, 30-day): e.g. `http_requests`,
  `firewall_events`, `dns_logs`, `audit_logs_v2`, `gateway_http`, `zaraz_events` — enabled on account
  via Log Explorer. Full list with event sizes: `observability/logs/datasets/`.
- **Custom Dashboards (changelog 2026-10-02):** two datasets, **Workers Observability — Logs** and
  **Workers Observability — Traces (OTel)**, chart invocations, levels, errors, CPU/wall time, spans
  and durations next to HTTP/security analytics. Need Workers Logs or Workers Traces turned on; follow
  the underlying retention (older ranges return no data). Up to **100 dashboards per account**.

## OpenTelemetry export
- Exports **Cloudflare Traces**, **Workers Traces**, **Workers Logs** over OTLP. Create an
  account-level destination (name, *Traces* or *Logs*, OTLP endpoint, custom auth headers), then
  attach it per domain (Traces) or per Worker (`destinations`).
- **No binary protobuf** OTLP encoding. Workers infrastructure metrics and custom metrics **cannot**
  be exported.
- Provider endpoints (traces/logs): Honeycomb `https://api.honeycomb.io/v1/traces` (header
  `x-honeycomb-team`), Axiom `https://api.axiom.co/v1/traces` (`Authorization: Bearer` + `X-Axiom-Dataset`),
  Sentry (`x-sentry-auth`), Grafana Cloud (`/otlp/v1/traces`), Datadog, New Relic, Firetiger,
  Sematext, SigNoz, Splunk. **PostHog = logs only**; **Splunk Observability** = traces only.
- Status: **Last: n minutes ago** / **Never run** (check traffic, export settings, sampling) /
  **Error** (check endpoint + auth headers).

## Workers Issues
- Built-in error monitoring, no SDK: uncaught exceptions, failed invocations, `5xx` returned by the
  Worker, and error-level logs become **occurrences**, grouped per Worker into **issues**.
- Statuses `Active` / `Resolved` (reopens on a newer occurrence) / `Ignored`; never auto-resolves.
  Occurrence details kept **7 days**. Only new traffic is processed (no backfill).
- Add context with `tracing.getActiveSpan()?.setAttribute(...)` from `cloudflare:workers` (tracing on).
- **Automations:** trigger on *occurrence threshold* (runs once) or *recurrence after inactivity*;
  destinations Coding agent (Claude Code, Cursor, Devin), Generic webhook (secret or mTLS), Chat,
  Incident management; up to **3** hand-off attempts per run.

## Gotchas
- **Dashboard-enabled Issues get turned off by the next `wrangler deploy`** unless
  `observability.issues.enabled` is also set to `true` in the Wrangler config.
- **Creating a destination exports nothing** until you attach it to a domain or a Worker.
- **`persist: true` is the default** — exporting to a vendor *and* storing in Cloudflare will count
  toward Cloudflare Observability usage from 2026-12-01.
- An automation does **not** grant the agent access to your account — use the Workers Observability
  MCP server for that, and never put secrets in span attributes/logs.

## Pricing & limits
> ⚠️ Announced model, effective **2026-12-01** (Enterprise: at contract renewal). Until then Workers
> Logs keeps its current pricing (Free 200,000 events/day, 3 days; Paid 20M/month + $0.60/M, 7 days).
> Verify on `developers.cloudflare.com/observability/pricing/` before quoting.
- **Cost drivers:** GB **ingested** (pre-compression, incl. enriched + custom attributes; dropped
  events excluded) and GB-month **stored** (sum of daily max queryable GB / 30). Queries,
  dashboards, alerts and analytics are free. Sampling lowers both meters.
- **Free:** 0.5 GB/day ingestion, 7-day retention; ingestion stops at the cap, resets 00:00 UTC.
- **Paid:** 50 GB ingestion + 10 GB-month storage per billing cycle, then **$0.25/GB** and
  **$0.10/GB-month**; meters are separate and do not roll over. Docs example: 75 GB + 20 GB-month → $7.05.
- **Unsampled security datasets** (the legacy Log Explorer datasets): **$1/GB ingested**, 30-day retention,
  outside the pooled allowance.
- Configurable 30/90/365-day retention is planned, not available.

## Going deeper
- Live docs: `https://developers.cloudflare.com/observability/` (logs, traces, export, pricing).
- Worker side: `workers/observability/opentelemetry-export/`, `workers/observability/issues/`.
- The official `cloudflare` skill `references/observability/` (if installed) covers Workers Logs/
  Traces/Analytics Engine/Logpush patterns — it predates Cloudflare Traces, Issues and the new pricing.
