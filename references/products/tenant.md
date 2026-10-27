# Tenant — provision & manage accounts at scale (Tenant API)

> A provisioning layer for **Channel and Alliance partners** (resellers, MSPs, agencies) to create and
> manage many Cloudflare customer accounts, users, zones, and subscriptions programmatically — built into
> the standard Client v4 API. **Not a self-serve product**: requires a signed partner agreement.

## Contents
- When to use (and when not)
- Structure & access
- Provisioning flow (API)
- Account management & subscriptions
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- You are a **reseller / MSP / agency** provisioning Cloudflare for many sub-customers programmatically.
- Multi-account provisioning at scale: spin up isolated accounts, invite users, create zones, attach plans.
- You want each customer's data/settings **isolated** but centrally administered under one Tenant.
- Reselling Cloudflare plans/add-ons (Pro/Biz/Ent zones, Zero Trust, Stream, Workers, etc.) per agreement.
- **Not** for: a single team managing their own account (just use the normal dashboard/API). Not a binding,
  Worker resource, or SDK — it's a set of v4 REST endpoints gated by partner entitlements.

## Structure & access
- A **Tenant** is a special account that contains other accounts + resources. You don't create it — Cloudflare
  provisions it when you sign a partner agreement and adds your user as a **Tenant admin**.
- Tenant admins are the default **Super administrator** for every account/zone in the Tenant. Their user
  API key provisions accounts per the catalog in your agreement.
- A Tenant can have multiple **units** (`unit_tag`); accounts are created on a unit.
- **Hierarchy:** Tenant → units → Accounts → Users + Resources (zones, Workers, Zero Trust apps).
- **Auth:** Global API Key via `X-Auth-Email` + `X-Auth-Key`. Some endpoints (subscriptions) accept a
  bearer API token (`Authorization: Bearer …`). There is no `wrangler.jsonc` binding — this is REST only.
- Not enabled by default: if not yet active, MSP → `partners@cloudflare.com`, Agency → `agency@cloudflare.com`.

## Provisioning flow (API)
All under `https://api.cloudflare.com/client/v4`.
1. **Get tenant details** — `GET /user/tenants` → returns units, memberships, entitlements. Grab `unit_tag`.
2. **Create account** — `POST /accounts` with `name`, `type` (`standard` default | `enterprise`), optional
   `unit.id`. Your user owns it for its whole lifecycle. Optional KYC fields (`business_name`,
   `business_address`, `business_email`, `business_phone`, `external_metadata` — each ≤120 chars).
3. **Grant user access** — either (a) invite the customer: `POST /accounts/{account_id}/members` with
   `email` + `roles` (Administrator role id is `05784afa30c1afe1440e79d9351c7430`), or (b) build your own
   interface: create a **service user** via `POST /users` and call the API on the customer's behalf.
4. **Create zone** — `POST /zones` with `name` + `account.id` (the customer account from step 2).
5. **Zone plan subscription** — `POST /zones/{zone_id}/subscription` with `rate_plan.id` (e.g. upgrade
   `PARTNERS_FREE` → `PARTNERS_BIZ`), optional `component_values`, `frequency` (`monthly`/`annual`).
6. **Account subscriptions** — `POST /accounts/{account_id}/subscriptions` for add-ons (Zero Trust, Stream…).

```bash
# create a customer account on a specific unit
curl https://api.cloudflare.com/client/v4/accounts \
  -H "X-Auth-Email: <EMAIL>" -H "X-Auth-Key: <API_KEY>" -H "Content-Type: application/json" \
  --data '{"name":"<ACCOUNT_NAME>","type":"standard","unit":{"id":"1a2b3c4d5e6f7g8h"}}'
```

## Account management & subscriptions
- **List Tenant accounts** — `GET /tenants/{tenant_id}/accounts?page=1&per_page=10` (paginated; `order` +
  `direction` 0=asc/1=desc). Returns accounts + feature flags. `GET /accounts` lists all you can access.
- **Update / delete account** — `PUT /accounts/{account_id}` · `DELETE /accounts/{account_id}`. **Delete is
  permanent and removes all zones/resources** under the account (except Logpush jobs and Zero Trust
  Gateway config — see Gotchas). Account subs also support `DELETE /accounts/{id}/subscriptions/{sub_id}`.
- **Subscriptions** — create/get/update on zones (`/zones/{id}/subscription`) and accounts
  (`/accounts/{id}/subscriptions/{sub_id}`). Plan values vary by program (sample, not exhaustive):
  - Zone plans: resellers `PARTNERS_FREE|PARTNERS_PRO|PARTNERS_BIZ|PARTNERS_ENT`; agency
    `CF_FREE|CF_PRO_20_20|CF_BIZ`; MSP `msp_biz`.
  - Add-ons: Zero Trust (`TEAMS_*`, `PARTNERS_ACCESS_*`), Stream, Workers, Images, Load Balancing, etc.
  - **Authoritative list:** call the zone/account rate-plans endpoints — what you see depends on your agreement.

## Gotchas
- **Partner-gated.** Endpoints fail without entitlements. Error `1225` = "account does not have access to
  this product. Contact billing@cloudflare.com for assistance." → your reseller plan lacks that
  subscription; to change program or add one, contact `partners@`/`agency@cloudflare.com`.
- **Specify `unit.id`** when your user administers multiple tenants/units, or account creation is ambiguous.
- **Per-customer users to avoid rate limits.** For interface-style integrations, route customer A's changes
  through user A, customer B's through user B — sharing one user invites API [rate limiting](https://developers.cloudflare.com/fundamentals/api/reference/limits/).
- **Service users** (interface option) aren't enabled by default — contact Support to expose their API key.
- **Account delete is irreversible** and cascades to all zones/resources. No undo. But it does **not**
  clean up everything: **Logpush jobs** keep delivering logs and **Zero Trust Gateway configs** may keep
  resolving DNS after deletion — delete them first (`DELETE /accounts/{id}/gateway`, then
  `DELETE /accounts/{id}/access/organizations`, then the account).
- KYC fields are optional unless the Tenant **enforces** them; all are 120-char text fields.

## Pricing & limits
> ⚠️ The Tenant API itself has **no separate price** — it's a provisioning mechanism. Your costs are the
> **wholesale/reseller rates** in your signed partner agreement, and what you charge customers is up to you.
> There is **no public pricing page**; terms are set per partner program. Verify with your Cloudflare
> partner contact before quoting anything.

- **Access:** requires a signed Channel/Alliance partner agreement (Agency Partner Program, or Enterprise
  Resellers & MSP Program). Not available self-serve.
- **Cost drivers:** the per-account/per-zone plan + add-on subscriptions you provision (billed to you at
  reseller rates), not the API calls. Standard Cloudflare [API rate limits](https://developers.cloudflare.com/fundamentals/api/reference/limits/) apply.
- **Subscription catalog** is bounded by your program — request additions via `partners@cloudflare.com`.

## Going deeper
- No official `cloudflare` skill ref for `tenant` — this file is the primary reference.
- Exact request/response schemas: Cloudflare API docs under `accounts`, `zones`, and their `subscriptions` /
  `rate_plans` subresources (`developers.cloudflare.com/api/`).
- Concepts & full guide: `developers.cloudflare.com/tenant/` (structure, get-started, how-to, subscriptions).
- Roles & members (Super admin, Administrator): `developers.cloudflare.com/fundamentals/manage-members/`.
