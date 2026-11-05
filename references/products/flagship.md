# Flagship — feature flags evaluated at the edge

> Cloudflare's feature flag service. Control feature visibility without redeploying: define flags with
> **targeting rules** and **percentage rollouts**, then evaluate them inside Workers via a native
> binding (`env.FLAGS`) or anywhere via OpenFeature SDKs. OpenFeature-compatible (swap providers freely).

## Contents
- When to use (and when not)
- Binding & config
- Ways to evaluate
- Targeting & rollouts
- Gotchas
- Limits & pricing
- Going deeper

## When to use
- **Feature toggles** (on/off) without a redeploy — flip a flag, changes propagate globally within seconds (up to 30s).
- **Targeting rules** — serve different values by user attributes (`plan`, `country`, `userId`...).
- **Percentage rollouts** — gradual release to a % of users, with sticky (consistent-hash) bucketing.
- **Multi-variant config** — flag values can be boolean, string, number, or JSON (ship a whole config block).
- **Not** for: static config that never changes (→ `wrangler.jsonc` vars/secrets); per-request rate
  limiting (→ Rate Limiting rules); environment switching (often → Wrangler environments).

## Binding & config (`wrangler.jsonc`)
```jsonc
{
  "flagship": [
    { "binding": "FLAGS", "app_id": "<APP_ID>" }
    // multiple apps: add more objects, e.g. { "binding": "EXPERIMENT_FLAGS", "app_id": "<APP_ID_2>" }
  ]
}
```
- `app_id` comes from the Flagship **app** (top-level org unit; create one in the dashboard first).
- Run `npx wrangler types` → `Env` interface types each binding as `Flagship`.
- Local (`wrangler dev` ≥4.135.0, Vite plugin ≥1.56.0, Vitest, `cf dev`): flags evaluate against an **empty local store** (code defaults
  until you add flags). Seed with `npx wrangler flagship flags pull <APP_ID>`; `--local` on `flagship flags` commands edits it; `Local Explorer`
  needs Wrangler ≥4.148.0. Binding `"remote": true` evaluates the live app instead (`flagship/configuration/#local-development`).

## Ways to evaluate
1. **Workers binding** (`env.FLAGS`) — recommended inside Workers; no HTTP, auto auth via binding.
   ```ts
   const enabled = await env.FLAGS.getBooleanValue("new-feature", false, { userId: "user-42" });
   ```
   Typed methods: `getBooleanValue` / `getStringValue` / `getNumberValue` / `getObjectValue<T>` (+ untyped
   `get`). Each takes `(flagKey, defaultValue, context?)` and returns `defaultValue` on known failures.
   `*Details` variants (`getBooleanDetails`...) add `.value`, `.variant`, `.reason`, `.errorCode`.
2. **OpenFeature SDK** (`@cloudflare/flagship`) — for Node.js, browser, or OpenFeature vendor-neutrality.
   TypeScript: `@cloudflare/flagship` + `@openfeature/server-sdk` (server) or `@openfeature/web-sdk` (browser).
   Python: `cloudflare-flagship` (server, HTTP). Go: `github.com/cloudflare/flagship/sdks/go` (server, HTTP).
   Rust: `cargo add cloudflare-flagship` (Rust ≥1.88, Tokio; HTTP or `.local_evaluation(true)` with a Read token; no Workers binding — `flagship/sdk/rust/`).
   Inside a Worker you can pass the binding into the SDK
   (`new FlagshipServerProvider({ binding: env.FLAGS })`) to keep OpenFeature API + binding speed.
3. **Evaluation API** (when you can't use the binding): The `GET` endpoint
   takes **scalar** context as query params (numbers/booleans coerced; JSON-looking values stay strings). `POST` to
   `/accounts/$ACCOUNT_ID/flagship/apps/$APP_ID/evaluate` with body `{ "flagKey", "context": { "targetingKey", "profile": {...}, "tags": [...] } }` carries structured
   context; both return `flagKey`, `value`, `variant`, `reason`. Invalid context → `400`.
4. **REST API / dashboard / `wrangler flagship`** — manage flags (CRUD), organize into apps. Management
   endpoints use Cloudflare v4 envelopes (`result`, `result_info`, `errors`) + snake_case; the `/evaluate`
   endpoint is the exception (OpenFeature-style camelCase, not enveloped). Wrangler ships a
   `wrangler flagship` command family (apps, flags, rules, rollouts, evaluate, changelog);
   `wrangler flagship flags update` does the read-modify-write for you.

## Targeting & rollouts
- **Rules** are priority-ordered (lower priority number first); **first match wins**, else default variant.
- 13 comparison operators (`equals`, `in`, `has`, `not_has`, `starts_with`…), logical AND/OR grouping (nesting up to 5 levels).
- **Structured context** (2026-10-23): evaluation context may hold nested objects, arrays and `null`. Target nested
  attributes with dot paths (`profile.plan`, max 5 segments; a literal top-level key wins over path traversal) and
  arrays with `has` / `not_has` (`tags has "beta"`). Rollouts can bucket on a nested id such as `profile.id`.
  Missing attributes never match (even negative operators); `null` only matches `not_equals` / `not_in`.
  Works via the binding, the evaluation API `POST`, and the TS/Python/Go OpenFeature SDKs from `0.6.0`.
- **Rollouts**: any rule can add `rollout: { percentage, attribute }`. Consistent hashing on the attribute
  (default `targetingKey`) gives sticky bucketing — same user → same value. `reason` is `SPLIT` when a
  rollout serves the variant. For A/B/n via API, use **cumulative** thresholds (30/40/30 → 30, 70, 100).

## Gotchas
- **Missing `targetingKey`/bucketing attr → random bucketing per request.** Always pass a stable id, or
  rollouts/experiments won't stick across requests.
- **Flag always returns default?** Check: flag enabled, rules actually match, and you passed the
  attributes the rules reference in `context`.
- **Invalid context:** binding `*Details` return the default with `reason` `ERROR`, `errorCode` `INVALID_CONTEXT`.
- **Type mismatch** (e.g. `getBooleanValue` on a string flag) → returns default; `*Details.errorCode` =
  `"TYPE_MISMATCH"`. All variants on one flag must share a single type.
- **REST PUT replaces the whole flag** — read-modify-write the full definition; partial PUT drops rules/variants.
- **Browser client provider is not recommended for public-facing apps** — `FlagshipClientProvider`
  requires a Cloudflare API token that would be exposed in client-side code; Cloudflare says a safer
  client-side solution is still in progress and to use the Worker binding or the TS server SDK meanwhile.
  Its `prefetchFlags` array is required: a key not listed returns `FLAG_NOT_FOUND` at resolution time.
- All variants share one type; propagation is eventual — **up to 30 seconds** globally, during which some
  evaluations still return the previous value.

## Limits & pricing
> ⚠️ Verify on the live pricing/limits pages (`developers.cloudflare.com/flagship/`) before quoting —
> Flagship is a newer product and public pricing was not published in these docs. Confirm cost before relying on it.

**Platform limits** (soft where noted): apps/account **10,000** (soft) · flags/app **5,000** (soft) ·
flag/app/variant keys **64 chars** · condition attribute names **64** · condition string values **256** ·
variant value size **10 KB** · condition nesting depth **5 levels** · flag description **512 chars** ·
flag config size per app **25 MB**. Keys allow letters/numbers/hyphens/underscores.
**Evaluation context limits:** ≤100 top-level attributes · key length 1–256 chars · nesting depth 10 · 32 KiB serialized JSON.
**API tokens:** account-wide or app-scoped (specified apps only), each with Read / Write / Evaluate permissions.

## Going deeper
- Covered by the official `cloudflare` skill (`references/flagship/`) — use it for full REST API
  schemas, OpenFeature SDK setup (server/client/Python), targeting patterns, and troubleshooting:
  `api.md`, `configuration.md`, `patterns.md`, `gotchas.md`.
- Live docs: `developers.cloudflare.com/flagship/` · OpenFeature standard: `openfeature.dev` ·
  SDK source: `github.com/cloudflare/flagship`.
