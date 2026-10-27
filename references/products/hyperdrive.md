# Hyperdrive — accelerate existing Postgres/MySQL from Workers

> Make a regional Postgres/MySQL feel global: connection **pooling** + query **caching** in front of
> your *existing* database, so Workers query it with low latency and without exhausting connections.

## Contents
- When to use (and when not)
- Binding & config
- Usage pattern
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- You **already have** a Postgres/MySQL (RDS/Aurora, Neon, Supabase, PlanetScale, Timescale,
  CockroachDB, Cloud SQL, Azure…) and want fast global access from Workers **without migrating**.
- High read ratios, popular/repeated queries, connection-heavy loads, single-region DB served globally.
- **Not** for: a brand-new app with no existing DB → use **d1** (serverless SQLite, edge-native).
  Also weak fit for write-heavy / real-time (<1s freshness) / single-region apps already next to the DB.
- **Engines:** PostgreSQL **9.0–17.x**, MySQL **5.7–8.x** (MariaDB too). SQL Server and MongoDB: not supported.
- Pair with **Smart Placement** (`"placement": {"mode": "smart"}`) for multi-query Workers — runs the
  Worker near the DB so each query isn't a round-trip from the edge.
- **No existing DB?** You can now create a **PlanetScale Postgres or MySQL** database directly, billed
  to your Cloudflare account, and wire it to Hyperdrive.

## Binding & config (`wrangler.jsonc`)
```bash
npx wrangler hyperdrive create my-db \
  --connection-string="postgres://user:pass@host:5432/dbname"
```
```jsonc
{
  "compatibility_flags": ["nodejs_compat"],          // REQUIRED — drivers need Node APIs
  "hyperdrive": [{ "binding": "HYPERDRIVE", "id": "<CONFIG_ID>" }]
}
```
In the Worker, use `env.HYPERDRIVE.connectionString` (or `.host/.user/.password/.database/.port`) as the
driver target — Hyperdrive proxies to your origin. Drivers: **pg** (recommended), **postgres.js**, **mysql2**.

## Usage pattern
```ts
import { Client } from "pg";
export default {
  async fetch(req, env, ctx): Promise<Response> {
    const client = new Client({ connectionString: env.HYPERDRIVE.connectionString });
    await client.connect();
    const { rows } = await client.query("SELECT * FROM users WHERE id = $1", [123]);
    ctx.waitUntil(client.end());        // close AFTER responding — don't block, don't leak
    return Response.json(rows);
  },
};
```
- **Pooling**: Hyperdrive keeps warm connections near your DB, eliminating per-request TCP/TLS/auth
  handshakes (~7 round-trips). You still open a client per request; Hyperdrive multiplexes behind it.
- **Caching** (on by default): non-mutating `SELECT`s cached `max_age=60s`, `stale_while_revalidate=15s`.
  Tune with `--max-age` (default 60s, **max 1 hour**) and `--swr`; disable per-config with
  `wrangler hyperdrive update <id> --caching-disabled`. Cache is **not** invalidated by your writes.

## Gotchas
- **New client per request** — create the client *inside* the handler, never in global/module scope.
- **Always close**: `ctx.waitUntil(client.end())`. Leaked connections → "Too many open connections".
- **`nodejs_compat` is mandatory** — without it the Postgres/MySQL driver won't run.
- **Only read queries cache.** Writes (`INSERT/UPDATE/DELETE`) and functions PostgreSQL marks
  *volatile* **or** *stable* (`NOW()`, `RANDOM()`, `LASTVAL()`) always hit origin and are never cached.
- **Driver pool `max: 5`** — not a Hyperdrive limit: Hyperdrive does *not* cap concurrent client
  connections from Workers. It's the Workers platform limit of **6 simultaneous outgoing connections
  waiting for response headers** per invocation (a 7th is *queued*, not rejected).
- **60s query cap**: statements >60s are terminated; responses >50 MB are returned but not cached.
- Self-signed DB cert → set `sslmode=require` (PG) / `sslMode=REQUIRED` (MySQL); upload CA if needed.

## Pricing & limits
> ⚠️ Verify live before quoting: `developers.cloudflare.com/hyperdrive/platform/pricing/` and `/limits/`.

**Pooling + caching are INCLUDED FREE** in the Workers plans — no per-feature charge, no egress charge.
- **Free plan:** 100,000 database queries / day (resets 00:00 UTC; cached *and* uncached both count).
- **Paid plan:** unlimited queries.

**Key limits (Free / Paid):** configs per account **10 / 25** · max origin connections per config
**~20 / ~100** (soft; tune with `--origin-connection-limit`) · query duration **60s** · cached response
**50 MB** · init connection timeout **15s** · idle timeout **10 min** · username & DB name **63 bytes**.
*(PlanetScale Postgres/MySQL DBs created via Cloudflare are billed to your Cloudflare account.)*

## Going deeper
- Covered by the official `cloudflare` skill (`references/hyperdrive/`) — use it for full API/patterns
  (`configuration.md`, `api.md`, `patterns.md`, `gotchas.md`).
- Driver/ORM examples (Drizzle, Prisma, node-postgres, postgres.js, mysql2) → `pages/hyperdrive/examples/`.
- "How Hyperdrive works / why" → `scripts/blog-search "Hyperdrive regional databases distributed"`.
