# Log Explorer — native log storage + SQL search in the Cloudflare dashboard/API

> Store Cloudflare logs on Cloudflare's network and query them with SQL — in the dashboard or API —
> **without forwarding to an external SIEM**. Cloudflare's native observability/forensics product.

## Contents
- When to use (and when not)
- vs Logpush / vs Trace
- Enable datasets (config)
- Query patterns (SQL API)
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- Investigate **real production traffic** after the fact: security incidents, forensics, anomaly hunting.
- Search patterns across thousands/millions of requests; analyze historical trends; monitor perf over time.
- You want logs queryable **natively in CF** — no data pipeline, no third-party storage, no ingest lag.
- Pairs with: Security Analytics (filters carry over into Log Explorer), Custom Dashboards.
- **Not** for: shipping raw logs to your own SIEM / data lake (→ **Logpush**); testing a hypothetical
  request against your rules (→ **Trace** / rules trace, which is "what-if", not actual traffic);
  long-term cheap archival you control (Logpush → R2/your bucket).

## vs Logpush / vs Trace
- **Logpush** delivers *raw* logs to third-party SIEMs/storage; Log Explorer *stores + queries* logs
  inside Cloudflare. You generally **don't need both** — but some use Log Explorer for fast
  investigation and Logpush for long-term retention / external integration.
- **Trace** simulates a request to show rule evaluation order ("what would happen?"). Log Explorer
  shows what *actually* happened. Use Trace to debug why a rule didn't fire; Log Explorer to find the
  request that hit it.

## Enable datasets (config)
No Worker binding. Since 2026-10-07 the dashboard **Log Explorer** menu is gone: datasets are queried on
**Observability → Logs** (shared with Workers Observability); manage them via the dataset selector →
**Configure**. The old Log Search page still works at its direct URL. You enable per-dataset ingestion there
or API. Ingestion starts at enable time — **no backfill** of prior events.

```bash
# Zone-level dataset
curl https://api.cloudflare.com/client/v4/zones/{zone_id}/logs/explorer/datasets \
  --header "Authorization: Bearer <API_TOKEN>" \
  --json '{ "dataset": "http_requests" }'

# Account-level dataset — swap zones/{zone_id} for accounts/{account_id}
curl https://api.cloudflare.com/client/v4/accounts/{account_id}/logs/explorer/datasets \
  --header "Authorization: Bearer <API_TOKEN>" --json '{ "dataset": "access_requests" }'
```

**Datasets** (subset): zone — `http_requests`, `firewall_events`, `dns_logs`, `page_shield_events`,
`spectrum_events`, `zaraz_events`, `nel_reports`. account — `access_requests`, `gateway_dns`,
`gateway_http`, `gateway_network`, `audit_logs`(`_v2`), `casb_findings`, `email_security_alerts`,
`network_analytics_logs`, `dns_firewall_logs`, `zero_trust_network_sessions`, and more.

**Ingest Field Selection** (since 2026-03-11): pick which fields of a dataset are ingested/stored,
at enable time or later on an already-enabled logstream; disabled fields stay queryable for the period
they were captured, and core fields like `Timestamp` are always kept. Fewer fields = smaller bill.

**Permissions** (account or zone scope): Logs Edit = manage datasets · Logs Read = query · Logs Write =
save queries · Analytics Read = custom dashboards. Auth via API token or API key + email.

## Query patterns (SQL API)
SQL `query/sql` endpoint; the dashboard's **Custom SQL** mode runs the same queries.

```bash
curl https://api.cloudflare.com/client/v4/zones/{zone_id}/logs/explorer/query/sql \
  --header "Authorization: Bearer <API_TOKEN>" \
  --url-query query="SELECT clientRequestHost, edgeResponseStatus FROM http_requests \
    WHERE RayID = '806c30a3cec56817' LIMIT 1"
```

- **Supported SQL:** `SELECT [DISTINCT]`, `FROM`, `WHERE`, `GROUP BY`, `ORDER BY`, `LIMIT`, `OFFSET`.
  Functions: `COUNT`/`SUM`/`AVG`/`MIN`/`MAX` (incl. `COUNT(DISTINCT …)`), `SUBSTRING`/`LOWER`/`UPPER`,
  `ARRAY_CONTAINS`. Expressions: `CASE WHEN`, `AS`, `LIKE`, `IN`, `BETWEEN`, arithmetic/logical/bitwise
  operators, `||` concat.
- **Headers/cookies** are NOT queryable until you log them via [Custom fields] — then query e.g.
  `requestheaders."x-test-header" LIKE '%…%'` (configure custom fields without touching a Logpush job).
- Output column names come back **lowercased** regardless of how you cased them in `SELECT`.

## Gotchas
- **No backfill:** logs only exist from when the dataset was enabled — newly enabled = empty until new
  traffic. Allow a few minutes after enabling before data appears.
- **Always filter on `date`** (`YYYY-MM-DD`, supports `< > =`): it's a partition key that limits data
  scanned → far faster queries. A missing date/limit is the most common cause of timeouts.
- **Timeouts = too much data**, not a bug. Narrow the time window; `SELECT` only needed columns
  (`SELECT RayID` first, then refine; `SELECT COUNT(*)` to probe). Omitting `ORDER BY`/`LIMIT` over a
  big range can actually be faster than `LIMIT N` over a broad range.
- `WHERE` supports **max 25 predicates** (parenthesizable). Default `LIMIT` = **10,000** if omitted.
- **L7 DDoS attack logs are NOT ingested by default** (so they don't bill); other attack traffic IS
  billable, since it's forensically valuable.
- Custom Dashboards currently run on **GraphQL**, not on stored Log Explorer data (yet) — but you can
  save a Log Explorer query as a dashboard chart; Log Explorer customers get up to **100 dashboards**
  (vs 25 standard).
- **Customer Metadata Boundary is not supported.** Generic query errors → check SQL syntax + date/limit.

## Pricing & limits
> ⚠️ Paid add-on, no free tier/trial — and pricing is volatile. Verify on the live page
> (`developers.cloudflare.com/log-explorer/pricing/`) before quoting.

- **Cost driver:** GB of logs **ingested + stored** (consumption-based). Querying/scanning is **free**
  once stored — unlike query-billed models (e.g. BigQuery).
- **Retention:** contract customers can store up to **2 years** at **$0.10 / GB / month** (added via
  account team). Available only as a paid add-on to an Application Services or Zero Trust purchase.
- **Estimate** storage from request volume in **Analytics** × avg record size (e.g. `http_requests`
  ~1.56 kB avg, `firewall_events` ~1.36 kB, `audit_logs` ~2.69 kB — see pricing page table).
- **Limits:** ingestion up to **50,000 records/sec** (contact account team to exceed).
- Data lives in **internal, single-tenant Cloudflare-managed R2** buckets (not visible in your R2 UI,
  not billed separately). To stop charges: disable datasets (stops ingestion now) **and** cancel the
  subscription (stops renewal). Usage alerts via Notifications → Usage-based Billing.

## Going deeper
- No dedicated official `cloudflare` skill ref for this product — this file is the primary reference.
- Full SQL grammar + per-dataset field lists: `developers.cloudflare.com/log-explorer/sql-queries/`
  and the Logpush dataset docs (`logs/logpush/logpush-job/datasets/`).
- Example investigations: `developers.cloudflare.com/log-explorer/example-queries/`.
- Exact API shapes: `developers.cloudflare.com/log-explorer/api/`.
