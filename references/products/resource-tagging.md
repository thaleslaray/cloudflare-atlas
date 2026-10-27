# Resource Tagging — key-value metadata for Cloudflare resources

> Attach custom key-value tags to a wide range of Cloudflare resources (zones, Workers, D1,
> R2, KV, Tunnels, DNS records, and more) for **organization, RBAC, and billing attribution**.
> Tags live separately from the resource — no config changes — and support cross-resource queries.

## Contents
- When to use (and when not)
- How it works
- Key API / access patterns
- Tag filtering
- Supported resource types
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- **Org/inventory:** label resources by `environment`, `team`, `region`, `cost-center`, `owner`.
- **RBAC / governance:** drive policy enforcement and access decisions off tags without touching
  the underlying resource config (e.g. quarantine anything tagged `sensitivity=high`).
- **Cost / billing attribution:** group spend by team or cost center across products.
- **Cross-resource queries:** "list every resource tagged `environment=production`" in one call.
- **Not** for: runtime app data (→ kv/d1), per-request routing logic, or anything needing a
  `PATCH`/single-tag mutation (the API has none — see Gotchas).

## How it works
- Tags are plain `string:string` key-value pairs stored as a JSON object, kept **separately**
  from the resource (no redeploy / config change to add or remove them).
- Managed entirely via the **Tagging API** (`GET`/`PUT`/`DELETE`). Dashboard UI exists
  (**Manage Account → Resource Tagging**) but is beta; API is the recommended interface.
- Auth: **Account Owned Tokens (AOTs)** recommended for automation (account-level, user-independent),
  or a user token. Caller needs **Super Admin**, **Workers Admin**, or **Tag Admin** role
  (token scope `#com.cloudflare.api.account.tag.*`).
- **No `wrangler` binding** — this is a control-plane / account-governance API, not a Worker runtime
  resource. You call `api.cloudflare.com/client/v4/.../tags` directly.

## Key API / access patterns
Account-level resources use `/accounts/{account_id}/tags*`; zone-level use `/zones/{zone_id}/tags*`.

```bash
# Set tags (PUT REPLACES ALL tags on the resource)
curl -X PUT "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/tags" \
  -H "Authorization: Bearer $API_TOKEN" -H "Content-Type: application/json" \
  -d '{"resource_type":"worker","resource_id":"'"$RID"'",
       "tags":{"environment":"production","team":"platform"}}'

# Get tags for one resource
curl "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/tags?resource_type=worker&resource_id=$RID" \
  -H "Authorization: Bearer $API_TOKEN"

# Delete ALL tags (204 No Content) — no single-tag delete
curl -X DELETE "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/tags" \
  -H "Authorization: Bearer $API_TOKEN" -H "Content-Type: application/json" \
  -d '{"resource_type":"worker","resource_id":"'"$RID"'"}'
```
- **Add/remove a single tag** → no `PATCH`. Do **GET → merge locally → PUT** the full set.
- **Discover tags:** `GET /tags/keys`, `GET /tags/values/{key}` (optional `?type=worker`),
  `GET /tags/resources` (all tagged resources).

## Tag filtering
On `GET /accounts/{id}/tags/resources` via the `tag` query param. Multiple `tag` params = **AND**.
- Key-only: `tag=environment` · Key-value: `tag=environment=production`
- OR values (comma): `tag=environment=production,staging` (max 10 values)
- Negate: `tag=!archived` (key absent) · `tag=region!=us-west-1` (value mismatch)
- Combine: `?tag=environment=production&tag=region=us-west-1,us-east-1&tag=!archived`

## Supported resource types
**25 account-level** types (account, worker, `worker_version`, d1_database, r2_bucket, kv_namespace,
queue, vectorize_index, durable_object_namespace, cloudflared_tunnel, ai_gateway, pages_project,
image, resource_share, stream_live_input, stream_video, load_balancer_monitor, load_balancer_pool,
access_application, access_group, gateway_list, gateway_rule, alerting_policy, alerting_webhook,
account_ruleset) and **11 zone-level** (zone, dns_record, custom_hostname, custom_certificate,
managed_client_certificate, healthcheck, load_balancer, worker_route, zone_ruleset,
api_gateway_operation, access_application_policy). Most need only `resource_type` + `resource_id`.
Exceptions: `worker_version` (account-level) also needs `worker_id`; `access_application_policy`
(**zone**-level) also needs `access_application_id`.

## Gotchas
- **`PUT` replaces ALL tags** — there is no partial update. Forgetting to merge wipes existing tags.
- **`DELETE` removes ALL tags** — no single-tag delete; `PUT` the remaining set instead.
- **Filter separator is `=`, not `:`** — error 1007's message says `:` but the API uses `tag=key=value`.
- **Beta: untagged resource → `500`, not `404`** on `GET .../tags` ("resource not found: …").
  List endpoints correctly return `200` + empty array. May change to `404` later.
- **Case-sensitive** keys/values: `Environment` ≠ `environment` ≠ `ENVIRONMENT`. Standardize casing.
- **Key validation (error 1014):** Unicode letters (any language)/digits/`_`/`.`/`-` only — no spaces, no special chars,
  no empty string.
- **Pagination** is cursor-based, **fixed 100/page** (not configurable); loop until `cursor` is `null`.

## Pricing & limits
> ⚠️ **Public beta** — API stable, behavior may change. **Available on all plans**; no separate
> Resource Tagging pricing line published. Verify on the live pricing/product page before quoting.

**Limits** (error code in parens; all over-limit → `400`):
- Max tags / account: **10,000** (beta soft cap — contact support to raise)
- Tag key length: **256 chars** (1011) · tag value length: **1,024 chars** (1012)
- Tag filters / query: **20** (1010) · OR values / filter: **10** (1013)
- Results / page: **100**, fixed

## Going deeper
- No dedicated `cloudflare` skill `references/` yet — this file is the primary reference.
- Full endpoint spec: `api/resource-tagging.md` in this skill. (The public API reference has no
  `api/resources/tags/` page — that URL 404s; browse from `developers.cloudflare.com/api/`.)
- Auth setup: Account Owned Tokens → `developers.cloudflare.com/fundamentals/api/get-started/account-owned-tokens/`.
- Rendered docs: `docs-oficiais/pages/resource-tagging/` (get-started, how-to, reference/error-codes).
