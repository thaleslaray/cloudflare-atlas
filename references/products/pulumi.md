# Pulumi — Cloudflare resources as IaC in real programming languages

> Provision and manage Cloudflare (Workers, DNS, KV, R2, D1, Queues, Pages, zones…) using the
> **Pulumi Cloudflare provider** — infrastructure as code written in TypeScript, JavaScript,
> Python, Go, .NET, Java, or YAML, with loops, functions, classes, and package management.

## Contents
- When to use (and when not)
- Setup & config
- Key resources / patterns
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- You want IaC for Cloudflare but prefer a **real language** (TS/Python/Go/.NET/Java) over HCL —
  loops, conditionals, functions, your own abstractions (component resources), unit tests.
- Multi-environment / multi-account fleets managed as code with state, drift detection, previews.
- **vs Terraform:** same job, different authoring. Terraform = declarative HCL (→ `terraform`).
  Pulumi = your programming language + a state backend (Pulumi Cloud or self-managed). Pick by team
  preference; both wrap the same Cloudflare API.
- **vs Wrangler:** Wrangler is the Workers-native CLI/dev loop (`wrangler dev/deploy`, bundling,
  bindings, `wrangler.jsonc`). Use Wrangler to **build and ship a Worker**; use Pulumi to provision
  the surrounding infra (zones, DNS, KV/R2/D1, routes) declaratively. They coexist — Pulumi does
  **not** bundle Worker code (see gotchas).
- **Not** for: app runtime logic, local Worker dev loop (→ wrangler), one-off clicks (dashboard).

## Setup & config
Provider package per language: `@pulumi/cloudflare` (TS/JS) · `pulumi-cloudflare` (Python) ·
`github.com/pulumi/pulumi-cloudflare/sdk/v…/go/cloudflare` (Go) · `Pulumi.Cloudflare` (.NET) ·
`com.pulumi:cloudflare` (Java). Provider is at **v6.x** (latest release v6.20.0); Cloudflare's own
tutorials still show v5-era code (`module: true`, `cloudflare.Record`).

```bash
brew install pulumi/tap/pulumi      # mac (or: curl -fsSL https://get.pulumi.com | sh)
pulumi login                        # Pulumi Cloud (state backend) — or self-managed backend
pulumi new typescript --name my-cf  # scaffold; then: npm install @pulumi/cloudflare
pulumi up                           # preview + apply;  pulumi destroy to tear down
```

**Auth — use an API token (not legacy key):** set `CLOUDFLARE_API_TOKEN` env, or
`pulumi config set --secret cloudflare:apiToken <token>`. Store `accountId` in stack config:
```yaml
# Pulumi.<stack>.yaml
config:
  cloudflare:accountId: "abc123..."
```
Secrets: `pulumi config set --secret …`, or Pulumi **ESC** environments for shared config/secrets.

## Key resources / patterns
- Resource names mirror Cloudflare: `WorkersScript`, `WorkersRoute`, `WorkersKvNamespace`,
  `R2Bucket`, `D1Database`, `Queue`, `PagesProject`, `DnsRecord`, `Zone`, `WorkersCustomDomain`.
  Deprecated aliases still in old samples: `Record` → `DnsRecord`, `WorkerDomain` →
  `WorkersCustomDomain`, `WorkerScript` → `WorkersScript`.
- **Bindings** in v6 are ONE list on `WorkersScript` — `bindings: [{ name, type, ... }]` (types per
  the multipart-upload-metadata docs), not per-kind `kvNamespaceBindings`/`d1DatabaseBindings` args
  (those are v5). Binding `name` must match the name your Worker reads from `env.*` —
  **case-sensitive**. `keepBindings` lists binding types to carry over from the previous upload.
- v6 script contents: `content` (inline) **or** `contentFile` + `contentSha256` (mutually
  exclusive); `mainModule` names the file exporting the `fetch` handler for ES-module Workers (v5's
  `module: true` is gone). Set `compatibilityDate` to lock behavior.
- Lookups & outputs: `cloudflare.getZone({...})` to resolve a `zoneId`; `pulumi.export`/`ctx.Export`
  to surface URLs. Use `dependsOn` to order side-effects (e.g. D1 migrations before the Worker).

## Gotchas
- **Pulumi does NOT bundle Worker code** — it uploads exactly what you give `content`. Build first
  (run `npm run build` / a `@pulumi/command` step), then point `content` at the built `dist/*.js`.
- **`wrangler.jsonc`/`.toml` is ignored** by Pulumi — config (bindings, compat flags) must be
  duplicated in the Pulumi program or generated from it. Keep them in sync or you get drift.
- **Stale redeploys with `contentFile`:** the update trigger is `contentSha256`, not the file's
  mtime — the registry states it is "Used to trigger updates when source code changes. Must be
  provided when `contentFile` is specified." Compute the hash of the built bundle each run, or
  Pulumi reports "no changes".
- **D1 migrations don't run** on create — Pulumi makes the DB but not the schema; run migrations via
  a `command.local.Command` with `dependsOn: [db]`.
- **v6.x Worker versioning:** `WorkersScript` auto-versions (simple path). The advanced path uses
  three resources — `Worker` + `WorkerVersion` + `WorkersDeployment` — for gradual rollouts.
- Token perms: missing scopes → `authentication error (10000)`. Grant e.g. Workers Scripts:Edit,
  Workers Route:Edit, DNS:Edit, Account Settings:Read as the resources require.
- **Always manage Pulumi-controlled resources via Pulumi** — editing them in the dashboard causes
  state conflicts on the next `pulumi up`.

## Pricing & limits
> ⚠️ Pulumi is third-party; pricing is set by Pulumi, not Cloudflare. Verify on the live page
> (`pulumi.com/pricing`) and on `developers.cloudflare.com` for per-product limits before quoting.

- **Pulumi itself** is open source (Apache 2.0) and free to run; you can self-manage state with no
  Pulumi Cloud account. **Pulumi Cloud** (hosted state, secrets, ESC) has an always-free individual
  tier plus paid team/enterprise plans — cost driver is roughly resources under management / users.
- **Cloudflare cost** is whatever the provisioned resources cost (Workers, R2, D1, KV…) — Pulumi
  adds no Cloudflare charge. Per-product free tiers and limits live in each product's reference.
- Cloudflare API is rate-limited (~1200 req / 5 min on free) — large stacks may hit it; Worker
  script size **64 MiB uncompressed** (no compressed limit). See per-product limits pages for exact numbers.

## Going deeper
- **Official `cloudflare` skill `references/pulumi/`** — use it for full API/config/patterns:
  `configuration.md` (provider + bindings), `api.md` (outputs, dependencies, imports, dynamic
  providers), `patterns.md` (multi-env, secrets, CI/CD, component resources), `gotchas.md`.
- Cloudflare docs: tutorials under `developers.cloudflare.com/pulumi/` — Hello World (deploy a
  Worker + Route + DNS), Add a site, **Manage secrets with Pulumi ESC**, and **Pulumi + Wrangler**
  (dynamic provider) for splitting infra-vs-Worker responsibilities.
- Provider registry & full resource list: `pulumi.com/registry/packages/cloudflare/`.
- Cross-refs: `terraform` (HCL alternative) · `wrangler` (Workers build/deploy) · `workers`.
