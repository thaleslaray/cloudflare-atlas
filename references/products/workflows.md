# Workflows — durable, multi-step applications

> Build **durable** apps as a series of independently-retriable **steps** with state that survives
> failures, restarts, and long sleeps (minutes → up to a year). Built on Workers.

## Contents
- When to use (and when not)
- Binding & config
- Core API
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- Long-running, multi-step orchestration where each step must **retry independently** and not re-run
  prior successful steps: ETL pipelines, user lifecycle (welcome → wait 7d → reminder), AI chains.
- You need to **sleep** (minutes to a year) or **wait for an external event** (approvals, webhooks)
  without consuming compute while idle.
- **vs Queues:** Queues for simple async/fire-and-forget message processing; Workflows when you need
  durable state across *ordered* steps, retries-per-step, sleep/wait, and human-in-the-loop.
- **vs Durable Objects:** DO for fine-grained stateful coordination/realtime; Workflows for
  step-sequenced durable execution. **Not** for a single quick request → just use a Worker.

## Binding & config (`wrangler.jsonc`)
```jsonc
{
  "compatibility_date": "2024-10-22",   // min for Workflows bindings
  "workflows": [
    { "name": "my-workflow", "binding": "MY_WORKFLOW", "class_name": "MyWorkflow",
      "schedules": ["0 * * * *"] }   // optional cron (≤100 exprs/account, ≤256 ch each)
    // "script_name": "other-worker"  → cross-script call
  ],
  "limits": { "cpu_ms": 300000 }        // optional: up to 5 min CPU/invocation
}
```
Class extends `WorkflowEntrypoint<Env, Params>` with an `async run(event, step)` method. Trigger via
`env.MY_WORKFLOW.create({ id, params })` from a Worker, Pages Function, cron, `schedules`, REST API, or wrangler.
On Paid, `schedules`-created instances get ~1h per firing without using a concurrency slot.

## Core API
```typescript
export class MyWorkflow extends WorkflowEntrypoint<Env, Params> {
  async run(event: WorkflowEvent<Params>, step: WorkflowStep) {
    const user = await step.do('fetch user', async () => this.env.DB.prepare(...).first());
    await step.do('call api', {
      retries: { limit: 10, delay: '10 seconds', backoff: 'exponential' },
      timeout: '30 minutes'
    }, async () => { /* ... */ });
    await step.sleep('wait', '7 days');              // also: step.sleepUntil(date)
    await step.waitForEvent('approval', { type: 'approved', timeout: '24h' });
  }
}
```
- `step.do(name, [config], fn)` — retriable unit; **name is the cache key** (must be deterministic).
- **`createBatch()`** (2026-10-08, Wrangler ≥4.148.0 locally): options object, ≤100 instances/call —
  `{ count, params }` (generated IDs) or `{ instances: [{ id, params }] }`; returns `{ created, errors }`
  (existing/duplicate IDs land in `errors`, not skipped silently). Array form deprecated, still works.
- Parallel: `Promise.all([step.do(...), step.do(...)])`. Idempotency: check-then-execute.
- `retries.delay` can be a **function** `({ ctx, error }) =>` duration — compute the next delay from
  `ctx.attempt`/`error`; returns a duration string, ms number, or a promise of either.
- **Rollback handlers** on `step.do()` enable saga-style compensation; they now receive step context —
  `{ ctx, error, output }` (`output` = the forward step's returned value, `undefined` if it failed);
  `rollbackConfig` sets retries/timeout for the handler itself.

## Gotchas
- **Floating promises:** you MUST `await` every `step.*` call — un-awaited = fire-and-forget, breaks
  durability ordering. Always `await step.do(...)`.
- **Serialization:** `step.do` return values are persisted (JSON-serializable, ≤1 MiB). Store state
  via returns, NOT module/local vars (lost on hibernation). Large data → R2/KV, return a reference
  (or return `ReadableStream<Uint8Array>` for big binary output).
- **Determinism:** no `Date.now()`/`Math.random()`/dynamic step names *outside* steps — replay breaks.
  Put non-deterministic logic inside a `step.do`.
- **NonRetryableError:** throw it (from `cloudflare:workers`) to fail a step permanently and skip
  remaining retries. `waitForEvent` *throws* on timeout — wrap in try/catch.
- `step.sleep` / `waitForEvent` don't count toward the max-steps limit; `waiting` instances don't
  count toward concurrency. Completed instance state is auto-deleted after the retention period.

## Pricing & limits
> ⚠️ Pricing changes — verify live (`developers.cloudflare.com/workflows/reference/pricing/`).

**Cost drivers** — Workers Standard SKUs (requests + CPU) **plus** per-step + storage billing that
starts **no earlier than 2026-08-10** (before that: no extra Workflows charge):
- **Requests** (invocations only; subrequests are free): Paid = 10M/mo + **$0.30/M**.
- **CPU time** (idle/sleep/I-O-wait don't count): Paid = 30M ms/mo + **$0.02/M ms**.
- **Steps** (per-step billing, from 2026-08-10): Paid = 500k steps/mo + **$0.80/100k** (~$8e-6/step);
  Free = 3,000 steps/day.
- **Storage** (persisted state, billed from 2026-08-10): Paid = 1 GB + **$0.20/GB-mo**.
- Free tier: shares Workers 100k req/day, 10 ms CPU/invocation, 1 GB storage.

**Key limits** (Free / Paid): steps/instance **1,024 / 10,000** (→25,000 configurable) · CPU/step
**10 ms / 30 s** (→5 min) · wall-clock/step **unlimited** · step return **1 MiB** · event payload
**1 MiB** · state/instance **100 MB / 1 GB** · max sleep **365 days** · concurrent running instances
**100 / 50,000** · create rate **100/s / 300/s** · retention **3 / 30 days max** · name 64 ch · ID 100 ch.
**Default retention changed 2026-09-10 (changelog; limits page not yet updated):** Workflows created on
Paid from that date keep completed/errored state **7 days** by default (max still 30); older Workflows
keep 30; Free stays 3. Override per instance: `create({ retention: { successRetention, errorRetention } })`.
Verify on `developers.cloudflare.com/workflows/reference/limits/`.

## Going deeper
- Covered by the official `cloudflare` skill (`references/workflows/`) — use it for full API,
  patterns (fan-out, parent-child, race, scheduled chains), testing/introspection, and debugging.
- REST/Workers API: `developers.cloudflare.com/workflows/build/workers-api/`.
