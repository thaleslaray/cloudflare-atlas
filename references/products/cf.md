# cf — Cloudflare CLI (unified API + Workers tooling)

> One command-line interface for the public Cloudflare API and Workers projects — **beta since
> 2026-09-28**. 2,900+ API commands (most print JSON) plus typed `cloudflare.config.ts` config.

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
- **Install:** `npm install --global cf` (also yarn/pnpm/bun). Beta as of Sep 2026 — commands and
  build output may change before stable.
- **Auth:** interactive `cf auth login` (browser approval; own credentials — it does **not** reuse the
  Wrangler login). CI: `CLOUDFLARE_API_TOKEN` (+ `CLOUDFLARE_ACCOUNT_ID`); the token beats any stored login.
- **Project config:** `cloudflare.config.ts` is typed; editors and agents get autocomplete for
  bindings and triggers. Replaces `wrangler.jsonc`/`toml` for new projects.
- **Dev/build/deploy:** `cf dev`, `cf build`, `cf deploy` run the framework's own command, else the
  Cloudflare Vite plugin 2.0 beta or Wrangler ≥ 4.136.0. Build Output lands in `.cloudflare/output/v0/`;
  `cf deploy --prebuilt` ships it without rebuilding; `cf previews deploy` for previews.
  `cf` does **not** run your `package.json` scripts (extra steps like `tsc -b` are skipped).
- **Resource commands:** zones, DNS, R2, D1… e.g. `cf dns records list --zone example.com`. They take
  the IDs the API expects (D1 database **ID**, not name) and act on **remote** data (`--local` only for
  some KV/D1/R2). `--dry-run` prints the request as JSON and needs no credentials.
- **Command discovery:** `cf cli search "<plain-language task>"` finds matching commands without
  memorizing subcommand trees.
- **CI:** set `CI=true` to avoid prompts; token via env (or a project `.env`, which `cf` reads for
  selected auth/context variables).
- **Markdown docs:** any page retrievable with `Accept: text/markdown` header (useful for agents
  ingesting docs programmatically).

## Gotchas
- **Beta status (Sep 2026):** commands, config schema, and build output can change. Pin versions in
  CI; expect breaking changes before stable release.
- **Never run `cf dev`/`build`/`deploy` in an unmigrated Wrangler project** (CI included): they ignore
  `wrangler.jsonc`, and *automatic configuration* may write a `cloudflare.config.ts` without your
  entrypoint/bindings and rewrite `package.json` — silently in CI. Resource commands are safe there.
- **Config migration is not automatic:** `cf migrate` produces follow-up items; read its output and
  verify bindings, environments, and build settings against the Wrangler-to-cf reference table.
- **Wrangler `env` blocks become modes** (`--mode`); only Vite and Astro framework commands accept
  `--mode`. Astro 6+ does not build with `cf` during the beta.
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
- Agent setup guide: https://developers.cloudflare.com/agent-setup/
- Wrangler migration: https://developers.cloudflare.com/cf/wrangler/migrate/
- Config explorer (typed fields): https://developers.cloudflare.com/cf/projects/config-explorer/
- CI guide: https://developers.cloudflare.com/cf/ci/
- Environment variables reference: https://developers.cloudflare.com/cf/environment-variables/