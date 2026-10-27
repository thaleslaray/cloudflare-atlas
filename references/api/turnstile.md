# API reference — turnstile

> Exact REST endpoints for **turnstile**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 6 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /accounts/{account_id}/challenges/widgets` — List Turnstile Widgets  · required: 
- `POST /accounts/{account_id}/challenges/widgets` — Create a Turnstile Widget  · required:   · body: domains:string[], mode:string, name:string
- `GET /accounts/{account_id}/challenges/widgets/{sitekey}` — Turnstile Widget Details  · required: 
- `PUT /accounts/{account_id}/challenges/widgets/{sitekey}` — Update a Turnstile Widget  · required:   · body: domains:string[], mode:string, name:string
- `DELETE /accounts/{account_id}/challenges/widgets/{sitekey}` — Delete a Turnstile Widget  · required: 
- `POST /accounts/{account_id}/challenges/widgets/{sitekey}/rotate_secret` — Rotate Secret for a Turnstile Widget  · required:   · body: (no required fields)
