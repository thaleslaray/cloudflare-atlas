# Durable Objects — stateful serverless (compute + storage, one instance per name)

> Globally-unique, single-threaded compute objects with **co-located, strongly-consistent storage**.
> The Cloudflare-native answer for coordination, sessions, real-time, and per-entity state.

## Contents
- When to use (and when not)
- Binding & config
- Distinctive points
- Lifecycle & hibernation
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- Per-entity state that must be **strongly consistent**: a chat room, a game match, a document, a
  user session, a rate limiter, a lock, a counter — one DO instance per logical entity.
- Real-time fan-out (WebSockets), coordination across many clients, serialized request processing
  (no race conditions — DOs are single-threaded).
- Backbone of the **Agents SDK** and **Workflows** (durable execution builds on DOs).
- **Not** for: bulk relational queries (→ d1/hyperdrive), object/file blobs (→ r2), global cache
  (→ kv), search vectors (→ vectorize). One DO maxes ~1K req/s — shard for higher throughput.

## Binding & config (`wrangler.jsonc`)
```jsonc
{
  "durable_objects": {
    "bindings": [{ "name": "MY_DO", "class_name": "MyDO" }]
  },
  "exports": { "MyDO": { "type": "durable-object", "storage": "sqlite" } }  // SQLite required for NEW namespaces (2026-07)
}
```
Class lifecycle is declared with **`exports`** (2026-07-04; `state`: `"deleted"` / `"renamed"` / `"transferred"`).
The legacy `migrations` array (`new_sqlite_classes`, `tag`) still works, but a Worker uses one or the other —
moving to `exports` cannot be undone.
Worker: `const stub = env.MY_DO.get(env.MY_DO.idFromName("room:42")); await stub.method()` (RPC,
needs `compatibility_date ≥ 2024-04-03`). External DO: add `"script_name"`. EU/FedRAMP data
residency: `env.MY_DO.jurisdiction("eu").idFromName(name)` — a jurisdiction-restricted *subnamespace*
is the recommended path (also `us` and `fedramp`); `newUniqueId({ jurisdiction: "eu" })` works but
Cloudflare does not recommend it. Read it back inside the DO via `ctx.id.jurisdiction`.

## Distinctive points
- **Class `extends DurableObject`** (not `implements`); constructor gets `(ctx, env)` — use `this.ctx`.
- **SQLite storage** (recommended): `ctx.storage.sql.exec(...)`, sync KV via `ctx.storage.kv`, 10 GB/DO,
  point-in-time recovery (30 days). **Mandatory for new namespaces** (2026-07); the legacy KV
  backend (async + Paid-only) is available **only to pre-existing namespaces**. Free plan support
  added 2025-04-07.
- **Namespace shortcut**: `env.MY_DO.getByName("room:42")` (2025-08-21) replaces `idFromName()` + `get()`;
  keep `idFromName` when you need to cache or inspect the ID.
- **Data Studio** (dashboard): view and write stored data of SQLite-backed DOs only —
  `durable-objects/observability/data-studio/`.
- **WebGPU API** (local dev only, DOs only — not Workers): `compatibility_flags = ["experimental", "webgpu"]`;
  cannot be deployed (`durable-objects/api/webgpu/`). Production GPU inference → Workers AI.
- **WebSocket Hibernation**: idle connections stay open at **zero compute / zero cost**; memory is
  cleared on hibernate. Use `ws.serializeAttachment()` / `setWebSocketAutoResponse()`. Message size
  limit raised from 1 MiB to **32 MiB** (2025-10-25).
- **Instance per name**: `idFromName()` = deterministic coordination; `newUniqueId()` = sharding.
- **Migrations** create/rename/transfer/delete classes; auto-applied on deploy, no rollback.

## Lifecycle & hibernation
- **Hibernation**: DO enters hibernation after **~10 s idle** (no requests, no active alarms). Memory
  is freed; WebSocket attachments preserved via serialization. Next request triggers a cold wake.
- **Eviction window**: once non-hibernateable work ends, the DO is evicted within **70–140 s**.
- **Pending I/O prevents eviction.** Always: outbound `fetch()` to external services, TCP sockets, outbound
  WebSockets. **New 2026-10-01** (default from compat date `2026-10-01`; earlier dates opt in with
  `durable_object_io_tasks_prevent_eviction`, opt out with `durable_object_io_tasks_do_not_prevent_eviction`):
  service-binding requests, DO RPC/`fetch()` calls, `ctx.container.monitor()`, `ctx.waitUntil()` promises,
  pending `setTimeout()`/`setInterval()`. Each blocks eviction until done or **15 min from its start** (per
  operation, not total) — work continues with no client connected, and **duration is billed** the whole time.
- **Wall time by invocation type**: alarm handler max **15 min**; HTTP/RPC handlers **unlimited**
  while the client remains connected (bounded by CPU/memory limits, not wall clock).
- **RPC session billing**: calls on a returned `RpcTarget` stub are the **same session** — only the
  initial call that creates the stub counts as a request.

## Gotchas
- **Persist to storage, not memory** — hibernation/eviction wipes in-memory fields. Reconstruct from
  `ctx.storage` or `deserializeAttachment()`.
- **Constructor runs on every wake** (cold start *and* hibernation wake) — keep it light, lazy-load.
- **`blockConcurrencyWhile()` is for init / critical sections**, not general use — it blocks all
  requests. `await` is a yield point, so naive read-modify-write races; prefer atomic SQL.
- **One alarm per DO** — multiple scheduled events need a queue pattern. Use `setAlarm()`, never
  `setTimeout` (in-memory, lost on eviction).
- **An interrupted alarm retries by default** — `ctx.abort()` while an alarm is running re-queues it,
  so an unrelated request can't permanently cancel it. To end a *finished* alarm, pass
  `ctx.abort("...", { retryAlarm: false })`; `retryAlarm` defaults to `true` and applies to abort
  calls made outside the alarm handler too.
- **Hot-reload breaks alarms locally**: after editing a DO in `wrangler dev`, alarm methods may fail
  silently; restart `wrangler dev` to restore alarm functionality (known issue).
- **SQLITE_FULL behavior**: when the 10 GB cap is hit, **writes fail** but reads and deletes still
  work, allowing recovery without external intervention. Empty SQLite DB consumes **~12 KB** baseline;
  metadata persists until explicit `deleteAll()`.
- **Up to 10 distinct Dynamic Workers** may have in-flight requests from one DO (was 4, raised
  2026-08-28) — see `dynamic-workers.md`.
- **Shard by entity** — a single DO is a serialization point (~1K req/s); don't funnel a whole app through one.
- **Pending work keeps the DO alive (and billing)** — see Lifecycle: close idle outbound connections and
  don't leave stray timers/`waitUntil()` promises if you want the DO to wind down.
- Deleting a class (`deleted_classes` migration or `exports` `state: "deleted"`) **destroys all data**
  irreversibly — test with `--dry-run`.

## Pricing & limits
> ⚠️ Pricing changes — verify on the live page (`developers.cloudflare.com/durable-objects/platform/pricing/`) before quoting.

**Cost drivers** (as of 2026-06, billed in addition to a $5/mo Workers Paid minimum):
- **Requests**: first 1M/month included, then $0.15/M (HTTP, RPC sessions, alarms; incoming WebSocket
  messages billed 20:1, outgoing free). Free: 100k/day.
- **Compute duration**: first 400k GB-s/month included, then $12.50/M GB-s of wall-clock while active
  (128 MB allocated regardless of use). Free: 13k GB-s/day. Hibernation eliminates idle duration
  charges — the big lever for WebSocket apps.
- **SQLite storage** (billing began Jan 2026): 5 GB-month + $0.20/GB-month; rows read first 25B/month
  included then $0.001/M, rows written first 50M/month included then $1.00/M (`setAlarm()` and each
  delete count as a row written). Free: 5 GB total, 5M row-reads/day, 100k row-writes/day.

**Key limits:** storage/DO **10 GB** (Free plan: 1 GB; account total Free 5 GB, Paid unlimited) ·
objects **unlimited** · DO classes 500 (Free 100) · req
throughput **~1K req/s per DO** (shard) · alarms **1 per DO** · CPU 30s default (max 5 min) ·
WebSocket msg 32 MiB · KV pair 2 MB · memory 128 MB/DO · 6 outbound conns/request. Verify on
`developers.cloudflare.com/durable-objects/platform/limits/`.

## Going deeper
- Covered by the official `cloudflare` skill (`references/durable-objects/`) — use it for full
  API, patterns (sharding, locks, real-time, sessions), configuration, and gotchas.
- Storage deep-dive: that skill's `references/do-storage/`. Agents on DOs → `cloudflare:agents-sdk`.
- "DO concepts / lifecycle" → the live blog (blog.cloudflare.com), search "Durable Objects".
