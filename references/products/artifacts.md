# Artifacts — versioned file trees that speak Git

> Store, version, and share filesystem artifacts (repos, build outputs, ML checkpoints) behind a
> **Git-compatible** interface, addressable from Workers, a REST API, and standard Git clients.
> ⚠️ **Open beta since 2026-10-01** (was closed beta; no access request needed) — Workers **Paid** plan
> only; **billing starts 2026-10-14**.

## Contents
- When to use (and when not)
- Binding & config
- Access patterns
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- **Versioned filesystem trees**: git-style repos, per-agent/per-session/per-task workspaces, build
  outputs, deployment bundles, ML checkpoints, generated assets, shared trees passed between tools.
- You want `clone`/`fetch`/`pull`/`push` over HTTPS with repo-scoped tokens.
- The same content must be reachable from **Workers binding + REST API + Git clients**.
- Sweet spot: agent/automation workflows where each unit of work gets its own isolated repo + token
  (create one repo per agent/session/task; fork from a reviewed baseline).
- **Not** for: flat objects by key (→ r2), key-value (→ kv), relational/SQL rows (→ d1). The line:
  **R2 = flat objects; Artifacts = versioned trees with git-compatible access.**

## Binding & config (`wrangler.jsonc`)
```jsonc
{
  "artifacts": [
    { "binding": "ARTIFACTS", "namespace": "default" }
  ]
}
```
Namespaces are **created implicitly** — pick a name (`default`, `prod`, `staging`, `agents-…`) and the
first repo created under it provisions it. Use them to separate environments/tenants/hot shards.

**Data localization (2026-08-13)** — a namespace can be pinned to a jurisdiction (`eu` or `us`), and
all repos inside it are stored and processed only there. It is set **only at creation, only
explicitly, and never changeable afterwards**:
```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/artifacts/namespaces" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" -H "Content-Type: application/json" \
  --data '{ "namespace": "my-eu-namespace", "jurisdiction": "eu" }'
```
⚠️ **A namespace born implicitly (first repo) is unrestricted** — if you have a data-residency
requirement, create the namespace explicitly *before* the first repo, or you will have to rebuild it.
Run `npx wrangler types`; `worker-configuration.d.ts` is the source of truth for the `Artifacts` type.

## Access patterns
- **Workers binding** (`env.ARTIFACTS`) — namespace methods: `create(name, opts?)` / `get(name)` /
  `list(opts?)` / `import(params)` / `delete(name)`. Repo handle from `get`: `createToken(scope?, ttl?)`,
  `listTokens()`, `revokeToken(tokenOrId)`, `fork(name, opts?)`, `log(opts?)`, `readCommit(hash)`,
  `readTree(hash)` (`/artifacts/api/workers-binding/` — that reference lists no `info()` or
  `validateToken()`; verify live before using them).
  ```typescript
  const created = await env.ARTIFACTS.create("starter-repo");
  // created.remote -> git remote URL,  created.token -> initial repo token
  ```
- **REST control plane** — standard Cloudflare v4 API, base
  `https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/artifacts/namespaces/$NS` (account-level
  base drops the `/namespaces/$NS` suffix), authed with a **Cloudflare API token** (Bearer) needing
  *Artifacts → Read* for read routes and *Artifacts → Edit* for write routes. Routes (under
  `/artifacts`): `POST/GET /namespaces`, `GET /namespaces/:ns`, `POST/GET /namespaces/:ns/repos`,
  `GET/DELETE /namespaces/:ns/repos/:name`, `POST /repos/:name/fork`, `POST /repos/:name/import`,
  content reads `log`/`commit/:hash`/`tree/:hash`/`blob/:hash`/`file`/`raw/:ref/:path`, tokens
  `GET /repos/:name/tokens`, `POST /namespaces/:ns/tokens`, `DELETE /namespaces/:ns/tokens/:id`.
- **Wrangler CLI** (since 2026-05-18): `wrangler artifacts namespaces list|get`,
  `wrangler artifacts repos create|list|get|delete`, `wrangler artifacts repos issue-token`.
- **Git over HTTPS** — use the returned `remote` + a repo token; prefer header auth:
  ```bash
  git -c http.extraHeader="Authorization: Bearer $ARTIFACTS_TOKEN" clone "$ARTIFACTS_REMOTE"
  ```
- **ArtifactFS** — mount-style access for large repos where startup beats a full clone.
- **Workers Builds** (2026-10-01) — *Create application → Continue with Artifacts*: production-branch pushes
  deploy the Worker, other branches create/update Worker Previews (`workers/ci-cd/builds/git-integration/artifacts-integration/`).
- **Dashboard** — view/create namespaces, view/create/fork/search repos, browse files + copy the Git
  remote, and provision repo tokens (read/write) under **Storage & databases → Artifacts**.

## Gotchas
- **Two distinct credentials.** A **Cloudflare API token** (scoped *Artifacts → Read/Edit*)
  authenticates the REST control plane (create repos, mint tokens); **repo tokens** authenticate only
  **Git operations** against the `remote`. They are not interchangeable. Keep control plane and data
  plane separate. The Workers binding passes no token at all — the binding itself is the auth.
- **Token scopes:** `read` covers clone/fetch/pull; `push` requires a `write` token. Mint the narrowest
  scope, prefer short-lived tokens for handoff, revoke when done. Never hardcode JWTs/tokens.
- **Repo names are unique within a namespace** — for many agent copies of one baseline, embed stable
  IDs (`${agent}-${session}-${repo}`) to avoid collisions; don't reuse a short shared name.
- **Don't share one repo as a queue** for many autonomous agents → hot spot for conflicts/large diffs.
  Use branches only when collaborators share one lifecycle.
- `import()` exists on **both** the binding (`env.ARTIFACTS.import({source:{url,branch?,depth?},
  target:{name,opts?}})`) and REST (`POST /repos/:name/import`). Imported/forked repos come back with
  `status` `importing`/`forking` before `ready` — `get()` throws while a repo is not ready.

## Pricing & limits
> ⚠️ Open beta — billing begins **2026-10-14**; pricing volatile. Verify on the live page (`developers.cloudflare.com/artifacts/platform/pricing/`) before quoting.

**Billing (Workers Paid only; Free tier = Unavailable), as of 2026-06:**
- **Operations** (create/push/pull/clone…): first **10,000/mo** included, then **$0.15 / 1,000 ops**.
- **Storage**: first **1 GB-mo** included, then **$0.50 / GB-mo** (GB-mo = avg peak storage/day over 30
  days; same metric as Durable Objects SQLite storage). Replicas add no charge; repos persist until deleted.

**Key limits:** storage/repo **10 GB** · storage/account **1 TB** (raisable) · repos **unlimited** ·
namespaces **unlimited** · control-plane rate **2,000 req / 10 s per namespace** · Git rate **2,000 req /
10 s per artifact** · names start with a letter/digit, then letters/digits/`.`/`_`/`-`.

## Going deeper
- Covered by the official `cloudflare` skill (`references/artifacts/`) — use it for the full
  Workers binding surface, REST routes, token ops, and Git protocol details.
- Live docs (authoritative during beta): `developers.cloudflare.com/artifacts/` · Git protocol &
  ArtifactFS under `/artifacts/api/`.
- Account-scoped REST endpoints → `references/api/artifacts.md` (17 ops, read-heavy: the spec omits
  the namespace `POST`, so the jurisdiction call above is doc-sourced only — see the note there).
