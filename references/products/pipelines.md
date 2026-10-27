# Pipelines → renamed Basin Pipelines

> Cloudflare Pipelines is now **Basin Pipelines** (part of the Basin product family).
> This stub exists for readers arriving with old links. **Use `products/basin-pipelines.md`.**

Old → new names (from the live `basin-pipelines/` and `basin/` pages):
- CLI: `wrangler pipelines …` → `wrangler basin pipelines …` (e.g. `wrangler basin pipelines setup`).
- Iceberg sink type: `--type basin-catalog` (the catalog is now Basin Catalog → `products/basin-catalog.md`).
- Worker binding is unchanged: `"pipelines": [{ "binding": "STREAM", "stream": "<STREAM_ID>" }]`,
  `env.STREAM.send(events)`; types from `cloudflare:pipelines`.
- Docs: `https://developers.cloudflare.com/basin-pipelines/` (index: `/basin-pipelines/llms.txt`).
