# API reference — registrar

> Exact REST endpoints for **registrar**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 13 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `POST /accounts/{account_id}/registrar/domain-check` — Check domain availability  · required: account_id  · body: domains:string[]
- `GET /accounts/{account_id}/registrar/domain-search` — Search for available domains  · required: account_id, q
- `GET /accounts/{account_id}/registrar/domains` — List domains  · required: account_id
- `GET /accounts/{account_id}/registrar/domains/{domain_name}` — Get domain  · required: domain_name, account_id
- `PUT /accounts/{account_id}/registrar/domains/{domain_name}` — Update domain  · required: domain_name, account_id  · body: (no required fields)
- `GET /accounts/{account_id}/registrar/extensions` — List extensions  · required: account_id
- `GET /accounts/{account_id}/registrar/extensions/{extension}` — Get extension  · required: account_id, extension
- `GET /accounts/{account_id}/registrar/registrations` — List Registrations  · required: account_id
- `POST /accounts/{account_id}/registrar/registrations` — Create Registration  · required: account_id  · body: domain_name:string
- `GET /accounts/{account_id}/registrar/registrations/{domain_name}` — Get Registration  · required: account_id, domain_name
- `PATCH /accounts/{account_id}/registrar/registrations/{domain_name}` — Update Registration  · required: account_id, domain_name  · body: (no required fields)
- `GET /accounts/{account_id}/registrar/registrations/{domain_name}/registration-status` — Get Registration Status  · required: account_id, domain_name
- `GET /accounts/{account_id}/registrar/registrations/{domain_name}/update-status` — Get Update Status  · required: account_id, domain_name
