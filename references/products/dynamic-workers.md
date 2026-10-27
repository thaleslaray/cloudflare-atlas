# Dynamic Workers — spin up isolated Workers on demand to execute code

> Spin up an unlimited number of Workers **at runtime** to execute arbitrary, possibly-untrusted
> code in a secure, sandboxed isolate. The lowest-level primitive for "run this code I was handed
> right now" — you compose the Worker, its bindings, its network access, and its limits per call.

## Contents
- When to use (and vs. Workers for Platforms / Linux sandboxes)
- Binding & config
- Core API (`load` vs `get`, `WorkerCode`)
- Sandboxing: bindings, egress, limits
- Gotchas
- Pricing & limits + status
- Going deeper

## When to use
- **Run untrusted / user-provided / AI-generated code** in an isolated V8 isolate, on demand — code
  is supplied as **strings at runtime**, no deploy step per snippet.
- **AI agent "Code Mode"**: give the LLM an API and let it write+execute code instead of tool calls
  (cuts inference tokens/cost — data is processed in-isolate, not round-tripped through the model).
- **"Vibe code" / generated apps, fast previews/playgrounds** (load in milliseconds), custom
  on-the-fly automations, **multi-tenant platforms** running user-uploaded code.
- **Not** for: your own first-party code (just deploy a normal Worker); long-running OS-level
  processes, arbitrary binaries, a full filesystem, or non-JS/Python runtimes (→ Containers).

### Dynamic Workers vs Workers for Platforms vs Linux sandboxes
- **Dynamic Workers** — *lowest-level primitive*. A `Worker Loader` binding (`env.LOADER`) that
  creates ephemeral isolates **in-process at runtime** from code strings. You hand-build each
  Worker's `env`, `globalOutbound`, and `limits`. Best for ephemeral, per-request, untrusted code.
- **Workers for Platforms (WfP)** — *deploy-time* multi-tenancy: customers' Workers are **uploaded
  and deployed** into dispatch namespaces, then routed to via a dispatcher Worker. Durable,
  managed, account-level — not runtime code injection. Use when tenants ship persistent apps.
- Linux sandbox (atlas: `sandbox.md`) — runs code in a **Cloudflare Container** (full Linux sandbox: processes, a
  filesystem, arbitrary languages/binaries, shell). Heavier and slower to start than a Dynamic
  Worker isolate. Use when you need a real OS environment, not just a JS/Python isolate.
- Rule of thumb: untrusted JS/Python, millisecond starts, per-request → **Dynamic Workers**;
  persistent tenant deployments → **WfP**; needs an OS/filesystem/binaries → a Linux sandbox (`sandbox.md`).

## Binding & config (`wrangler.jsonc`)
```jsonc
{
  "worker_loaders": [
    { "binding": "LOADER" }
  ]
}
```
Unlike most bindings this points at **no external resource** — it just exposes the Worker Loader
API as `env.LOADER`. The Worker holding this binding is the "loader Worker" / supervisor.

## Core API (`env.LOADER`)
Two loading modes:
- **`load(code)`** → `WorkerStub`. Always creates a **fresh** isolate; no caching. Best for
  one-off execution (e.g. each new AI-generated tool call).
- **`get(id, async () => code)`** → `WorkerStub` (returned **synchronously**, no `await`). Caches
  by `id`: the isolate may stay warm and be reused across requests. The callback runs **only** when
  no warm instance exists (so you skip re-loading code from storage). Best when the same code gets
  repeated requests (building apps).

`WorkerStub.getEntrypoint(name?, opts?)` returns the Worker's `export default` (or a named
`WorkerEntrypoint`); call `.fetch(request)` or RPC methods on it.

**`WorkerCode`** (returned by the callback / passed to `load`):
- `compatibilityDate` (req), `compatibilityFlags?` (Python needs `["python_workers"]`).
- `mainModule` (req) — must be a key in `modules`.
- `modules: Record<string, string | Module>` — string content needs a `.js`/`.py` extension, or use
  typed objects `{js}`, `{cjs}`, `{py}`, `{text}`, `{data: ArrayBuffer}`, `{json}`.
- `env` — the environment object handed to the dynamic Worker (structured-clonable values +
  service-binding stubs). This is how you inject capabilities.
- `globalOutbound?: ServiceStub | null` — network policy (see below).
- `limits?: { cpuMs, subRequests }`, `tails?: ServiceStub[]`, `allowExperimental?`.

```js
const worker = env.LOADER.load({
  compatibilityDate: "2026-06-26",
  mainModule: "src/index.js",
  modules: { "src/index.js": `export default { fetch() { return new Response("hi"); } };` },
  globalOutbound: null,            // cut off from the network
});
return worker.getEntrypoint().fetch(request);
```

## Sandboxing — bindings, egress, limits
**Capability-based security** (powered by Workers RPC / Cap'n Web): a dynamic Worker can access
**only what you explicitly hand it**. Stubs can't be forged; the only way to get one is to receive it.

- **Custom bindings** — export a `WorkerEntrypoint` class in the loader Worker, instantiate it with
  `ctx.exports.MyClass({ props })`, and pass the stub in `WorkerCode.env`. The dynamic Worker calls
  `this.env.X.method()`; each call is an RPC **back into your loader Worker**, where the real logic
  (auth, key-prefixing, logging) runs. `ctx.props` are visible only to the loader, never the
  dynamic Worker — use them to scope per-tenant (e.g. prefix a shared KV/R2/D1 per customer).
- **Egress control** via `globalOutbound`:
  - omitted → **inherits parent's network access** (usually full public Internet — the unsafe default).
  - `null` → fully cut off; `fetch()`/`connect()` throw.
  - a service stub (e.g. `ctx.exports.HttpGateway()`) → every `fetch`/`connect` is **routed through
    your gateway** to allowlist destinations, inject credentials the worker never sees, or audit.
- **Custom limits** — `limits: { cpuMs, subRequests }` per invocation; exceeding either throws
  immediately. Can also be set on `getEntrypoint(null, { limits })`; if set both places, the **lower**
  applies. Without custom limits, your account/plan Workers limits apply.
- **Durable Object Facets** — give dynamic code **isolated persistent SQLite** without handing it a
  DO namespace: a supervisor DO calls `this.ctx.facets.get()` to spawn a facet (an instance of the
  dynamically-loaded `DurableObject` class) with its **own** SQLite DB, separate from the supervisor's.

## Gotchas
- **`get()` cache key = id; callback must be deterministic.** If anything in the code/config changes,
  use a **new id** (e.g. `name:version` or a hash of the code) — otherwise you may serve stale code.
  Conversely, reuse a stable id for identical code to get caching **and** avoid extra billing.
- **No build step.** TypeScript/npm deps must be transpiled+bundled first — use
  `@cloudflare/worker-bundler` (`createWorker({ files })`) which returns `{ mainModule, modules }`.
- **Python is much slower to start** than JS — for one-off AI-generated code prefer JS (LLMs write
  either equally well). Python also requires the `python_workers` compat flag.
- **No isolate affinity:** two requests on the same stub may hit different isolates; the `get`
  callback can fire more than once. Don't assume in-isolate state persists across requests — use
  facets/bindings for state.
- **Default network is OPEN** when `globalOutbound` is omitted — for untrusted code, always set `null`
  or a gateway explicitly.
- **Billing trap:** `load()` (or `get` with no/random id) counts as a new Dynamic Worker **per
  invocation**. Use `get()` with a stable id for repeated requests.

## Pricing & limits + status
> ⚠️ Verify on the live page (`developers.cloudflare.com/dynamic-workers/pricing/`) — this product is
> new and fast-moving (docs dated mid-2026; billing rules changed May 26, 2026).

- **Workers Paid plan only.** Three billing dimensions:
  - **Dynamic Workers created daily:** 1,000 unique/month included, then **+$0.002 per Dynamic
    Worker per day**. Unique = distinct (Worker ID + code); count resets daily.
  - **Requests:** 10M/month included, **+$0.30/M** — Workers Standard rates, on your Workers bill.
    Each `fetch()` and each RPC call into a dynamic stub counts (returned `RpcTarget` stubs share the
    session and aren't re-billed).
  - **CPU time:** 30M CPU-ms/month included, **+$0.02/M CPU-ms**. Unlike standard Workers, bills
    **startup time** (isolate init + code parse) **plus** execution time.
- **Concurrency — distinct Dynamic Workers with in-flight requests** (`platform/limits/`): **4 per
  Worker request**, **10 per Durable Object** (raised from 4, 2026-08-28). Multiple in-flight requests
  to the *same* Dynamic Worker count as one; a DO shares a single I/O context across its concurrent
  requests, which is why its budget is per-object rather than per-request.
- View usage: dash → Workers & Pages → Overview, or GraphQL `distinctDynamicWorkerCount` (data from
  2026-06-01). Per-invocation CPU/subrequest limits default to your plan limits unless overridden.
- **Status: open beta** since 2026-03-24 ("Dynamic Workers are now in open beta for all paid Workers
  users" — changelog `2026-03-24-dynamic-workers-open-beta`); no GA announcement as of 2026-08-25.
  Billing for "created daily" started 2026-05-26. Treat APIs and prices as subject to change —
  **verify live** before quoting or relying on stability.

## Going deeper
- No dedicated official `cloudflare` skill ref for this yet — this file is the primary reference.
- Examples: Dynamic Workers Starter & Playground, Code Mode example (LLM writes JS to orchestrate
  tools in one sandbox), Dynamic Workflows (per-tenant Workflow logic). See `pages/dynamic-workers/`.
- Related atlas refs: `agents.md` (Code Mode), `cloudflare-for-platforms.md`, `sandbox.md`,
  `durable-objects.md` (facets), `workers.md` (bindings/RPC).
