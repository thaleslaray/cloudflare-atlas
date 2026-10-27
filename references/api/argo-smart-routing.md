# API reference — argo-smart-routing

> Exact REST endpoints for **argo-smart-routing**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 4 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /zones/{zone_id}/argo/smart_routing` — Get Argo Smart Routing setting  · required: zone_id
- `PATCH /zones/{zone_id}/argo/smart_routing` — Patch Argo Smart Routing setting  · required: zone_id  · body: value:string
- `GET /zones/{zone_id}/argo/tiered_caching` — Get Tiered Caching setting  · required: zone_id
- `PATCH /zones/{zone_id}/argo/tiered_caching` — Patch Tiered Caching setting  · required: zone_id  · body: value:string
