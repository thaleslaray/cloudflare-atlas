# R2 SQL → renamed Basin SQL

> R2 SQL is now **Basin SQL**. This stub exists for readers arriving with old links.
> **Use `products/basin-sql.md`.**

Old → new names (from the live `basin-sql/` pages):
- CLI: `wrangler r2 sql query` → `wrangler basin sql query "<WAREHOUSE>" "<SQL>"`.
- Token env var: `WRANGLER_BASIN_SQL_AUTH_TOKEN`.
- REST: `https://api.sql.cloudflarestorage.com/api/v1/accounts/{ACCOUNT_ID}/basin-sql/query/{BUCKET_NAME}`.
- Warehouse name: from `wrangler basin catalog get` (format `ACCOUNTID_BUCKETNAME`).
- Docs: `https://developers.cloudflare.com/basin-sql/`.
