# API reference — artifacts

> Exact REST endpoints for **artifacts**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 19 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

> Note: this slice is **read-heavy and incomplete on purpose — the spec is**. Artifacts is closed
> beta and its write surface is only partly published: there is `GET` on `/artifacts/namespaces` but
> **no `POST`**, so the documented namespace-creation call that sets `jurisdiction` (see
> `products/artifacts.md`) does not appear here. Checked against both the 2026-08-08 spec and one
> downloaded fresh on 2026-08-15 — absent from both, so it is a publishing gap, not a stale copy.
> The Git/repo data plane (`artifacts.cloudflare.net`) is a different API and is never in this spec.
> **Missing here ≠ does not exist** — trust `products/artifacts.md` and the live docs over silence.

- `GET /accounts/{account_id}/artifacts/namespaces` — List namespaces  · required: 
- `POST /accounts/{account_id}/artifacts/namespaces` — Create a namespace  · required:   · body: namespace:string
- `GET /accounts/{account_id}/artifacts/namespaces/{namespace}` — Get a namespace  · required: namespace
- `DELETE /accounts/{account_id}/artifacts/namespaces/{namespace}` — Delete a namespace  · required: namespace
- `GET /accounts/{account_id}/artifacts/namespaces/{namespace}/repos` — List repositories  · required: namespace
- `POST /accounts/{account_id}/artifacts/namespaces/{namespace}/repos` — Create a repository  · required: namespace  · body: name:string
- `GET /accounts/{account_id}/artifacts/namespaces/{namespace}/repos/{name}` — Get a repository  · required: namespace, name
- `DELETE /accounts/{account_id}/artifacts/namespaces/{namespace}/repos/{name}` — Delete a repository  · required: namespace, name
- `GET /accounts/{account_id}/artifacts/namespaces/{namespace}/repos/{name}/blob/{hash}` — Read a Git blob  · required: namespace, name, hash
- `GET /accounts/{account_id}/artifacts/namespaces/{namespace}/repos/{name}/commit/{hash}` — Read a Git commit  · required: namespace, name, hash
- `GET /accounts/{account_id}/artifacts/namespaces/{namespace}/repos/{name}/file` — Read a file  · required: namespace, name, ref, path
- `POST /accounts/{account_id}/artifacts/namespaces/{namespace}/repos/{name}/fork` — Fork a repository  · required: namespace, name  · body: name:string
- `POST /accounts/{account_id}/artifacts/namespaces/{namespace}/repos/{name}/import` — Import a repository  · required: namespace, name  · body: url:string
- `GET /accounts/{account_id}/artifacts/namespaces/{namespace}/repos/{name}/log` — Read commit history  · required: namespace, name
- `GET /accounts/{account_id}/artifacts/namespaces/{namespace}/repos/{name}/raw/{ref}/{path}` — Read a raw file with content type  · required: namespace, name, ref, path
- `GET /accounts/{account_id}/artifacts/namespaces/{namespace}/repos/{name}/tokens` — List repository tokens  · required: namespace, name
- `GET /accounts/{account_id}/artifacts/namespaces/{namespace}/repos/{name}/tree/{hash}` — Read a Git tree  · required: namespace, name, hash
- `POST /accounts/{account_id}/artifacts/namespaces/{namespace}/tokens` — Create a repository token  · required: namespace  · body: repo:string
- `DELETE /accounts/{account_id}/artifacts/namespaces/{namespace}/tokens/{id}` — Revoke a token  · required: namespace, id
