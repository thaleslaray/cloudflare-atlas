# API reference — secrets-store

> Exact REST endpoints for **secrets-store**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 12 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /accounts/{account_id}/secrets_store/quota` — View secret usage  · required: 
- `GET /accounts/{account_id}/secrets_store/stores` — List account stores  · required: 
- `POST /accounts/{account_id}/secrets_store/stores` — Create a store  · required:   · body: name:string
- `GET /accounts/{account_id}/secrets_store/stores/{store_id}` — Get a store by ID  · required: 
- `DELETE /accounts/{account_id}/secrets_store/stores/{store_id}` — Delete a store  · required: 
- `GET /accounts/{account_id}/secrets_store/stores/{store_id}/secrets` — List store secrets  · required: 
- `POST /accounts/{account_id}/secrets_store/stores/{store_id}/secrets` — Create a secret  · required:   · body: (no required fields)
- `DELETE /accounts/{account_id}/secrets_store/stores/{store_id}/secrets` — Delete secrets  · required:   · body: ids:string[]
- `GET /accounts/{account_id}/secrets_store/stores/{store_id}/secrets/{secret_id}` — Get a secret by ID  · required: 
- `PATCH /accounts/{account_id}/secrets_store/stores/{store_id}/secrets/{secret_id}` — Patch a secret  · required:   · body: (no required fields)
- `DELETE /accounts/{account_id}/secrets_store/stores/{store_id}/secrets/{secret_id}` — Delete a secret  · required: 
- `POST /accounts/{account_id}/secrets_store/stores/{store_id}/secrets/{secret_id}/duplicate` — Duplicate Secret  · required:   · body: name:string, scopes:string[]
