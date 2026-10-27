# Terraform provider — Cloudflare as Infrastructure as Code

> Manage Cloudflare resources (zones, DNS, Workers, WAF, Zero Trust…) declaratively with HashiCorp
> Terraform. Define config in `.tf` files, version it in git, `plan`/`apply` to reconcile.

## Contents
- When to use (and when not)
- Setup & authentication
- Core workflow
- Importing existing config (cf-terraforming)
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- **Declarative IaC** for Cloudflare config you want versioned, reviewed, and reproducible across
  environments (dev/staging/prod) — zones, DNS, WAF/rulesets, Load Balancers, Zero Trust, Workers, KV, R2, D1, Pages.
- You already run Terraform for the rest of your stack (AWS/GCP) and want one tool/workflow.
- **vs Wrangler:** Wrangler is the right tool for *building & deploying Workers* (code, bindings,
  dev loop). Terraform is for *managing infrastructure declaratively*. Don't manage the same Worker
  with both — pick one owner per resource (see 409-conflict gotcha).
- **vs Pulumi:** Pulumi is code-based IaC (TS/Python/Go) over the same Cloudflare API — choose it if
  you prefer real programming languages over HCL. Both are valid; Terraform/HCL is more common.
- **Not** for: the Workers build/deploy dev loop (→ wrangler) · one-off dashboard tweaks.

## Setup & authentication
Pin the **v5** provider (current; auto-generated from the OpenAPI spec — breaking changes from v4):
```hcl
terraform {
  required_version = ">= 1.0"
  required_providers {
    cloudflare = { source = "cloudflare/cloudflare", version = "~> 5" }
  }
}
provider "cloudflare" {
  api_token = var.cloudflare_api_token  # or the CLOUDFLARE_API_TOKEN env var
}
```
Auth (priority order): **API Token** (recommended — scope to specific accounts/zones) → Global API
Key (`api_key` + `email`, legacy) → `api_user_service_key` (Origin CA certs). Never hardcode tokens;
use variables + env vars, and a secrets store (e.g. Vault) in CI.

## Core workflow
```bash
terraform init        # download provider, set up backend
terraform plan        # preview diff
terraform apply       # reconcile remote → matches config
terraform destroy     # tear down
terraform fmt -recursive && terraform validate
```
- **Remote state** for any team setup (Terraform Cloud, S3, etc.) — never share local `terraform.tfstate`.
- Cloudflare's best-practice docs recommend isolating state by **account / zone / product** (scoped
  owners, scoped blast radius) and **avoiding modules** (or using sparingly) — shared modules drift
  and complicate debugging. (Note: the official skill ref leans pro-module; the live docs are cautious.)

## Importing existing config (cf-terraforming)
Terraform only manages resources it created or was told about. To adopt resources made via dashboard/API:
1. Generate HCL: `cf-terraforming generate --resource-type cloudflare_dns_record -z <zone-id> > out.tf`
2. Import into state (emits `terraform import …` commands you then run): `cf-terraforming import --resource-type cloudflare_dns_record -z <zone-id>`
3. `terraform plan` should then report **No changes**.

Install: `brew install cloudflare/cloudflare/cf-terraforming`. Auth via `--email`/`--token` (or
`CLOUDFLARE_EMAIL`/`CLOUDFLARE_API_TOKEN` env vars), scope with `-a` (account) / `-z` (zone).

## Gotchas
- **v5 breaking changes** (renames): `cloudflare_record` → `cloudflare_dns_record`;
  `cloudflare_worker_script` → `cloudflare_workers_script`; `cloudflare_access_*` →
  `cloudflare_zero_trust_*`. Migrate HCL with `tf-migrate migrate --source-version v4 --target-version v5`;
  migrate state with `moved` blocks (Terraform 1.8+) or `terraform import` — **not** `terraform state mv`.
  (Note: `workers_*` plural isn't a universal rule — v5.24 also ships new singular `cloudflare_worker`
  and `cloudflare_worker_version` resources.)
- **State drift** — add `lifecycle { ignore_changes = [...] }` for: `cloudflare_pages_project`
  (`deployment_configs`), `cloudflare_workers_script` (secrets return REDACTED),
  `cloudflare_load_balancer` (`adaptive_routing`, `random_steering`).
- **R2 `location` is lowercase in v5**: `apac`, `eeur`, `enam`, `weur`, `wnam`, `oc` (uppercase was v4).
  Only honored the first time a bucket of that name is created, and it's best-effort.
- **D1**: Terraform creates the database only, **not the schema** — run `wrangler d1 migrations apply` after.
- **KV special chars** in keys were URL-encoded incorrectly before provider 5.16.0 — upgrade.
- **409 on Worker deploy**: deploying the same Worker via both Terraform and wrangler — pick one.
- **"DNS record already exists"** / "couldn't find resource": import it or `terraform state rm`.
- **State lock stuck** (crashed run): `terraform force-unlock <lock-id>` (with caution).

## Pricing & limits
- **The provider/tooling is free** (open source). You pay only for the underlying Cloudflare
  resources you provision (Workers, R2, D1, etc.) per their own pricing — Terraform adds no cost.
> ⚠️ Underlying-product pricing changes — verify on the live pricing page before quoting.

**Limits to mind:** Worker size **64 MiB uncompressed**, Free and Paid (no gzip limit) · D1 **50,000 dbs/account** (10 on
Free) · Pages **100 projects/account** (flat, not routinely raised) · DNS records/zone: **200** Free (zones
created ≥ 2024-09-01), 1,000 older Free, **3,500** Pro/Business · API-token rate
limits vary by plan (`TF_LOG=DEBUG` to debug — the v4 `api_client_logging` provider arg no longer exists in v5).
Verify against each product's limits page.

## Going deeper
- Official `cloudflare` skill `references/terraform/` is the primary deep reference — use it over
  duplicating here: `configuration.md` (resource HCL for zones/DNS/Workers/KV/R2/D1/Pages/rulesets),
  `api.md` (data sources for existing resources), `patterns.md` (multi-env, CI/CD), `gotchas.md`.
- Provider docs & full resource catalog: `registry.terraform.io/providers/cloudflare/cloudflare/latest/docs`.
- cf-terraforming supported resources: `github.com/cloudflare/cf-terraforming#supported-resources`.
- Alternative IaC: official skill `references/pulumi/` · Worker dev loop → `references/wrangler/`.
