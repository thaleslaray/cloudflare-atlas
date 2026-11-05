# TanStack Start — full-stack React on one Worker (Vite plugin, no adapter)

> SSR, server functions and static assets run in a **single Worker** through `@cloudflare/vite-plugin`
> — the framework's `ssr` environment *is* the Worker, no adapter translating build output. Start 1.0
> is stable (2026-10-13); Cloudflare is a TanStack Gold sponsor and Official Hosting Partner.

## Contents
- When to use (and when NOT)
- Canonical config (checked live 2026-11-05)
- Bindings & custom entrypoint
- Prerendering
- Local dev, remote bindings, deploy
- Gotchas (official, then practitioners)
- Open issues
- Limits
- Timeline
- Going deeper

## When to use
- New full-stack React app that should live entirely on Cloudflare: pages + server functions + D1/R2/KV/AI
  bindings + Durable Objects / Queues / Cron / Workflows **in the same Worker**.
- Target stack that fits: TanStack Start + Tailwind + shadcn/ui + D1/Drizzle + Better Auth + R2 + Durable Objects.
- Start and React Router use the Vite plugin directly (no adapter); Astro, SvelteKit, Nuxt etc. go through adapters/presets
  (`workers/framework-guides/automatic-configuration/`).

### When NOT
- **Pure API / webhooks / no UI** → Hono on Workers (`products/workers.md`); a framework adds weight for nothing.
- **Content / marketing / docs site** → Astro (static-first, no per-request CPU).
- **Internal SPA behind login** → Vite + React + Hono (or the React guide); no SSR needed.
- **Existing Next.js app** → `frameworks/vinext.md` (experimental/beta). OpenNext is the documented fallback.
- Need React Server Components by default → Start treats RSC as an **opt-in** integration (1.0 post); the
  Cloudflare guide does not cover it. Check before promising it.

## Canonical config
Do not improvise this; copy it. Source: `workers/framework-guides/web-apps/tanstack-start/`.
```ts
// vite.config.ts — ORDER MATTERS: cloudflare() first, tanstackStart() second
import { defineConfig } from "vite";
import { tanstackStart } from "@tanstack/react-start/plugin/vite";
import { cloudflare } from "@cloudflare/vite-plugin";
import react from "@vitejs/plugin-react";
export default defineConfig({
  plugins: [cloudflare({ viteEnvironment: { name: "ssr" } }), tanstackStart(), react()],
});
```
```jsonc
// wrangler.jsonc
{ "$schema": "node_modules/wrangler/config-schema.json",
  "name": "<YOUR_PROJECT_NAME>",
  "compatibility_date": "2026-11-05",                 // today's date
  "compatibility_flags": ["nodejs_compat"],
  "main": "@tanstack/react-start/server-entry",       // default entry; point at src/server.ts for a custom one
  "observability": { "enabled": true } }
```
- `package.json` scripts: `dev: vite dev` · `build: vite build` · `preview: vite preview` ·
  `deploy: npm run build && wrangler deploy` · `cf-typegen: wrangler types`.
- Install: `npm i -D @cloudflare/vite-plugin wrangler`. New app: `npm create cloudflare@latest -- my-app --framework=tanstack-start`.
- **Existing project without `wrangler.jsonc`:** `wrangler deploy` (or `wrangler setup`) detects Start and generates
  config; needs **Wrangler ≥ 4.68.0** (`workers/framework-guides/automatic-configuration/`).
- **Remove `nitro()`** (or any other deployment adapter) and its import before adding the Cloudflare plugin.
  **Rsbuild is not supported** — migrate to Vite first.
- `nodejs_compat` is on by default for compat date ≥ **2026-08-04**; the flag is redundant there (harmless, ignored).
- **Plugin v1 vs v2 beta:** the guide uses **v1** (stable, `wrangler.jsonc`, `wrangler deploy`). v2 beta uses
  `cloudflare.config.ts` + `cf deploy`, writes `.cloudflare/output`, Vite ≥ 7, and **Wrangler cannot deploy it**.
  Never mix the two (`workers/vite-plugin/v2-beta/`).

## Bindings & custom entrypoint
```ts
import { createServerFn } from "@tanstack/react-start";
import { env } from "cloudflare:workers";            // server-side only
const getData = createServerFn().handler(async () => env.MY_BUCKET.get("key"));
```
- Bindings = `import { env } from "cloudflare:workers"` **inside** server functions / server routes. Types via `wrangler types`.
- TanStack's own doc: **read env per request, never at module scope** — on Workers it is injected at request time.
- `cloudflare:workers` must never reach the client bundle (the Vite error often points at an unrelated file —
  Hongwei Wang suggests one server-only file that owns the import).
- **Custom entry** (`src/server.ts`, then `"main": "src/server.ts"`): reuse Start's handler and add the rest.
```ts
import handler from "@tanstack/react-start/server-entry";
export { MyDurableObject } from "./my-durable-object";      // DO + Workflow classes: named exports
export default {
  fetch: handler.fetch,
  async queue(batch, _env, _ctx) { /* … message.ack() */ },
  async scheduled(event, _env, _ctx) { /* … */ },
} satisfies ExportedHandler<Env>;
```
- Run `npm run cf-typegen` **before** adding the custom entry (TS). Declare DOs/Workflows/Queues/crons in `wrangler.jsonc`.
- Test cron locally: `curl "http://localhost:3000/cdn-cgi/local/scheduled?cron=*+*+*+*+*"`.
- Service bindings: add `services`, call `env.AUTH_SERVICE.verify(…)` from a server function; target must extend `WorkerEntrypoint`.
- **Auxiliary Workers** (`auxiliaryWorkers: [{ configPath }]` in `cloudflare()`) need **Vite ≥ 7**; `wrangler deploy` ships only
  the entry Worker — deploy each auxiliary from `dist/<name>/wrangler.json`. Assets are reachable only from client + entry Worker.
- Intercepting a WebSocket upgrade before `handler.fetch` is a **community pattern**, not official text.

## Prerendering
```ts
tanstackStart({ prerender: { enabled: true } })   // inside the same plugins array, after cloudflare()
```
- Needs `@tanstack/react-start` **≥ 1.138.0**. Output is served as static assets.
- ⚠️ Runs **at build time with LOCAL env vars, secrets and bindings data** — not production. For production data use
  remote bindings. In CI set **`CLOUDFLARE_INCLUDE_PROCESS_ENV=true`** and pass values as env vars (Workers Builds: build settings).
- Practitioners: prerender that reads R2/D1 makes the build depend on a live bucket (Raul Carini deferred the photo manifest to hydration).
  `crawlLinks: true` follows every link: `?query` URLs overwrite the same `index.html`, and **guarded pages (`/dashboard`) get a static
  copy served without their guard** — filter private paths (Hongwei Wang). Any module touching a binding at import time can fail `vite build`.

## Local dev, remote bindings, deploy
- `vite dev` runs the Worker in local `workerd` with simulated bindings; state in `.wrangler/state` (add it to `server.watch.ignored`
  or each DB write reloads the page — Hongwei Wang). `vite preview` tests the built output. Secrets: `.dev.vars`.
- **Remote bindings** (`remote: true` per binding; `remoteBindings` plugin option defaults `true`) — your code still runs locally:
  - Supported: AI (**always remote; `remote:false` is an error**), Analytics Engine, Browser Run, D1, Email, Flagship, Images, KV,
    Media Transformations, mTLS, Queues, R2, Service Bindings, Vectorize.
  - **Never remote:** Durable Objects, Workflows, Containers, Hyperdrive, Rate Limiting, Static Assets, `vars`, secrets, Version Metadata.
  - Local DOs/Workflows *can* talk to remote bindings; to reach a deployed DO, bind a remote Service Binding to a deployed Worker.
  - **No `wrangler dev --remote` equivalent** in the Vite plugin. Remote writes hit real data and bill normally.
- **Deploy:** `npm run deploy`. **Workers Builds:** set build command `npm run build` (deploy default `npx wrangler deploy`); it does
  **not** honor `[build]` Custom Builds in the Wrangler config. No Wrangler config in the repo → autoconfig opens a PR.
- Static assets: the plugin adds them automatically when the `client` environment builds. Add `assets` only for routing
  (`not_found_handling`) or the `ASSETS` binding. Side effect: Workers with Static Assets get no `ctx.access` (Cloudflare Access).

## Gotchas
Official / doc-backed:
- **`server-entry not found`** → plugin order. Cloudflare first (sakimyto lost ~3 h to this, 2026-03, on Pages).
- **Memory:** Zod < **4.5.0** uses substantially more memory per schema (limits page). Use ≥ 4.5.0.
- **Node APIs:** `node:fs` is a memory-based **virtual** filesystem (`/bundle` read-only, `/tmp` writable) — no real disk. `node:child_process`,
  `node:worker_threads`, `node:vm`, `node:http2`, `node:sqlite`, `node:tty` import fine but are **non-functional stubs** (`workers/runtime-apis/nodejs/`).
- Native addons (`sharp`, `@resvg/resvg-js`, `@napi-rs/canvas`) can't load on Workers (vinext README; same runtime constraint).
Practitioner reports (2026, not official — treat as leads, re-check against your version):
- **Per-request factories:** build the Better Auth instance and the DB client per request, never as module singletons (Rokcso; Hongwei Wang).
- **Better Auth on Workers:** `tanstackStartCookies()` must be the **last** plugin; set `ipAddressHeaders: ["cf-connecting-ip"]`;
  its CLI runs in Node and can't resolve `cloudflare:workers` (use a bindings-free config just to generate tables).
- **Background work:** unawaited promises vanish. `ctx.waitUntil()` exists but inside framework server functions you often have no `ctx`;
  OVOV's rule became *await everything*, and `waitUntil` only from the custom entry where `ctx` is in hand.
- **Postgres:** direct TCP from Workers to a pooler hung intermittently; Hyperdrive in front was required (OVOV). D1 is SQLite: no nested
  transactions (Rokcso).
- **Tree-shaking:** Zod marks itself side-effect-free, so Vite dropped its locale setup and messages became "Invalid input" in prod (Harrison Milbradt).
- **Stale tabs:** after a deploy, old tabs request chunks that no longer exist (Harrison Milbradt).
- **Route tree:** `routeTree.gen.ts` is generated — commit it or types break on a clean clone (Raul Carini).
- **Lost from Next.js:** `next/image`, `next/font`, `@vercel/og`. OG images → separate Worker with `workers-og` (Tightknit).

## Open issues (state read 2026-11-05)
- [TanStack/router#7740](https://github.com/TanStack/router/issues/7740) — SPA shell includes `/` loader data with the Cloudflare plugin (open).
- [TanStack/router#6330](https://github.com/TanStack/router/issues/6330) — build with prerender + Cloudflare plugin fails (open).
- [TanStack/router#7431](https://github.com/TanStack/router/issues/7431) — `__vite_ssr_import_*__.u is not a function` in `vite dev` (open).
- [workers-sdk#13425](https://github.com/cloudflare/workers-sdk/issues/13425) — HMR 30–40 s: **closed** (the research copy listed it open).
- Re-check state before citing: `gh api repos/TanStack/router/issues/<n> --jq .state`.

## Limits (`workers/platform/limits/`, verified 2026-11-05)
| | Free | Paid |
|---|---|---|
| CPU per HTTP request | 10 ms | 30 s default, max 5 min (`limits.cpu_ms`) |
| Memory / isolate | 128 MB | 128 MB |
| Worker size | **64 MiB uncompressed** | 64 MiB; **no compressed limit** |
| Subrequests / invocation | 50 | 10,000 |
| Startup time | 1 s | 1 s |
| Static assets | 20,000 files · 25 MiB each | 100,000 files · 25 MiB each |
- The "3 MiB free / 10 MiB paid compressed" figure in older blogs is **obsolete** — do not quote it.
- `waitUntil()` extends up to 30 s after the response. Pricing: `products/workers.md`; verify on the live page before quoting.

## Timeline (official)
| Date | Source | Milestone |
|---|---|---|
| 2025-09-23 | [Cloudflare blog](https://blog.cloudflare.com/cloudflare-astro-tanstack/) | Cloudflare + Netlify sponsor TanStack; Start 1.0 RC announced |
| 2025-10-24 | [changelog](https://developers.cloudflare.com/changelog/post/2025-10-24-tanstack-start/) | Vite plugin supports TanStack Start |
| 2025-12-16 | [changelog](https://developers.cloudflare.com/changelog/post/2025-12-16-wrangler-autoconfig/) | `wrangler deploy` autoconfig (experimental) |
| 2025-12-19 | [changelog](https://developers.cloudflare.com/changelog/post/2025-12-19-tanstack-start-prerendering/) | Prerendering with build-time bindings (≥ 1.138.0) |
| 2026-01-20 | [changelog](https://developers.cloudflare.com/changelog/post/2026-01-20-auxiliary-workers/) | Auxiliary Workers with full-stack frameworks (Vite ≥ 7) |
| 2026-10-13 | [TanStack blog](https://tanstack.com/blog/tanstack-start-1-0) | **Start 1.0 stable**; guide last updated the same day |
| 2026-10-26 | [docs](https://developers.cloudflare.com/workers/framework-guides/automatic-configuration/) | Autoconfig page (Wrangler ≥ 4.68.0) |
- Unconfirmed: which Vite major Start 1.0 requires (sources conflict); RSC status beyond "opt-in".

## Going deeper
- Live guide: `curl -sL -H "Accept: text/markdown" https://developers.cloudflare.com/workers/framework-guides/web-apps/tanstack-start/`
- Plugin reference: `workers/vite-plugin/reference/{api,vite-environments,static-assets}/` · bindings: `workers/local-development/bindings-per-env/`.
- TanStack side: `tanstack.com/start/latest/docs/framework/react/guide/{hosting,environment-variables}`.
- Related atlas refs: `products/workers.md`, `products/d1.md`, `products/r2.md`, `products/durable-objects.md`,
  `products/hyperdrive.md`, `products/queues.md`, `products/workflows.md`.
- Same plugin, other frameworks: React Router (live docs say **v8**; SPA mode and prerendering unsupported with the plugin).
- Source research: `~/pesquisas/pesquisa-tanstack-start-cloudflare-2026-11-05.md` (190 sources). Re-checked live on 2026-11-05; corrected vs. that file: `node:fs` exists (virtual FS),
  `waitUntil` advice (see Gotchas), workers-sdk#13425 closed, React Router is v8, Harrison Milbradt's R2-prerender claim not found on his page.
