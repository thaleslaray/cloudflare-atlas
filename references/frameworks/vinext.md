# vinext — Next.js API on Vite, deployed to Workers (⚠️ EXPERIMENTAL / beta)

> Cloudflare's Vite plugin that **reimplements the Next.js API surface** (not a fork, not `next build` output).
> Keep `app/`, `pages/`, `next.config.js`; swap the toolchain. **Not a drop-in replacement** — its own README says
> "under active development", the blog says "experimental", the docs say "beta". Never sell it as production-safe.

## Contents
- Status (read first)
- When to use (and when not)
- Setup & deploy
- Bindings & caching
- Known gaps
- Going deeper

## Status (read first)
| Source | Wording |
|---|---|
| Blog, 2026-02-24 (`blog.cloudflare.com/vinext/`) | "**Status: Experimental**", not battle-tested at scale; ~94% of the Next.js 16 API surface |
| Workers docs, Next.js guide (updated 2026-08-25) | "vinext is **in beta**" — run `npx vinext check` before adopting for production |
| README (read 2026-11-05) | "**Under active development**… not yet a drop-in replacement for every application or production workload" |
- The same Workers guide **recommends vinext as the default way to run Next.js on Workers** (C3 `--framework=next` and
  `wrangler deploy` autoconfig both configure it). Recommended ≠ stable: label it experimental/beta whenever you propose it.
- The blog is **stale in places**: it says no build-time static prerender and shows `vinext deploy`. Today the README/docs list
  static generation, ISR and `output: "export"` as working, and the deploy command is `npx @vinext/cloudflare deploy`.
  Trust the README and the docs page over the blog.
- Targets **Next.js 16.x only**. README peer deps: `react ^19.3.1`, `react-dom ^19.3.1`, `react-server-dom-webpack ^19.3.1`, `vite ^8.0.0`.

## When to use
- You **already have a Next.js 16 app** and want it on Workers without OpenNext. Start with `npx vinext check`.
- vinext's own README says OpenNext is the safer, more proven choice when you need broad Next.js coverage; the Workers guide keeps
  OpenNext documented for apps that can't migrate because of a gap, and Pages only for a static export.
- **Not** for a new project on the target stack → `frameworks/tanstack-start.md`. **Not** for content sites → Astro.
- **Not** if you depend on Vercel-specific features (`@vercel/og`, Vercel KV/Blob/Postgres), webpack/Turbopack config or `next/jest`.

## Setup & deploy
```bash
npx vinext check                  # compatibility scan — do this first
npx vinext init                   # non-destructive; `next dev` keeps working; pick Cloudflare Workers
pnpm create vinext-app@latest my-app     # new project (or: npm create cloudflare@latest -- my-app --framework=next)
npx vinext init --platform=cloudflare    # README prerequisite before the first deploy
npx @vinext/cloudflare deploy            # build + deploy (--env <name> picks the Vite mode; --preview = --env preview)
```
- README says Cloudflare init installs **`cf` and Vite plugin v2 (beta)** and generates `cloudflare.config.ts`; deploy goes through `cf`.
  So a vinext-on-Workers project is on the **v2 beta path** (Wrangler cannot deploy it — see `frameworks/tanstack-start.md`).
  Auth: `cf auth login` locally or `CLOUDFLARE_API_TOKEN` (Edit Cloudflare Workers template) in CI; set `accountId` or `CLOUDFLARE_ACCOUNT_ID`.
- Agent route: `npx skills add cloudflare/vinext`, then "migrate this project to vinext".
- Scripts after `init`: `dev:vinext`, `build:vinext` (projects from `create-vinext-app`: plain `dev` / `build` / `deploy`).

## Bindings & caching
- Bindings: `import { env } from "cloudflare:workers"` in server components, route handlers and server actions — no `getPlatformProxy()`,
  no custom worker entry. D1, R2, KV, Durable Objects, AI, Queues, Vectorize all work.
- Declare bindings in `cloudflare.config.ts` (`bindings.d1(...)`, `bindings.kv()`); types generate into `.cloudflare/types` (add to `tsconfig`).
- Cache is pluggable (default `MemoryCacheHandler`). Adapters in `@vinext/cloudflare/cache/*`: `kvDataAdapter()` (`"use cache"` data; binding
  default `VINEXT_KV_CACHE`), `workersCacheCdnAdapter()` (page ISR), `staticAssetsAdapter()`, `responseStoreAdapter()` (needs an R2 bucket).
- Traffic-aware warming (formerly "TPR"): `deploy --traffic-aware-warm-cache`; needs a **custom domain** (no `workers.dev`) and a token with
  Zone › Analytics › Read + Zone › Zone › Read. Old `--experimental-tpr` names remain as aliases.

## Known gaps (README, 2026-11-05 — re-read before promising anything)
- `"use cache"` partial; **Cache Components / Partial Prerendering** incomplete.
- No full build-time image/font optimization (images optimized at request time on Cloudflare; Google Fonts from CDN).
- Native modules (`sharp`, `resvg`, `satori`, `lightningcss`, `@napi-rs/canvas`) can fail in App Router dev; Workers can't load Node-API addons.
- `preferredRegion` ignored; `runtime` doesn't pick where a route runs.
- Intentionally unsupported: Vercel-only features, AMP, legacy `next export`, webpack/Turbopack config, `next/jest`, `create-next-app`.
- Other hosts: via the Nitro Vite plugin, with less support than Workers.

## Going deeper
- Docs: `developers.cloudflare.com/workers/framework-guides/web-apps/nextjs/` · `vinext.dev/compatibility` (module-level dashboard).
- Source: `github.com/cloudflare/vinext` (README is the most current page) · blog: `blog.cloudflare.com/vinext/`.
- OpenNext fallback: `workers/framework-guides/web-apps/opennext/`. Related: `products/workers.md`, `products/pages.md`.
