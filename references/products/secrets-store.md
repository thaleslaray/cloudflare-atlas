# Secrets Store — account-level encrypted secrets

> Encrypt and store sensitive values **once at the account level** and reuse them across the account
> (Workers, AI Gateway). Centralized, role-controlled, audited — versus per-Worker `wrangler secret`.

## Contents
- When to use (and when not)
- The account-level model
- Binding & config
- Access patterns
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- One secret (API key, token, private key, password) is **shared across many Workers / products** and you
  want a single source of truth — update once, every consumer gets the new value.
- You want **role-based access** (who can create/edit vs. who can bind/deploy) and **audit logs** on secret
  changes — security-team-friendly governance over secrets.
- Integrations today: **Cloudflare Workers** and **AI Gateway** (Bring Your Own Keys). More to come.
- **Not** for: a secret used by exactly one Worker with no sharing → plain per-Worker
  [Workers Variables and Secrets](https://developers.cloudflare.com/workers/configuration/secrets/)
  (`wrangler secret put`) is simpler. Not for non-secret config (→ Worker vars / env).

## The account-level model
- Secrets live in a **store** (one store per account in beta), not in a Worker. A Worker references a secret
  by `store_id` + `secret_name` via a binding.
- Each secret has **scopes** (`workers`, `ai-gateway`) that gate which product can read it. Wrong scope → not
  accessible from that integration.
- **Write-once / read-never**: after creation a secret can never be decrypted or viewed again via dashboard or
  API — only the bound service can read its value at runtime. To rotate, edit/replace the value.
- First store is auto-created when a Super Admin / Secrets Store Admin first interacts; or create explicitly:
  `wrangler secrets-store store create <name> --remote`.

## Binding & config (`wrangler.jsonc`)
```jsonc
{
  "secrets_store_secrets": [
    {
      "binding": "API_KEY",        // env var name in your Worker
      "store_id": "<STORE_ID>",    // from dashboard Secrets Store tab or `wrangler secrets-store store list`
      "secret_name": "MY_SECRET_NAME"  // exact, case-sensitive, no spaces
    }
  ]
}
```
Create a secret (must have `workers` scope to bind to a Worker):
```
npx wrangler secrets-store secret create <STORE_ID> --name MY_SECRET_NAME --scopes workers --remote
```

## Access patterns
- In the Worker, the binding is on `env` and the value is fetched **asynchronously**:
  ```js
  const apiKey = await env.API_KEY.get();   // async only
  ```
- Manage via **Wrangler** (`secrets-store store` / `secrets-store secret` subcommands), **Dashboard**
  (Secrets Store tab, or inline from a Worker's Bindings panel), or the **Secrets Store API**
  (`/accounts/{id}/secrets_store/...`).
- **Local dev**: production (`--remote`) secrets are *not* readable locally. Create separate local-only
  secrets with the same Wrangler commands **without** `--remote`.

## Gotchas
- **`.get()` throws on failure** (missing secret, wrong scope, wrong `store_id`) — it does **not** return
  null. Wrap in try/catch and return a clean error, don't leak details.
- **Scope mismatch** is the most common "secret not found": secret exists but only has `ai-gateway` scope, not
  `workers`. Add the scope (`secret update ... --scopes workers --remote`).
- **Don't access secrets at module top-level** — `env` isn't available then. Read inside the request handler.
- **Never log the secret value** — log only metadata ("retrieved API_KEY").
- Name is **case-sensitive and cannot contain spaces**; mismatch → not found.
- **Roles matter**: creating/editing secrets needs Super Admin or Secrets Store Admin; *binding* a secret to a
  Worker needs Super Admin or Secrets Store **Deployer**. Reporter is read-only metadata.
- **API tokens: binding counts as a write.** Deploying a Worker with a Secrets Store binding (e.g. Wrangler in
  CI/CD) needs **Account Secrets Store Edit**; a Read-only token fails with
  `failed to fetch secrets store binding due to authorization error - check deploy permissions and secret scopes`.
- **Audit logs**: create/update/delete are logged; a *duplicate* shows up as a `create` with
  `duplicated_from_id`.

## Pricing & limits
- **Open beta** — no public pricing page; effectively free during beta. **Verify on the live pricing page
  before quoting** (and watch for GA pricing).
- Limits (beta): **100 secrets per account**, **1 store per account**, **65,536 bytes** max per secret (must be a
  string). Local-only secrets do **not** count toward the 100. Check usage:
  `GET /accounts/{account_id}/secrets_store/quota` (returns `secrets.quota` / `secrets.usage`).
- **Not available in the Cloudflare China Network** (operated by JD Cloud).

## Going deeper
For the full API surface (CRUD endpoints, quota, list/duplicate), TypeScript binding types, and detailed
patterns, see the official `cloudflare` skill `references/secrets-store/` (`api.md`, `configuration.md`,
`patterns.md`, `gotchas.md`). Docs: `developers.cloudflare.com/secrets-store/`.
