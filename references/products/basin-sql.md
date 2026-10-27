# Basin SQL

> Serverless, distributed SQL analytics engine for querying Apache Iceberg tables stored in Basin Catalog (R2). GA as of Oct 2026; formerly "R2 SQL".

## Contents

- [When to use (and when not)](#when-to-use-and-when-not)
- [Key API / access patterns](#key-api--access-patterns)
- [Gotchas](#gotchas)
- [Pricing & limits](#pricing--limits)
- [Going deeper](#going-deeper)

## When to use (and when not)

**Use when:**

- You need ad-hoc or scheduled SQL analytics over large datasets already in R2/Basin Catalog.
- Your data is in Apache Iceberg format (or you can convert it via Basin Pipelines).
- You want serverless query execution without provisioning warehouses or clusters.
- You are building an end-to-end streaming pipeline: ingest → Basin Pipelines → Iceberg → Basin SQL.

**Do not use when:**

- You need OLTP / transactional workloads (use D1 or Postgres instead).
- Your data is not in Iceberg format and cannot be converted.
- You require persistent compute, materialized views with incremental refresh, or UDFs beyond the built-in function set.
- Latency target is sub-second interactive dashboarding on large scans (it is an analytics engine, not a caching layer).

## Key API / access patterns

### Authentication

Wrangler needs an API token with permissions for **Basin Catalog**, **R2 storage** and **Basin SQL** (the query-data page; tutorials create one with **Admin Read & Write**). `basin sql query` reads it from `WRANGLER_BASIN_SQL_AUTH_TOKEN`:

```bash
export WRANGLER_BASIN_SQL_AUTH_TOKEN=YOUR_API_TOKEN
# or in .env
WRANGLER_BASIN_SQL_AUTH_TOKEN=YOUR_API_TOKEN
```

### CLI queries

```bash
npx wrangler basin sql query "<WAREHOUSE_NAME>" "SELECT * FROM default.my_table LIMIT 10"
```

The warehouse name comes from `wrangler basin catalog get` (also shown in the dashboard: R2 bucket → Settings → Basin Catalog → **Warehouse name**).

REST: `POST https://api.sql.cloudflarestorage.com/api/v1/accounts/{ACCOUNT_ID}/basin-sql/query/{BUCKET_NAME}`.

### SQL surface

Standard analytics SQL: `SELECT`, `JOIN` (inner/left/right/full/cross), CTEs, window functions (`ROW_NUMBER`, `LAG`, `LEAD`, running aggregates), `GROUP BY` with `ROLLUP`/`CUBE`/`GROUPING SETS`, `QUALIFY`, set operations (`UNION`, `INTERSECT`, `EXCEPT`), `EXPLAIN [FORMAT JSON]`. Schema discovery via `SHOW DATABASES`, `SHOW NAMESPACES`, `SHOW TABLES IN namespace_name`, `DESCRIBE namespace_name.table_name`.

Data types: `integer`, `float`, `string`, `boolean`, `timestamp` (RFC3339), `date`, `struct`, `array` (1-indexed), `map`.

### Interoperability

Any engine that supports Apache Iceberg can read Basin Catalog tables directly (Spark, Trino, DuckDB, StarRocks, PyIceberg, Snowflake). Basin SQL is one reader among many; the storage layer is open.

## Gotchas

- **Minimum scan per query: 10 MB.** Even if the query touches less data, you are billed for 10 MB. This covers engine initialization overhead.
- **Nested (parenthesized) JOINs are not supported.** Flatten multi-way joins: `FROM t1 JOIN t2 ON ... JOIN t3 ON ...` instead of `(t1 JOIN t2) JOIN t3`.
- **`NOT IN` on nullable columns is unsupported.** Use `NOT EXISTS` instead to avoid silent wrong results.
- **`LATERAL` derived tables are not supported.** Subqueries in `FROM` cannot reference outer columns from sibling tables.
- **Named `WINDOW` clause is not supported.** Inline the `OVER (...)` specification at each call site.
- **`LIMIT` must be between 1 and 10,000** — larger values fail with `maximum LIMIT is 10000`. Resource-heavy queries (3+ large-table joins, `COUNT(DISTINCT)` across joins, `ARRAY_AGG`/`STRING_AGG`, big sorts) may time out: filter with `WHERE`, add `LIMIT`, prefer `approx_*` aggregates.
- **Metadata-only ops (`EXPLAIN`, `SHOW`, `DESCRIBE`) are free** for Basin SQL but still incur standard R2 Class B and Basin Catalog request charges.
- **Failed queries are not charged** — neither syntax errors caught before execution nor runtime errors mid-execution.
- **Formerly "R2 SQL":** legacy API names still work but are deprecated. Migrate to `basin sql` commands.

## Pricing & limits

> **Verify on the live pricing page before quoting.** Pricing is volatile and may have changed since this file was written.

| Dimension | Rate | Included |
|---|---|---|
| Data scanned | $0.0025 / GB ($2.50 / TB) | 10 GB / month |
| Minimum per query | 10 MB | — |

- **Data scanned** = compressed bytes read from R2 to execute the query. If a Parquet file is 100 MB on disk, scanning it bills 100 MB.
- **No egress fees.** The query engine runs adjacent to R2 within Cloudflare's network.
- **Additive to R2 + Basin Catalog charges.** Reads count as R2 Class B operations; catalog operations and compaction are billed separately.
- **Requires active R2 subscription** and a linked payment card.

Key limits: no published concurrency cap in current docs; monitor for throttling on burst workloads. Metadata operations (`EXPLAIN`, `SHOW`, `DESCRIBE`) do not count toward data-scanned billing.

## Going deeper

- Official docs: <https://developers.cloudflare.com/basin-sql/>
- Getting started (end-to-end pipeline tutorial): <https://developers.cloudflare.com/basin-sql/get-started/>
- SQL reference (full syntax, functions, data types): <https://developers.cloudflare.com/basin-sql/sql-reference/>
- Basin Catalog (storage layer): <https://developers.cloudflare.com/basin-catalog/>
- Basin Pipelines (streaming ingest + SQL transforms): <https://developers.cloudflare.com/basin-pipelines/>
- Connect external Iceberg engines: <https://developers.cloudflare.com/basin-catalog/config-examples/>
- Pricing detail + billing examples: <https://developers.cloudflare.com/basin-sql/platform/pricing/>
- Feedback / bugs: #basin-sql channel on <https://discord.cloudflare.com/>