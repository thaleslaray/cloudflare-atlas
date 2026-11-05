# API reference — web-search

> Exact REST endpoints for **web-search**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 1 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

> Note: Web Search API (`/ai/websearch`, GA 2026-10-02) is its own product with its own file
> (`products/web-search.md`). Seeded 2026-10-31 so the endpoint stops surfacing as an in-scope gap
> under the `ai` root that `workers-ai` touches but does not own.

- `POST /accounts/{account_id}/ai/websearch` — Search the web through AI Gateway  · required: account_id  · body: options:object, query:string
