# Basin

> Serverless analytics platform on Apache Iceberg and R2: ingest and transform events (Basin
> Pipelines), keep them as Iceberg tables (Basin Catalog), query them (Basin SQL or external engines).
> **Generally Available since 2026-10-01.** Formerly "Cloudflare Data Platform"; Cloudflare Pipelines,
> R2 Data Catalog and R2 SQL are now Basin Pipelines, Basin Catalog and Basin SQL — existing
> resources and configurations keep working.

## Contents
- When to use (and when not)
- Architecture
- Key API / access patterns
- Gotchas
- Pricing & limits
- Going deeper

## When to use (and when not)
**Use when:**
- Serverless OLAP over event data in R2, without running streaming infrastructure or query clusters.
- Data must stay portable: open Iceberg tables readable by Spark, Snowflake, DuckDB, Trino, PyIceberg.
- You want managed table maintenance (compaction, snapshot expiration).

**Do not use when:**
- OLTP/transactional workloads → `products/d1.md` or `products/hyperdrive.md`.
- Low-latency key lookups → `products/kv.md`.
- Custom per-Worker metrics with no lakehouse → `products/analytics.md` (Analytics Engine).

## Architecture
`Source → Basin Pipelines → Basin Catalog → Basin SQL` (the docs' own flow).
| Part | Role | File |
|---|---|---|
| Basin Pipelines | HTTP / Worker-binding ingestion, stateless SQL transforms, exactly-once sinks to R2 | `products/basin-pipelines.md` |
| Basin Catalog | Iceberg REST catalog built into an R2 bucket; compaction + snapshot expiration | `products/basin-catalog.md` |
| Basin SQL | Distributed serverless SQL over Catalog tables | `products/basin-sql.md` |

## Key API / access patterns
```bash
npx wrangler basin pipelines setup                         # stream + sink + pipeline, interactive
npx wrangler basin catalog enable <BUCKET_NAME>            # returns Catalog URI + Warehouse name
npx wrangler basin sql query <WAREHOUSE> "SELECT ..."      # ad-hoc query
```
- Workers send events through a `pipelines` binding (`env.STREAM.send(events)`); external producers
  use the stream's HTTP endpoint.
- External engines authenticate to the catalog with an API token carrying Basin Catalog + R2 storage
  permissions (read-only or read-write).
- The docs ship a "prompt an agent" guide: `https://developers.cloudflare.com/basin/get-started/prompting/`.

## Gotchas
- **Renamed, not replaced.** Old names (R2 SQL, R2 Data Catalog, Cloudflare Pipelines) still work;
  the Catalog and SQL pages say the old APIs "will be deprecated in the future". Write new code
  against `wrangler basin ...`.
- **R2 storage, read, and write operations add separate charges** — the Basin pricing page excludes them from every table.
- **No egress fees** — R2 does not charge for egress, so external engines reading the tables pay none
  (they still generate R2 read operations).
- **Exactly-once delivery** is a sink guarantee; schema-invalid events are dropped, not retried.

## Pricing & limits
> ⚠️ Verify on the live page (`https://developers.cloudflare.com/basin/platform/pricing/`) before quoting.
> R2 storage and operations are extra.

| Product · dimension | Included / month | Additional |
|---|---|---|
| Pipelines · stream ingress | unlimited | free |
| Pipelines · SQL transforms | 50 GB | $0.04 / GB |
| Pipelines · sink delivery JSON | 50 GB (shared sink allowance) | $0.03 / GB |
| Pipelines · sink delivery Parquet/Iceberg | 50 GB (shared sink allowance) | $0.06 / GB |
| Catalog · operations | 1 million | $9 / million |
| Catalog · compaction data processed | 10 GB | $0.005 / GB |
| Catalog · compaction objects processed | 1 million | $2 / million |
| SQL · compressed data scanned | 10 GB | $0.0025 / GB ($2.50 / TB), 10 MB minimum per query |

- Snapshot expiration has no separate charge. Failed SQL queries (syntax, system, runtime) and
  metadata-only `EXPLAIN` / `SHOW` / `DESCRIBE` incur no scan charge.
- Doc's end-to-end example: Pipelines subtotal **$33.00**, Catalog compaction **$0.05**.
- Key limits: 1 GB/s ingest **per stream**; 20 streams / sinks / pipelines per account; 5 MB per
  ingestion request; SQL `LIMIT` 1–10,000. Detail in the three product files.

## Going deeper
- Live docs: `https://developers.cloudflare.com/basin/` (fetch as Markdown).
- CLI guide: `https://developers.cloudflare.com/basin/get-started/guide/`.
- No official `cloudflare` skill reference covers Basin yet; this file and its three siblings are primary.
