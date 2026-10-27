# Logs — detailed metadata logs (Logpush, Logpull, Instant Logs)

> Ship detailed request/event logs (HTTP, Firewall, Workers, Gateway, DNS...) out of Cloudflare for
> debugging, analytics, and SIEM. **Logpush** = batched push to storage/SIEM; **Instant Logs** =
> live tail in dashboard/CLI; **Logpull** = legacy pull REST API.

## Contents
- When to use (and when not)
- The three mechanisms
- Config (Logpush job)
- Datasets & destinations
- Key API / access patterns
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- **Ship request/event logs to external storage or a SIEM** → Logpush (R2, S3, GCS, Azure, Splunk,
  Datadog, Sumo Logic, SentinelOne, New Relic, Elastic, BigQuery, HTTP...). This is the main use.
- **Live-tail HTTP traffic** to investigate an attack / debug a config change right now → Instant Logs.
- **Pull request logs over HTTP into an origin pipeline** (legacy) → Logpull. Prefer Logpush/Logs Engine.
- **Not** for Workers application logs / `console.log` → use **Workers Logs / observability** (and
  `workers_trace_events` via Workers Logpush for shipping them out). Not for ad-hoc **in-dashboard querying** of
  stored logs → use **Log Explorer**. Not for **account change history** → use **Audit Logs**.
- These are metadata logs *about* traffic, not your app's stdout and not analytics aggregates.

## The three mechanisms
| | Logpush | Instant Logs | Logpull (legacy) |
|---|---|---|---|
| Model | Batched push (~once/min, no min batch) | Live WebSocket stream | Pull REST API |
| Destination | Storage / SIEM / HTTP | Dashboard or CLI (websocat) | Your HTTP client |
| Datasets | Many (zone + account) | HTTP requests only | HTTP requests only |
| Storage/search | None (delivery only) | None | None (7-day retention) |
| Plan | All plans, usage-based (since 2026-09-30) | Business + Enterprise | Enterprise |

## Config (Logpush job)
No Wrangler binding — Logpush is configured via dashboard or the REST API, per zone or per account.
```jsonc
// POST .../logpush/jobs  (zone-scoped dataset shown; account datasets use /accounts/{id})
{
  "name": "example.com",
  "dataset": "http_requests",
  "destination_conf": "r2://my-bucket/logs/{DATE}?account-id=<ID>&access-key-id=<K>&secret-access-key=<S>",
  "output_options": {
    "field_names": ["ClientIP","ClientRequestHost","EdgeResponseStatus","RayID","EdgeStartTimestamp"],
    "timestamp_format": "rfc3339",   // unixnano (API default) | unix | rfc3339 (dash default)
    "output_type": "ndjson",          // ndjson (default) | csv
    "sample_rate": 1.0                // 0.0 (excl) .. 1.0; 0.1 = 10% of records
  },
  "kind": "edge"                       // "edge" = Edge Log Delivery (http_requests only); omit for normal
}
```
`destination_conf` schemes: `r2`, `s3`, `gs`, `azure`, `https`, `sumo`, `splunk`, `sentinelone`,
`datadog`. `{DATE}` placeholder → `YYYYMMDD` daily subdirs (R2/S3/GCS/Azure). **Ownership must be
proven first** (`POST .../logpush/ownership` writes a challenge file to the destination; supply its
token on job create).

## Datasets & destinations
- **Zone datasets:** `http_requests`, `firewall_events`, `dns_logs`, `nel_reports`,
  `page_shield_events`, `spectrum_events`, `zaraz_events`.
- **Account datasets:** Zero Trust / Gateway (`gateway_dns`, `gateway_http`, `gateway_network`, `access_requests`,
  `dns_firewall_logs`), `workers_trace_events`, `audit_logs(_v2)`, `network_analytics_logs`,
  `casb_findings`, `dlp_forensic_copies`, `device_posture_results`, `email_security_alerts`, `email_security_post_delivery_events`,
  `firewall_events` and (new, 2026-10) **`http_requests`** — account-scoped twins of the zone datasets; the
  account `http_requests` page lists the **same 125 fields** as the zone one (incl. `ZoneName`) — no
  field difference documented — `websocket_analytics` (Enterprise), and more.
- **Pipelines is a native destination (2026-08-07)** — the analytics-shaped alternative to dumping raw
  JSON in a bucket. Logs go through a pipeline that filters/transforms them (Simple pass-through, or
  Custom SQL) and land as Parquet or Iceberg tables in **Basin Catalog**, compact and queryable with
  Basin SQL. The dashboard wizard provisions the whole chain in one pass (stream, sink, R2 credentials or
  catalog token, pipeline, Logpush job). **Only these datasets:** zone `http_requests`,
  `firewall_events`, `dns_logs` · account `workers_trace_events`. Reach for it when logs feed analytics;
  keep a plain R2/S3 destination when you just need raw archives.
  → `products/basin-pipelines.md`, `products/basin-catalog.md`, `products/basin-sql.md`
- Fields per dataset: `GET .../logpush/datasets/{dataset}/fields` (and `/fields/default`).
- **Custom fields** (HTTP requests only): request/response headers + cookies, for all zone http_requests jobs.

## Key API / access patterns
- **Manage jobs:** `POST/GET/PUT/DELETE .../logpush/jobs[/{id}]`. Token perm `Logs Write` — **all** Logpush
  API operations (including reads) require it, because jobs hold sensitive credentials; `Logs Read`
  only grants Logpull + Instant Logs.
- **Instant Logs (CLI):** `POST .../logpush/edge/jobs` with `"kind": "instant-logs"` → returns a
  `destination_conf` WebSocket URL; connect with `websocat wss://logs.cloudflare.com/instant-logs/...`,
  pipe NDJSON through `agrind` (Angle Grinder) for filter/aggregate.
- **Logs Engine** (`logs/list`, `logs/retrieve`, `logs/rayids`): store via Logpush→R2, then query R2
  by time range or RayID directly through Cloudflare's API. Being **replaced by Log Explorer**.
- **Filters / sampling:** `output_options.sample_rate` plus job `filter` (key/operator/value JSON).
  `"filter_attack_traffic": true` (2026-09-18) excludes identified DDoS attack traffic from
  `http_requests`, `firewall_events` and `network_analytics_logs` jobs.
- **Transformers (GA 2026-09-30, all plans):** one SQL query per job, run per record before delivery
  (`FROM http_requests`, field names from the dataset) to filter, reshape, redact or enrich. NDJSON
  jobs only; a job has **either a transformer or filters, not both** — via API, move the filter into
  the transformer's `WHERE`, then clear `filter` and set `transformer_id` in one update. Built and
  previewed in **Transformer Studio**.

## Gotchas
- **No backfill.** Logpush delivers each log once as it arrives; if a job is disabled or failing,
  those logs are **permanently lost**. Configure **Logpush health notifications**.
- **Drops on persistent destination failure:** retries have **no fixed attempt count** — Cloudflare
  retries a batch until it succeeds or the buffered data ages out of the internal retention window,
  then drops it (error `1201 FlushMaxLag`), permanently. **After 24 h with no successful delivery the
  job is auto-disabled**; re-enable it in the dashboard (no backfill).
- **PUT replaces `output_options` entirely** — omitted fields reset to defaults (e.g. dropping
  `timestamp_format` reverts to `unixnano` on API jobs). Always send the full object.
- **Push frequency is fixed (~1/min)** and not adjustable; `max_upload_bytes` / `max_upload_records` control batch *size*, not
  latency. Only **Edge Log Delivery** (`"kind":"edge"`, http_requests only) lets you set a max batch
  interval, between 30 s and 5 min.
- `sample_rate` stacks on top of any upstream `SampleInterval` (e.g. Network Analytics) — multiply them.
- **Logpull CMB limit:** unavailable when Customer Metadata Boundary is set to EU-only.
- **CVE-2021-44228 redaction** (`${`→`x{`) is API-only; editing the job in the dashboard resets it to false.

## Pricing & limits
> ⚠️ Verify on the live pricing page (`https://developers.cloudflare.com/logs/logpush/pricing/`) before quoting.
- **Logpush is usage-based on Free, Pro, Business and Enterprise** (2026-09-30; self-service below
  Enterprise). Per account per month: internal exports (R2, Pipelines) 25 GB included then
  **$0.03 / GB**; external exports (everything else) 25 GB then **$0.10 / GB**; Transformers input
  1 GB then **$0.04 / GB**. Measured on uncompressed bytes delivered. Doc example: 40 GB internal +
  60 GB external + 5 GB transformed = **$4.11**. **Existing Enterprise contracts** keep their pricing
  through renewal.
- **Workers Logpush** (**Workers Trace Events**) is unchanged: Workers Paid, 10 million requests/month
  included, then $0.05 per additional million. OpenTelemetry destinations keep Workers
  Observability event pricing (`products/observability.md`).
- **Logpull = Enterprise; Instant Logs = Business + Enterprise** (plan features, no meter). Destination
  costs (R2/S3 storage, SIEM ingest) are always extra.
- **Limits:** **4 Logpush jobs / zone**. Instant Logs: 1 active session/zone, max 60 min, auto-stops
  after 5 min of not reading the socket, HTTP-requests dataset only. `max_upload_records` default
  100,000 (Datadog auto-uses ~1,000). Logpull retention/RayID indexes expire after 7 days.

## Going deeper
- No official `cloudflare` skill ref for logs — this file is the primary reference.
- Full field tables per dataset → `docs-oficiais/pages/logs/logpush/logpush-job/datasets/`.
- Destination setup guides (each provider) → `.../logpush/logpush-job/enable-destinations/`.
- Output formatting (CSV, templates, prefixes) → `.../logpush/logpush-job/log-output-options/`.
- Related products: **Log Explorer** (in-dashboard store + query), **Workers observability/Logs**
  (app logs), **Audit Logs** (account changes), **Web Analytics** (privacy-first aggregates).
