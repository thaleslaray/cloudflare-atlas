# Workers — serverless compute on V8 isolates at the edge

> Run JS/TS/Python/Rust/Wasm globally on **V8 isolates** (not containers) with sub-ms cold starts,
> across 300+ locations. The compute layer everything else on Cloudflare binds into.

## Contents
- When to use (and when not)
- Binding & config
- Key APIs (handlers & context)
- Workers Previews (per-branch environments)
- Putting a Worker behind Access (sign-in)
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- Edge APIs, request/response transformation, auth layers, routing/proxy, A/B tests, rate limiting.
- WebSocket apps, cron jobs, queue consumers — anywhere you want compute close to the user.
- The **host for bindings**: Workers is what you attach KV / D1 / R2 / DO / Queues / AI to.
- Pairs with: Static Assets (serve a frontend free), Durable Objects (state), Workflows (durable steps).
- **Not** for: long-running stateful processes (→ durable-objects), heavy/long compute or full
  containers (→ Containers), or anything needing a real filesystem / native binaries.
- **Python** (Pyodide, same isolates): **3.14** default from compat date **2026-09-08**; Django via
  `workers.wsgi`/`workers.asgi` (`uv run pywrangler init … --template …/django`).

## Binding & config (`wrangler.jsonc`)
```jsonc
{
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2025-01-01",  // ALWAYS current date; >= 2026-08-04 => nodejs_compat by default
  "vars": { "ENVIRONMENT": "production" },
  "kv_namespaces": [{ "binding": "MY_KV", "id": "..." }],
  "observability": { "enabled": true, "head_sampling_rate": 0.1 }
}
```
- **Inheritable**: `name`, `main`, `compatibility_date`, `routes`, `workers_dev`. **Non-inheritable**:
  all bindings (`vars`, `kv_namespaces`, `r2_buckets`, ...) — redeclare them per `env`.
- **Secrets** via CLI, never in config: `wrangler secret put API_KEY` → read as `env.API_KEY`.
- **Types**: run `wrangler types` after changing bindings; import the generated `Env`. Use
  `@cloudflare/workers-types` **v5** (simplified runtime types; dated entrypoints removed).
- Other bindings/triggers: `routes`, `triggers.crons`, `services` (Worker-to-Worker RPC),
  `durable_objects`, `queues`, `placement: { mode: "smart" }`, `analytics: { binding }` (Analytics SQL:
  `env.X.query({ query, params })`, one `SELECT`, Wrangler ≥4.145.0 — `runtime-apis/bindings/analytics-sql/`;
  datasets in `analytics.md`).

## Key APIs (handlers & context)
- **Module Worker** (use this, not Service Worker / `addEventListener`):
  ```typescript
  export default {
    async fetch(req: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
      return new Response("Hello");
    },
  };
  ```
- Other handlers: `scheduled(event, env, ctx)` (cron), `queue(batch, env, ctx)`, `tail(events, ...)`.
- `ctx.waitUntil(p)` — background work after the response (counts against CPU) ·
  `ctx.passThroughOnException()` — fall back to origin on error.
- Web-standard APIs: `fetch`, `Request`/`Response`, `URL`, `Headers`, Streams, `crypto.subtle` — post-quantum
  ML-KEM-768/1024 + ML-DSA-44/65/87 behind the `webcrypto_modern_algorithms` compat flag (2026-10-01).
- `ctx.exports.MyWorkflow.create({ params })` calls a Workflow declared in `exports` — no `workflows`
  binding needed (2026-09-27); shares instances with a same-`name` binding. Local-dev minimum versions:
  `developers.cloudflare.com/workflows/build/workers-api/`.
- `fetch()` subrequests support **`cf.vary`** — key the edge cache by request headers (e.g. `Accept`,
  `Accept-Language`); takes precedence over Cache Rules Vary for that subrequest.
- Dev loop: `wrangler dev` (local) · `wrangler dev --remote` (real resources) · `wrangler tail` (logs)
  · `wrangler deploy [--env staging] [--dry-run]` · auth profiles for multiple accounts (verify live).

## Workers Previews — 2026-09-22 (Wrangler ≥4.135.0)
- `npx wrangler preview` creates/updates an isolated Preview **of the same Worker** for the current branch
  (prod stays `wrangler deploy`). Each gets a **Preview URL** (latest) + immutable **Deployment URL**;
  `workers.dev` adds `X-Robots-Tag: noindex`. Public by default — gate with Access (table below).
- Settings are **not inherited**: a `previews` block (required, may be empty) holds `vars`/bindings; secrets
  via commands. DOs and Containers get a fresh namespace/app per Preview automatically; KV/D1/R2 isolate
  only if you bind a separate resource. Limits: crons, routes, Queue consumers, service bindings → prod only.
- Previews per Worker: **100** (Free) / **500** (Paid); **100** deployments per Preview; oldest auto-deleted.
  No separate pricing documented on `developers.cloudflare.com/workers/previews/`.
- Per-PR automation: Git-connected CI builds create a Preview per branch — `developers.cloudflare.com/workers/ci-cd/builds/build-branches/`.

## Putting a Worker behind Access (sign-in) — 2026-08-14
Require sign-in before a request reaches your Worker, without writing auth code. Needs **Zero Trust
enabled** on the account. Four scopes, chosen by the `destinations[].type` of a self-hosted Access
app (`POST /accounts/{account_id}/access/apps`):

| Scope | `type` | Extra field |
|---|---|---|
| Previews of **every** Worker (incl. future ones) | `all_preview_workers` | — |
| Prod + previews of **every** Worker | `all_workers` | — |
| Previews of **one** Worker | `preview_worker` | `worker_id` |
| Prod + previews of **one** Worker | `worker` | `worker_id` |
| One hostname / Custom Domain / path | self-hosted app domain | — |

- Dashboard: **Workers & Pages** → *Protect all Workers*, or a Worker's **Access** tab (*Previews only* / *All traffic*).
- **Worker-level Access breaks WebSockets** — upgrade requests fail with **403**. Anything using
  WebSockets (Durable Objects, Realtime, RDP-over-WS) needs a **hostname-based** Access app instead.
- Worker-level covers *every* route into that Worker (routes, Custom Domains, `workers.dev`, previews);
  hostname-based protects only that URL — use it to make just `/login` or `admin.example.com` private.
- With account-level Access on, exempt one Worker with a `worker` destination + a policy of
  `decision: "bypass"` and `include: [{ "everyone": {} }]`.

## Gotchas
- **CPU time, not wall time, is what's limited & billed** — `await`ing on a slow subrequest is free;
  burning CPU isn't. "Too much CPU time used" → offload to waitUntil/DO/Workers AI.
- **No persistent module-level state** — isolates reset unpredictably; never store data in globals.
  Use KV/D1/DO. Also: **no `fetch()` in global scope** (move it into a handler).
- **Bodies are streams, read once** — "Body has already been used" → `response.clone()` first. Stream
  large bodies (`TransformStream`); buffering >128 MB triggers Error 1102 `exceeded resource limits`.
- **Node built-ins**: default-on for compat date **≥ 2026-08-04** (older: add `nodejs_compat`).
- **Frameworks**: use Workers-native ones (Hono, itty-router); Express-style Node middleware won't run.
- DO calls: prefer **RPC** (`stub.method()`); legacy `stub.fetch()` still works for HTTP-shaped flows.
- **Static Assets bypass auth middleware** (measured 3× 2026-08-27): `run_worker_first` defaults to
  **false**, so a request matching a file in `public/` is served without invoking the Worker. Fix:
  `assets.run_worker_first: ["/admin", "/admin/*", "/api/*"]` — list extensionless canonical paths too
  (`html_handling` maps extensionless paths to their .html file); internal `env.ASSETS.fetch()` with `.html` gets a 307.
  Vitest calls the handler directly and won't catch it — prove with `wrangler dev` + curl (expect 302/401).

## Pricing & limits
> ⚠️ Pricing changes — verify on the live page (`developers.cloudflare.com/workers/platform/pricing/`)
> before quoting.

**Cost drivers** (Standard usage model, as of 2026-06):
- Requests: **10M/mo included, then $0.30/M**. Static-asset requests are **free & unlimited**.
- CPU time: **30M CPU-ms/mo included, then $0.02/M CPU-ms**. Duration (wall time) is **not** billed.
- Paid plan: **$5/mo minimum**. No egress/bandwidth charges.
- **Free plan**: 100,000 requests/day · 10ms CPU/invocation · no duration charge.

**Key limits:** memory **128 MB/isolate** · response **unlimited (stream)** · CPU/invocation
**30s default, 5min max** (Paid) / 10ms (Free) · Worker size **64 MiB uncompressed**, Free and Paid (no compressed limit) ·
startup **1s** · subrequests **10,000** Paid / 50 Free · env vars **128** Paid / 64 Free, 5 KB each ·
Workers/account **500** Paid. Verify on `developers.cloudflare.com/workers/platform/limits/`.

**Request body size is set by the *Cloudflare* plan, not the Workers plan** — Free/Pro **100 MB**,
Business **200 MB**, Enterprise **up to 5 GB** self-serve from the zone's Network page
(*Maximum Upload Size*); above 5 GB needs the account team. Over-limit returns **413**.

## Going deeper
- Deep-dive: live docs `developers.cloudflare.com/workers/` (canonical, fetch as Markdown). Official `cloudflare` skill `references/workers/` is an optional extra **if installed**.
- Agents/MCP/durable workflows → `cloudflare:agents-sdk`, `cloudflare:build-mcp`. Wrangler depth → `cloudflare:wrangler`. Best practices → `cloudflare:workers-best-practices`.
- Observability: OTLP export of logs/traces → `developers.cloudflare.com/workers/observability/opentelemetry-export/`
  (page renamed 2026-10; the old *exporting-opentelemetry-data* slug is retired).
  **Profiling in production** (CPU or Heap/allocation flamegraphs of deployed Workers & DOs, 1–50 s capture on live traffic): dashboard → Worker → Observability → *Flamegraph*, or `cf workers versions profile`; set `upload_source_maps` to true first → `developers.cloudflare.com/workers/observability/profiling-in-production/`
- **Testing** (real runtime via Miniflare, per-test-file storage): `@cloudflare/vitest-pool-workers` was
  **renamed 2026-08-19** → **`@cloudflare/vitest-plugin`** (API, config, `/config` `/types` subpaths unchanged);
  migrate: `npx @cloudflare/codemods vitest:pool-workers-to-vitest-plugin`. Outbound mocking → **`@msw/cloudflare`**.
