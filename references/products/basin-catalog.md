# Basin Catalog

> Managed Apache Iceberg catalog built into an R2 bucket. Exposes a standard Iceberg REST catalog
> interface for Spark, Snowflake, PyIceberg, DuckDB, Trino and StarRocks, with R2's zero egress.
> Formerly **R2 Data Catalog**; **Generally Available** since 2026-10-01 — existing configurations
> and APIs keep working and "will be deprecated in the future".

## Contents
- When to use (and when not)
- Key API / access patterns
- Table maintenance
- Gotchas
- Pricing & limits
- Going deeper

## When to use (and when not)
**Use when:**
- Building a lakehouse/warehouse directly on R2 without running an external metastore.
- Several engines (Spark, Trino, DuckDB, Snowflake, Basin SQL) must share the same Iceberg tables.
- You want managed compaction and snapshot expiration instead of custom orchestration.

**Do not use when:**
- The bucket is in a non-default jurisdiction — "Basin Catalog does not currently support R2 buckets
  in a non-default jurisdiction".
- You need a query engine — the catalog stores metadata only; bring compute (or use `products/basin-sql.md`).

## Key API / access patterns
- **Enable:** `npx wrangler basin catalog enable <BUCKET_NAME>` (or dashboard → Basin Catalog →
  **Create catalog**). It returns the **Catalog URI** and **Warehouse name** Iceberg clients need.
- **Disable:** `npx wrangler basin catalog disable <BUCKET_NAME>` — the catalog stops serving
  immediately and its Iceberg table references are inaccessible until re-enabled.
- **Auth:** a Cloudflare API token with **both** Basin Catalog and R2 storage permissions.
  - **Admin Read only** → listing namespaces, loading tables, querying (Basin SQL, DuckDB, PyIceberg readers).
  - **Admin Read & Write** → creating/dropping tables, committing transactions.
  - Via API, the permission groups are still named `Workers R2 Data Catalog Write` and
    `Workers R2 Storage Bucket Item Write` (read-only variants for readers).
  - The catalog **vends SigV4 credentials** to engines, and they **inherit the token's R2 storage
    permissions**: read-only catalog + read-write storage can still write objects. Scope storage
    read-only too if you need true read-only.
- **Engines:** config examples for Spark (Python/Scala), Snowflake, PyIceberg, DuckDB, Trino, StarRocks
  at `https://developers.cloudflare.com/basin-catalog/config-examples/`.
- **R2 Local Uploads:** writes land at a nearby location and copy asynchronously to the bucket; data is
  queryable immediately and strongly consistent — cuts write latency for Iceberg clients far from
  the bucket's region.
- **Metrics (GraphQL):** `r2CatalogDataOperationsAdaptiveGroups`, `r2CatalogTableMaintenanceAdaptiveGroups`.

## Table maintenance
- **Compaction** merges small files toward a **target file size: default 128 MB, minimum 64 MB,
  maximum 512 MB** (`--target-size 128`). Docs suggest 256–512 MB for scan-heavy OLAP, 64–128 MB for
  latency-sensitive workloads. **Parquet data files only.**
- **Snapshot expiration** removes old snapshots and unreferenced data files:
  `--older-than-days 7 --retain-last 10` (dashboard: Max snapshot age `7d`/`h`/`m`/`s`, Min snapshots
  to keep). Commands need Wrangler **4.56.0+**.
- Both run **catalog-level** (all tables, retroactive; needs `--token <API_TOKEN>` as a service
  credential with R2 storage + Basin Catalog read/write) or **table-level**
  (`... enable <BUCKET_NAME> <NAMESPACE> <TABLE>`).
  CLI: `wrangler basin catalog compaction enable` / `disable`, `wrangler basin catalog snapshot-expiration enable` / `disable`.

## Gotchas
- **Never delete files directly in the bucket.** Deletes must go through a catalog transaction;
  "Manually deleting metadata or data files directly can lead to data catalog corruption."
- **Copy-on-Write vs Merge-on-Read:** both create a new snapshot; on MOR tables run `rewrite_data_files`
  to apply deletes when many delete files slow queries.
- **`DROP TABLE ... PURGE` deletes the data files** — the docs say to PURGE tables before a `CASCADE`
  namespace drop to permanently delete data files.
- **Compaction pricing is binpacking today**; sort or z-order "may be priced differently in the future".

## Pricing & limits
> ⚠️ Verify on the live pricing page (`https://developers.cloudflare.com/basin-catalog/platform/pricing/`) before quoting.

Requires an active R2 subscription and a linked payment card. Charged on top of R2 storage/operations:
| Dimension | Included / month | Additional |
|---|---|---|
| Catalog operations (metadata requests) | 1 million | $9.00 / million |
| Compaction — data processed | 10 GB | $0.005 / GB |
| Compaction — objects processed | 1 million | $2.00 / million objects |
| Snapshot expiration | — | free |

- Compaction charges apply only to tables with compaction turned on.
- Doc example: 500,000 operations + compaction over 20 GB / 200,000 files → **$0.05**.

## Going deeper
- Live docs: `https://developers.cloudflare.com/basin-catalog/` (fetch as Markdown).
- Manage catalogs & tokens: `https://developers.cloudflare.com/basin-catalog/manage-catalogs/`.
- Table maintenance: `https://developers.cloudflare.com/basin-catalog/table-maintenance/`.
- Deleting data: `https://developers.cloudflare.com/basin-catalog/deleting-data/`.
- Related here: `products/basin.md`, `products/basin-sql.md`, `products/basin-pipelines.md`, `products/r2.md`.
