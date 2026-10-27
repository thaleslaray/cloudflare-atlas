# Basin Pipelines — streaming ingestion, SQL transforms, and delivery to R2

> Ingest high-volume event streams, transform them with stateless SQL, and deliver the results to
> R2 as Iceberg, Parquet, or JSON files. Formerly Cloudflare Pipelines; **Generally Available**
> under the Basin platform since 2026-10-01. Available on the Workers Paid plan.

## Contents
- When to use (and when not)
- Binding & config
- Key API / access patterns
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- Streaming ETL: ingest events from Workers, HTTP clients, or external producers and land them in
  R2 as queryable Iceberg tables (via Basin Catalog) or raw JSON/Parquet files.
- Fan-out: one pipeline can run several `INSERT` statements separated by semicolons, each reading
  the same stream and writing a different sink (see the Bluesky firehose fan-out example).
- Pairs with: R2 (storage sink), Basin Catalog (Iceberg tables), Basin SQL (querying landed data),
  Workers (ingestion binding).
- **Not** for: real-time serving or sub-second reads (→ KV, Durable Objects); stateful stream
  processing — aggregations, joins and windows are not available yet (see Gotchas).

## Binding & config
```jsonc
// wrangler.jsonc — the binding key is still "pipelines"; it points at a STREAM
{ "pipelines": [ { "binding": "STREAM", "stream": "<STREAM_ID>" } ] }
```
- The old `pipeline` field was renamed to `stream`; `pipeline` still works with a Wrangler
  deprecation warning.
- `wrangler types` generates a named record type for streams with a schema
  (`Pipeline<Cloudflare.EcommerceStreamRecord>` from `cloudflare:pipelines`); it falls back to the
  generic `Pipeline<PipelineRecord>` when unauthenticated, the stream ID is wrong, or the stream
  is unstructured.

## Key API / access patterns
- **Worker ingestion:** `await env.STREAM.send(events)` — sends an array of JSON-serializable
  records; the Promise resolves when they are confirmed ingested.
- **HTTP ingestion:** each stream has an optional endpoint `https://{stream-id}.ingest.cloudflare.com`
  (find it with `wrangler basin pipelines streams get <STREAM_NAME_OR_ID>`).
- **Pipelines:** SQL like `INSERT INTO my_sink SELECT * FROM my_stream`, created with
  `wrangler basin pipelines create my-pipeline --sql "..."` or the interactive
  `wrangler basin pipelines setup`. Streams and sinks are sub-commands:
  `wrangler basin pipelines streams list`, `wrangler basin pipelines sinks list`.
- **Sinks:** R2 as JSON or Parquet (`--type r2 --bucket my-bucket`), or Basin Catalog as Iceberg
  (`--type basin-catalog`). Rolling policy: `--roll-size` (MB, minimum 5 MB) and
  `--roll-interval` (seconds, minimum 10 seconds); also `--compression`, `--format`.
- **Delivery guarantee:** sinks provide exactly-once delivery — events are never duplicated or
  dropped.
- **Errors:** events dropped by schema validation are queryable in GraphQL via
  `pipelinesUserErrorsAdaptiveGroups` / `pipelinesUserErrorsAdaptive`.

## Gotchas
- **Pipeline SQL cannot be modified after creation** — delete and recreate the pipeline to change it.
  **Sinks cannot be modified after creation** either.
- **Sinks cannot be created for existing Iceberg tables** — the sink creates its table.
- **Sink egress is measured on uncompressed data.** Compressed Parquet/Iceberg output is billed on
  the pre-compression volume.
- **Stateless only.** Pricing covers filter, reshape, unnest, cast and compute; stateful operations
  (aggregations, joins, windows) are future and "may be priced separately".
- **Schema enforcement drops events.** With a structured schema, invalid events are dropped (see the
  GraphQL error datasets above) — streams accept JSON only.
- **Legacy pipelines** (created before September 25, 2025 via the legacy API) are on a deprecation
  path and labeled "legacy" in `wrangler basin pipelines list`. Migrate with
  `wrangler basin pipelines setup`, repoint producers, then delete the legacy pipeline.
- **Files appear on roll, not per record.** Do not expect an ingested event to be visible in R2
  before the rolling policy fires.

## Pricing & limits
> ⚠️ Pricing changes — verify on the live page (`https://developers.cloudflare.com/basin-pipelines/platform/pricing/`) before quoting.

Cost drivers (Workers Paid, monthly included usage):
- **Streams (ingress): free**, unlimited.
- **SQL transforms:** 50 GB / month included, then **$0.04 / GB** processed.
- **Sinks (egress):** 50 GB / month included, then **$0.03 / GB** (R2 — JSON) or **$0.06 / GB**
  (R2 — Parquet / Iceberg).
- R2 storage/operations and Basin Catalog charges apply separately.
- Doc example: 500 GB ingested, filtered to 300 GB into Iceberg → $18.00 transforms + $15.00 sink
  = **$33.00**.

Limits (`https://developers.cloudflare.com/basin-pipelines/platform/limits/`):
| Limit | Value |
|---|---|
| Streams / sinks / pipelines per account | 20 each |
| Max payload per ingestion request | 5 MB |
| Max ingest rate | **1 GB/s per stream** (raised 2026-10-01) |

Higher limits via the Limit Increase Request Form linked on the limits page.

## Going deeper
- Live docs: `https://developers.cloudflare.com/basin-pipelines/` (fetch as Markdown).
- Writing to streams: `https://developers.cloudflare.com/basin-pipelines/streams/writing-to-streams/`.
- Fan-out example: `https://developers.cloudflare.com/basin-pipelines/examples/bluesky-firehose-fanout/`.
- Legacy migration: `https://developers.cloudflare.com/basin-pipelines/reference/legacy-pipelines/`.
- SQL functions: `https://developers.cloudflare.com/basin-pipelines/sql-reference/scalar-functions/`.
- Related here: `products/basin.md` (platform), `products/basin-catalog.md`, `products/basin-sql.md`,
  `products/r2.md`.
