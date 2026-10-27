# Queues — message queue (at-least-once, no egress fees)

> Decouple producers from consumers with a managed message queue. Workers push/pull messages with
> configurable **batching, retries, delays, and Dead Letter Queues** — and **no egress charges**.

## Contents
- When to use (and when not)
- Binding & config
- Access patterns
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- **Async / background processing:** offload slow work (emails, webhooks, image jobs) off the request path.
- **Decoupling & buffering:** absorb bursts, smooth load onto a slow downstream (DB, third-party API).
- **Retries + DLQ:** built-in retry with backoff; messages that exhaust retries land in a Dead Letter Queue.
- Pairs with: Workers (producer/consumer), R2/D1 (event notifications → queue), Workflows.
- **Not** for: durable multi-step orchestration with per-step state/sleep → **Workflows**. Pub/sub
  fan-out to many subscribers → not the model (one queue = one consumer). Sub-ms RPC → Service bindings.

## Binding & config (`wrangler.jsonc`)
```jsonc
{
  "queues": {
    "producers": [{ "queue": "my-queue", "binding": "MY_QUEUE" }],
    "consumers": [{
      "queue": "my-queue",
      "max_batch_size": 10,        // 1-100, default 10
      "max_batch_timeout": 5,      // 0-60s
      "max_retries": 3,            // max 100
      "dead_letter_queue": "my-dlq"
    }]
  }
}
```
Producer: `await env.MY_QUEUE.send(body, { contentType })` / `.sendBatch([...])`.
Consumer: export an `async queue(batch, env)` handler. CLI: `wrangler queues create|consumer add|pause-delivery|purge`.

## Access patterns
- **Push consumer (Worker)** — Cloudflare invokes your `queue()` handler with a batch; lowest friction.
- **Pull consumer (HTTP)** — external workers poll via HTTP API with a `visibility_timeout_ms`; enable with
  `wrangler queues consumer http add <QUEUE>` (or the dashboard). Enabling via `"type": "http_pull"` in
  the Wrangler config is no longer supported.
- **Batching** — tune `max_batch_size` + `max_batch_timeout` to trade throughput vs latency.
- **Per-message control** — `msg.ack()`, `msg.retry({ delaySeconds })`, or `batch.ackAll()` / `batch.retryAll()`.
- **Delays** — delay delivery on `send` or `retry` (up to 24h) for deferred/scheduled jobs.

## Gotchas
- **Uncaught error retries the ENTIRE batch**, not just the failed message. Wrap each message in
  try/catch and call `msg.retry()` explicitly.
- **Unhandled messages auto-retry** until `max_retries` (then DLQ). Always `ack()` or `retry()` every
  message — including ones you intentionally skip.
- **At-least-once delivery → duplicates happen.** Make consumers idempotent (e.g. dedup on `msg.id` in KV).
- **`v8` content type is push-only** — invisible to pull consumers and the dashboard. Use `json`
  (the default) if you need pull/dashboard visibility; `v8` only for Date/Map/Set/BigInt.
- **CPU time defaults to 30s** per consumer invocation; raise via `limits.cpu_ms` (max 5 min).

## Pricing & limits
> ⚠️ Pricing changes — verify on the live page (`developers.cloudflare.com/queues/platform/pricing/`) before quoting.

**Cost drivers** (as of 2026-06):
- Billed per **operation** = each 64 KB of data **written, read, or deleted**. A message <64 KB normally
  costs **3 ops** (write + read + delete); larger messages charge per 64 KB chunk.
- Each **retry** adds a read op; DLQ writes add write ops. **Egress/throughput: FREE.**
- Rate: **$0.40 / million operations**.
- Free tier: Workers Paid → 1M ops/month included; Workers Free → 10k ops/day (24h retention, non-configurable).

**Key limits:** message size **128 KB** · consumer batch **100 msgs** · `sendBatch` **100 msgs / 256 KB**
· throughput **5,000 msgs/s per queue** · queues/account **10,000** · backlog/queue **25 GB** · retries
**100** · retention **4 days default, configurable 60s–14 days** (Free: 24h, non-configurable) · delay **24h** · consumer wall time **15 min** · CPU
**30s default / 5 min max** · concurrent consumer invocations **250** (push) · pull `visibilityTimeout` **12h**. Verify on `developers.cloudflare.com/queues/platform/limits/`.

## Going deeper
- Covered by the official `cloudflare` skill (`references/queues/`) — use it for full API/patterns
  (`configuration.md`, `api.md`, `patterns.md`, `gotchas.md`).
- **Queues vs Workflows:** Queues = fire-and-forget message delivery with retries; Workflows = durable,
  resumable multi-step orchestration with per-step state. Reach for Workflows when steps must survive
  restarts and run in order.
