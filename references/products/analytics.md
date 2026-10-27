# Analytics — query Cloudflare metrics (GraphQL API + Workers Analytics Engine)

> Visualize and query the performance, security, and reliability metadata Cloudflare collects.
> Three programmatic surfaces: the **GraphQL Analytics API** (cross-product CF metrics), the **SQL API**
> (the same analytics + observability datasets in SQL, also from a Worker binding) and **Workers
> Analytics Engine** (write custom, unlimited-cardinality metrics from a Worker, query with SQL).

## Contents
- When to use (and when not)
- The landscape (which surface for what)
- Binding & config (Analytics Engine)
- Access patterns
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- **Query Cloudflare's own product metrics** (HTTP requests, bandwidth, WAF/firewall events, cache,
  DNS, Load Balancing, Workers) programmatically → **GraphQL Analytics API**. Powers the dashboard.
- **Cross-product data from one endpoint** — select exactly the metrics you need, filter/group by
  dimension, aggregate per-zone or per-account → **GraphQL Analytics API** (70+ datasets).
- **Custom metrics from your own Worker** (usage billing, per-customer health) → **Workers Analytics Engine**.
- **Not** for billing-grade usage numbers (GraphQL counts all measurable traffic incl. mitigated DDoS;
  it is not the billing meter). **Not** for raw logs (→ Logs / Logpush) or live tail (→ Instant Logs).

## The landscape (which surface for what)
| Surface | Writes? | Query | Use it for |
|---|---|---|---|
| **GraphQL Analytics API** | no (CF-generated) | GraphQL, one endpoint | CF product metrics, dashboards, cross-product reports |
| **SQL API** | no | one `SELECT` per request, or `env.<BINDING>.query()` | CF analytics, Workers logs, Log Explorer and WAE datasets in SQL |
| **Workers Analytics Engine (WAE)** | `writeDataPoint()` from Worker | SQL API (or GraphQL) | your own high-cardinality custom metrics |
| Web Analytics, Account/Zone, Network Analytics | — | dashboard UI | privacy-first site stats, traffic overview, L3/L4 + DDoS |

GraphQL endpoint (`POST`, query as JSON body): `https://api.cloudflare.com/client/v4/graphql`.
SQL API endpoint (`GET` or `POST`): `https://api.cloudflare.com/client/v4/analytics/sql` (catalog: `/analytics/sql/introspection`).
WAE SQL endpoint: `POST .../accounts/{account_id}/analytics_engine/sql`.

## Binding & config — Workers Analytics Engine (`wrangler.jsonc`)
```jsonc
{
  "analytics_engine_datasets": [
    { "binding": "WEATHER", "dataset": "weather_data" }
  ]
}
```
Datasets auto-create on first write — no dashboard step. Write from a Worker:
```js
env.WEATHER.writeDataPoint({
  blobs: ["Seattle", "USA", "sensor_9000"],  // strings: dimensions to filter/group by
  doubles: [25, 0.5],                         // numbers: the values you measure
  indexes: ["customer_a3cd45"],               // single string: the sampling key
});
```
`writeDataPoint()` returns void immediately (fire-and-forget; do **not** await). Query later:
```sql
SELECT blob1 AS city, SUM(_sample_interval * double2) / SUM(_sample_interval) AS avg_humidity
FROM weather_data WHERE double1 > 0 GROUP BY city ORDER BY avg_humidity DESC LIMIT 10
```

## Access patterns
- **GraphQL** — pick dataset → metrics (sum/avg/count) → filter + group by dimensions (incl. time).
  Auth with a zone/account-scoped API token; introspect the schema to discover fields.
- **Analytics Engine SQL** — `curl` the SQL endpoint with an `Account Analytics Read` token; integrates with
  Grafana for time-series. Round `timestamp` then `GROUP BY` it for time buckets.
- **WAE via GraphQL** — same dataset is also queryable through the GraphQL API (dashboard parity).
- **SQL API** — every query needs an account or zone scope, a lower `timestamp` bound, and exactly
  one schema-qualified dataset: `events.` (sampled events, e.g. `events.httpRequests`), `states.`, or
  `logs.` (e.g. `logs.workersLogs`, Log Explorer). WAE datasets appear as
  `events.analyticsEngine.<DATASET_NAME>` (account scope only). Token: **Account Analytics Read**
  (or **Zone Analytics Read** per named zone). Discover datasets with the introspection endpoint —
  the catalog varies per account, don't hard-code it. CLI: `cf sql query`, `cf sql datasets`.
- **SQL API from a Worker** — `"analytics": { "binding": "ANALYTICS_SQL" }` (Wrangler **4.145.0+**),
  then `await env.ANALYTICS_SQL.query({ query, params: { start } })`; scoped to the Worker's account,
  no API token. Limits: 1 statement, 10 KiB, 1 dataset and 1 account per statement, `ORDER BY` needs
  `LIMIT` (except WAE); overload returns `429`/`507`/`503` — honor `Retry-After`.

## Gotchas
- **Sampling (ABR):** both surfaces sample. Always weight aggregates by `_sample_interval` in WAE SQL
  (`SUM(_sample_interval * x)`), else counts/sums under-report. CF stores data at 100%/10%/1% and picks
  a resolution by query cost. Don't treat sampled numbers as exact event counts.
- **WAE `indexes` is a single value** — the array accepts one entry; passing multiple silently drops
  the data point. It's the sampling key, not a free dimension (use `blobs` for those).
- **WAE blobs vs doubles:** blobs = strings (dimensions), doubles = numbers (measures). Ordered arrays —
  keep field order consistent across writes (`blob1`, `double1`… map by position).
- **No custom timestamps in WAE** — every point is auto-stamped at write time; you can't backfill.
- **GraphQL is not a billing meter** — includes mitigated/DDoS traffic that billing excludes.
- **30 days on every plan (2026-10-02):** adaptive datasets (HTTP requests, security events, DNS)
  retain at least 31 days for Free and Pro domains, queryable up to 30 days per request (was 24 h–8 d).
  Aggregated datasets like `httpRequests1hGroups` keep their per-plan limits — check the `settings`
  node. Account-level analytics moved to **Observability** > **Analytics** in the dashboard.
- **Custom Dashboards** now chart Workers Observability logs and traces (2026-10-02) — see
  `products/observability.md`.
- **GraphQL `filter` + `limit` are often required** per node; missing them returns errors or empties.
  A 200 response can still carry an `errors` array — check it. CMB (Customer Metadata Boundary) region
  mismatches surface as "data unavailable".

## Pricing & limits
> ⚠️ Pricing changes — verify live (`developers.cloudflare.com/analytics/analytics-engine/pricing/`)
> before quoting. WAE billing is announced but **not yet charged** ("Currently, you will not be billed",
> pricing page re-checked 2026-10-03).

**Workers Analytics Engine** — priced on two metrics (each data point and each read query cost the
same; no surcharge for cardinality/complexity):
- **Workers Paid:** 10M data points written + 1M read queries / month included; +$0.25 / additional
  million written, +$1.00 / additional million read.
- **Workers Free:** 100,000 written + 10,000 read queries **per day**.
- WAE limits: ≤20 blobs, ≤20 doubles, **1 index** per point · blobs ≤16 KB/point · index ≤96 bytes
  · ≤250 data points per Worker invocation · **3-month** retention.

**GraphQL Analytics API** — no separate charge (access tied to your plan). Limits:
- ≤10 zones per zone-scoped query · 1 account per account-scoped query.
- **300 queries / 5-min window** per user (≈1 q/s sustained), on top of general API rate limits.
- Per-node limits (history depth, max time range, fields, rows) vary by **plan** and dataset — higher
  plans unlock more datasets/fields/history. Check the `settings` discovery node for exact bounds.

## Going deeper
- **GraphQL Analytics API** → official `cloudflare` skill `references/graphql-api/`
  (`api.md`, `patterns.md`, `gotchas.md`) — full schema/query patterns. Don't duplicate here.
- **Workers Analytics Engine** → official `cloudflare` skill `references/analytics-engine/`
  (`api.md`, `patterns.md`, `gotchas.md`) + docs `analytics-engine/sql-reference/`, `grafana/`.
- Dashboard-only surfaces (Account/Zone, Network, Web Analytics) live under
  `developers.cloudflare.com/analytics/types-of-analytics/`.
