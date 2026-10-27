# Vectorize — vector database (embeddings, RAG, semantic search)

> Globally distributed **vector database**: store embeddings and query by similarity. The
> Cloudflare-native answer for RAG / semantic search — pairs with Workers AI + AI Search.

## Contents
- When to use (and when not)
- Binding & config
- Insert / query / metadata
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- **Semantic search, RAG, recommendations, classification, anomaly detection** over your own data.
- You have **embeddings** (vectors) and want nearest-neighbor search by cosine/euclidean/dot.
- Pairs with: **Workers AI** (generate embeddings, e.g. `@cf/baai/bge-base-en-v1.5`) + **AI Search**
  (managed RAG over R2). Matches reference objects in **R2/D1/KV** — search result → concrete object.
- The CF-native answer vs **Pinecone/Weaviate** — no separate infra, runs on the Workers platform.
- **Not** for: relational/SQL (→ d1), key-value (→ kv), blobs/files (→ r2), full-text only (→ d1 FTS).

## Binding & config (`wrangler.jsonc`)
```jsonc
{ "vectorize": [ { "binding": "VECTORIZE", "index_name": "my-index" } ] }
```
Create the index first (dimensions + metric are **immutable**):
```bash
npx wrangler vectorize create my-index --dimensions=768 --metric=cosine
```
Access in Worker: `env.VECTORIZE.insert(...)` / `.upsert(...)` / `.query(vec, opts)` / `.getByIds(...)`.

## Insert / query / metadata
```typescript
// Embed with Workers AI, then query — pass result.data[0], NOT the whole result
const e = await env.AI.run("@cf/baai/bge-base-en-v1.5", { text: [query] });
await env.VECTORIZE.upsert([{ id: "1", values: e.data[0], metadata: { category: "docs" } }]);
const res = await env.VECTORIZE.query(e.data[0], {
  topK: 5, returnMetadata: "indexed", filter: { category: "docs" },
});
```
- **Metadata filtering** needs a metadata index, created **before** inserting:
  `wrangler vectorize create-metadata-index my-index --property-name=category --type=string`
  (types: `string` / `number` / `boolean`; operators incl. `$in`, `$gte`, dot-notation for nested).
- **Multi-tenant:** `namespace` per vector (≤50K tenants, fastest) or a metadata filter (beyond that).
- `insert` ignores duplicate IDs; `upsert` overwrites — prefer `upsert` for idempotent ingestion.

## Gotchas
- **Dimensions must match the embedding model** — index dims (e.g. 768) must equal the model's output;
  mismatch = error. Can't change dims/metric after creation → new index + re-migrate.
- **Metadata index must exist BEFORE inserting** — existing vectors are NOT retroactively indexed.
- **Async mutations:** insert/upsert/delete return immediately; vectors become queryable after a short
  lag — median under ~30s, p99 under ~2 min (WAL throughput improved 2026-07). Not read-your-writes.
- **Batch size:** Workers API max **1,000** vectors/call (HTTP API 5,000) — chunk larger sets.
- **topK caps:** 100 with `returnMetadata:"none"/"indexed"`; drops to **50** with `"all"` or `returnValues`
  (was 20 until 2026-03-16; 20 still applies to legacy V1 indexes).
- **Indexed string metadata truncates at 64 bytes** — use `returnMetadata:"all"` for full strings.

## Pricing & limits
> ⚠️ Pricing changes — verify on the live page (`developers.cloudflare.com/vectorize/platform/pricing/`) before quoting.

**Cost drivers** (billed on dimensions, not CPU/hours/index count; as of 2026-06):
- **Queried vector dimensions:** `(stored + queried vectors) × dims` — **$0.01 / million** (Paid; first 50M/mo free).
- **Stored vector dimensions:** `vectors × dims` — **$0.05 / 100 million** (Paid; first 10M/mo free).
- Free plan: 30M queried + 5M stored dimensions/month. No egress/data-transfer charge; empty indexes cost nothing.

**Key limits:** dims/vector **1,536** (float32) · vectors/index **20,000,000** (raised from 10M on
2026-08-04 — older sources say 10M) · indexes/account 50,000 paid /
100 free · metadata/vector **10 KiB** · metadata indexes/index **10** · namespaces/index 50,000 paid / 1,000 free · upload
**100 MB** · vector ID & index name 64 bytes. Verify on `developers.cloudflare.com/vectorize/platform/limits/`.

## Going deeper
- Covered by the official `cloudflare` skill (`references/vectorize/`) — use it for full API/patterns
  (`api.md`, `configuration.md`, `patterns.md` for RAG/multi-tenant/hybrid, `gotchas.md`).
- Embeddings + managed RAG: Workers AI (`references/workers-ai/`) and AI Search.
