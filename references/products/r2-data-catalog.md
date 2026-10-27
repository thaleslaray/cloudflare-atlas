# R2 Data Catalog → renamed Basin Catalog

> R2 Data Catalog is now **Basin Catalog** (managed Apache Iceberg REST catalog on an R2 bucket).
> This stub exists for readers arriving with old links. **Use `products/basin-catalog.md`.**

Old → new names (from the live `basin-catalog/` and `basin-pipelines/` pages):
- CLI: `wrangler r2 bucket catalog …` → `wrangler basin catalog enable|get|compaction|snapshot-expiration …`.
- Pipelines sink type: `--type basin-catalog` (→ `products/basin-pipelines.md`).
- Terraform resource and API permission group names still use the legacy R2 Data Catalog
  identifiers (e.g. `cloudflare_r2_data_catalog`; see `products/basin-pipelines.md`).
- Docs: `https://developers.cloudflare.com/basin-catalog/`.
