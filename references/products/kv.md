# KV — global key-value store (eventually consistent, read-optimized)

> Globally-distributed key-value store optimized for **high read volume, low-latency reads**.
> Writes replicate to the edge with **eventual consistency** (≤60s global propagation).

## Contents
- When to use (and when not)
- Binding & config
- Access patterns
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- Read-heavy, write-light data: app **config**, feature flags, **user sessions**, cached responses,
  A/B-test assignments, edge **caching** of upstream results.
- You can tolerate **eventually-consistent reads** — writes are visible immediately in the same
  location but take ≤60s to propagate globally.
- **Not** for: **strong consistency** or coordination (→ durable-objects), relational/SQL queries
  (→ d1), object/file storage (→ r2), high write-rate to a single key (1 write/s/key cap).

## Binding & config (`wrangler.jsonc`)
```jsonc
{
  "kv_namespaces": [
    { "binding": "MY_KV", "id": "abc123", "preview_id": "preview-abc123" }
  ]
}
```
Create: `wrangler kv namespace create MY_NAMESPACE` (add `--preview` for local dev).
Access in Worker: `env.MY_KV.get(key)` / `.put(key, value, opts)` / `.delete(key)` / `.list(opts)`.
Also: CLI (`wrangler kv key …` / `wrangler kv bulk …`) and a REST API (bulk up to 10,000 keys).
**Jurisdictions — GA 2026-10-02:** `wrangler kv namespace create` with `--jurisdiction=eu` (or REST
`"jurisdiction": "eu"`); supported `eu`, `us`, `fedramp`. Set **only at creation**, never changed later.
It controls durable storage only — Workers still read from anywhere and data can be **cached outside**
the jurisdiction (use Regional Services to restrict serving). Docs: `developers.cloudflare.com/kv/reference/data-location/`.

## Access patterns
- **get** — `env.MY_KV.get(key, "text"|"json"|"arrayBuffer"|"stream")`; missing key → `null`
  (not an error). Bulk read up to **100 keys**: `get([k1, k2, …])` → `Map`, billed per key.
- **put** — `put(key, value, { expirationTtl, expiration, metadata })`. TTL in seconds from now;
  `expiration` is a UNIX timestamp; `metadata` ≤1024 bytes.
- **list** — `list({ prefix, limit, cursor })` → `{ keys, list_complete, cursor }`.
- **getWithMetadata(key)** — value + stored metadata in one read.

## Gotchas
- **Eventual consistency:** do NOT read immediately after a write — other locations may still
  return the old value (or `null`) for up to 60s. Return/reuse the value you just wrote instead.
- **Negative caching:** a `null` lookup is cached as "not found" for ~60s, so a key created right
  after a miss may stay invisible. Don't rely on read-after-write check→create.
- **1 write/s per key:** concurrent writes to the same key 429. Use unique keys or backoff retry.
- **TTL:** `expirationTtl` is seconds-from-now; min `cacheTtl` is **30s**. Use TTL for sessions/cache
  so entries self-expire instead of manual deletes.
- **Every op is billed**, including reads that return `null`. Coalesce many small keys into one JSON
  value, and use bulk `get` (counts the keys read, but one round-trip).

## Pricing & limits
> ⚠️ Pricing changes — verify on the live page (`developers.cloudflare.com/kv/platform/pricing/`) before quoting.

**Cost drivers** (Paid plan, as of 2026-06):
- Reads: **$0.50 / million** (beyond 10M/mo included)
- Writes: **$5.00 / million** (beyond 1M/mo included)
- Deletes: **$5.00 / million** · List requests: **$5.00 / million**
- Storage: **$0.50 / GB-month** (beyond 1 GB included)
- **No egress / data-transfer charge.**
- Free tier (daily, resets 00:00 UTC): 100k reads · 1k writes · 1k deletes · 1k lists · 1 GB stored.

**Key limits:** value size **25 MiB** · key size **512 bytes** · key metadata **1,024 bytes** ·
write-to-same-key **1/s** · ops per Worker invocation **1,000** (bulk = 1) · bulk get **100 keys** ·
namespaces/account **1,000** · keys/namespace **unlimited** · min `cacheTtl` **30s** · global
propagation **≤60s**. Verify on `developers.cloudflare.com/kv/platform/limits/`.

## Going deeper
- Covered by the official `cloudflare` skill (`references/kv/`) — use it for full API/patterns
  (caching, sessions, rate-limiting, A/B testing, bulk/REST operations).
- Exact REST API: `references/api/kv.md` — exact endpoints sliced from the OpenAPI spec (verify shapes live).
- "KV vs Durable Objects / when eventual consistency bites" → `scripts/blog-search "Workers KV consistency"`.
