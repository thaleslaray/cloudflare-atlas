# cf — Cloudflare CLI (unified API + Workers tooling)

> One command-line interface for the public Cloudflare API and Workers projects — beta since
> 2026-09-28, **1.0 release candidate (`1.0.0-rc.1`) since 2026-11-17**. 2,900+ API commands (most print JSON) plus typed `cloudflare.config.ts` config.

## Contents
- When to use (and when not)
- Key API / access patterns
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- New Workers projects that want typed configuration (`cloudflare.config.ts`) and editor/agent autocomplete.
- Managing Cloudflare resources (zones, DNS, storage, security) from the terminal or CI without
  wrapping REST calls manually.
- Coding-agent workflows: `cf cli search <task>` discovers commands from plain language; agents run
  the same commands humans do.
- Migrating a Wrangler project: `cf migrate` converts `wrangler.jsonc`/`toml` to `cloudflare.config.ts`.
- **Not** for: dev/deploy of Wrangler projects you won't migrate (keep Wrangler there); one-off
  dashboard tasks where the UI is faster; products with no public API surface yet.

## Key API / access patterns
- **Install:** `npm install --global cf` (also yarn/pnpm/bun; `cf@latest` for the RC). **Stable in the RC:** `cloudflare.config.ts`, Build Output,
  `cf init`/`dev`/`build`/`deploy`, `cf previews deploy`, `cf workers versions create`, most generated API commands; a few rarely used API commands may still change before 1.0.
- **Auth:** interactive `cf auth login` (browser approval; own credentials — it does **not** reuse the
  Wrangler login). CI: `CLOUDFLARE_API_TOKEN` (+ `CLOUDFLARE_ACCOUNT_ID`); the token beats any stored login.
- **Project config:** `cloudflare.config.ts` is typed; editors and agents get autocomplete for
  bindings and triggers. Replaces `wrangler.jsonc`/`toml` for new projects.
- **Dev/build/deploy:** `cf dev`, `cf build`, `cf deploy` run the framework's own command, else the
  Cloudflare Vite plugin 2.0 (`@cloudflare/vite-plugin` ≥2.0.0-rc.0 per the RC post) or Wrangler **≥4.163.0**. Build Output lands in `.cloudflare/output/v1/`
  (was `v0`; `cf deploy` rebuilds on first run); `cf deploy --prebuilt` ships it without rebuilding; `cf deploy ./dist` deploys a static directory (assets-only Worker);
  `cf previews deploy --preview-name <n>` for previews; `cf deploy --no-provision` fails on bindings without resource IDs; `--force` overrides a remote/local conflict.
  `cf` does **not** run your `package.json` scripts (extra steps like `tsc -b` are skipped).
- **Resource commands:** zones, DNS, R2, D1… e.g. `cf dns records list --zone example.com`. They take
  the IDs the API expects (D1 database **ID**, not name) and act on **remote** data (`--local` only for
  some KV/D1/R2). `--dry-run` prints the request as JSON and needs no credentials.
- **Source maps:** `cf deploy` uploads every source map in the build output by default (since 2026-10-20). Vite plugin
  ≥1.64.0 generates Worker maps by default; opt out by setting `build.sourcemap` to `false` on the Worker's Vite environment
  (`ssr` by default). `cf migrate` does not carry `upload_source_maps` over.
- **Activate subscriptions in place** (changelog, 2026-11-25): OAuth sessions of `cf` and the Cloudflare MCP servers can now create **Workers Paid**, **R2** and **Zero Trust** subscriptions
  (CLI: `cf` `1.0.0-rc.5`+ and re-run `cf auth login` for the new OAuth scopes; account needs a verified email and a billing profile with a payment method). MCP clients with
  the `2026-07-28` spec + elicitation show the plan price and ask permission first; others are sent to the dashboard. Billing side → `billing.md`.
- **Send feedback** (`cf/agent-feedback/`, 2026-11-23): `cf feedback "<note>"`, repeatable `--field key=value`, or a JSON report via `--input-json <file>` (`=-` for stdin; flags win over
  JSON). Needs `cf auth login` or `CLOUDFLARE_API_TOKEN`. Prints a JSON receipt with `submission_id`; an agent that sends feedback must tell the user at the next natural break, with the ID.
  Reports always carry diagnostics (CLI version, OS, detected agent/model; whole report ≤16 KiB) regardless of telemetry settings.
- **Docs search:** `cf docs search "<query>"` (live docs, needs Internet; `cf` ≥1.0.0-beta.16) complements `cf cli search`.
- **Command discovery:** `cf cli search "<plain-language task>"` finds matching commands without
  memorizing subcommand trees.
- **CI:** set `CI=true` to avoid prompts; token via env (or a project `.env`, which `cf` reads for
  selected auth/context variables). Destructive commands without a terminal abort unless `--force`.
- **Custom API headers** (`cf` 1.0.0-beta.29+, Wrangler 4.160.0+): `CLOUDFLARE_API_HEADERS='{"X-Custom-Header":"value"}'` (JSON object of string values) is added to Cloudflare **API**
  requests only (not local emulation or OAuth) and overrides existing headers incl. auth; protected: `Host`, `Content-Type`, `Content-Encoding`, `Content-Length`, `Connection`, `Transfer-Encoding`, `Upgrade`, `TE`, `Trailer`.
- **Live logs:** `cf observability tail --worker <name>` (or `--zone`, `--all`; `--filters`) streams NDJSON; Worker events need Workers Logs on.
- **Static assets path:** `worker.assets.basePath` in `cloudflare.config.ts` (needs `cf` ≥1.0.0-beta.13) — see `workers.md` `assets.base_path`.
- **Markdown docs:** any page retrievable with `Accept: text/markdown` header (useful for agents
  ingesting docs programmatically).

## Gotchas
- **RC renames, no aliases:** e.g. `cf workers secrets bulk` → `bulk-edit`; generated commands use kebab-case (`cf accounts billing get-credits`); prompts/progress go to **stderr** (stdout = output only);
  `cf` no longer remembers the account — set `accountId` in config or `CLOUDFLARE_ACCOUNT_ID`; `--local` state lives in `.cloudflare/state`. Pin versions in CI.
- **Never run `cf dev`/`build`/`deploy` in an unmigrated Wrangler project** (CI included): they ignore
  `wrangler.jsonc`, and *automatic configuration* may write a `cloudflare.config.ts` without your
  entrypoint/bindings and rewrite `package.json` — silently in CI. Resource commands are safe there.
- **Config migration is not automatic:** `cf migrate` produces follow-up items; read its output and
  verify bindings, environments, and build settings against the Wrangler-to-cf reference table.
- **Wrangler `env` blocks become modes** (`--mode`/`-m`, selects what a function-form config returns); `cf build` accepts only `--mode`; `cf dev` forwards other args to the dev server.
- **Command count ≠ coverage depth:** 2,900+ commands are schema-generated; niche endpoints may have
  minimal flags or documentation. Verify specific subcommands with `cf <command> --help`.
- **Env vars steer it:** auth/targeting (`CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`,
  `CLOUDFLARE_ZONE_ID`), telemetry (`CF_SEND_TELEMETRY`; `DO_NOT_TRACK=1` always wins), `CI`, `NO_COLOR`.

## Pricing & limits
- No CLI charge is documented; costs come from the services it manages (Workers, R2, etc.).
- API commands go through the public Cloudflare API, so its normal rate limits apply.
- Verify on the live pricing page before quoting costs for any service managed through `cf`.

## Going deeper
- Official docs: https://developers.cloudflare.com/cf/
- Agent feedback: https://developers.cloudflare.com/cf/agent-feedback/
- Agent setup guide: https://developers.cloudflare.com/agent-setup/
- Wrangler migration: https://developers.cloudflare.com/cf/wrangler/migrate/
- Config explorer (typed fields): https://developers.cloudflare.com/cf/projects/config-explorer/
- CI guide: https://developers.cloudflare.com/cf/ci/
- Environment variables reference: https://developers.cloudflare.com/cf/environment-variables/