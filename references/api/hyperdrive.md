# API reference — hyperdrive

> Exact REST endpoints for **hyperdrive**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 8 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /accounts/{account_id}/hyperdrive/configs` — List Hyperdrives  · required: account_id
- `POST /accounts/{account_id}/hyperdrive/configs` — Create Hyperdrive  · required: account_id  · body: name:string, origin:object
- `GET /accounts/{account_id}/hyperdrive/configs/{hyperdrive_id}` — Get Hyperdrive  · required: account_id, hyperdrive_id
- `PUT /accounts/{account_id}/hyperdrive/configs/{hyperdrive_id}` — Replace Hyperdrive  · required: account_id, hyperdrive_id  · body: id:string, name:string, origin:object
- `PATCH /accounts/{account_id}/hyperdrive/configs/{hyperdrive_id}` — Update Hyperdrive  · required: account_id, hyperdrive_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/hyperdrive/configs/{hyperdrive_id}` — Delete Hyperdrive  · required: account_id, hyperdrive_id
- `POST /accounts/{account_id}/hyperdrive/configs/{hyperdrive_id}/restart` — Restart Hyperdrive  · required: account_id, hyperdrive_id
- `POST /accounts/{account_id}/hyperdrive/integrationsOperations/{integration}/createDatabaseSignature` — Create Database Signature  · required: account_id, integration
