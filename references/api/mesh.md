# API reference — mesh

> Exact REST endpoints for **mesh**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 11 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /accounts/{account_id}/warp_connector` — List Mesh nodes  · required: account_id
- `POST /accounts/{account_id}/warp_connector` — Create a Mesh node  · required: account_id  · body: name:string
- `GET /accounts/{account_id}/warp_connector/{tunnel_id}` — Get a Mesh node  · required: account_id, tunnel_id
- `PATCH /accounts/{account_id}/warp_connector/{tunnel_id}` — Update a Mesh node  · required: account_id, tunnel_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/warp_connector/{tunnel_id}` — Delete a Mesh node  · required: account_id, tunnel_id
- `GET /accounts/{account_id}/warp_connector/{tunnel_id}/configurations` — Get Mesh node HA configuration  · required: account_id, tunnel_id
- `PUT /accounts/{account_id}/warp_connector/{tunnel_id}/configurations` — Update Mesh node HA configuration  · required: account_id, tunnel_id  · body: ha_mode:string
- `GET /accounts/{account_id}/warp_connector/{tunnel_id}/connections` — List Mesh node connections  · required: account_id, tunnel_id
- `GET /accounts/{account_id}/warp_connector/{tunnel_id}/connectors/{connector_id}` — Get a Mesh node connector  · required: account_id, tunnel_id, connector_id
- `PUT /accounts/{account_id}/warp_connector/{tunnel_id}/failover` — Trigger a manual failover for a Mesh node  · required: account_id, tunnel_id  · body: client_id:object
- `GET /accounts/{account_id}/warp_connector/{tunnel_id}/token` — Get a Mesh node token  · required: account_id, tunnel_id
