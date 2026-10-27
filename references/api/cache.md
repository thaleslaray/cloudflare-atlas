# API reference — cache

> Exact REST endpoints for **cache**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 25 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /zones/{zone_id}/cache/cache_reserve` — Get Cache Reserve setting  · required: zone_id
- `PATCH /zones/{zone_id}/cache/cache_reserve` — Change Cache Reserve setting  · required: zone_id  · body: value:string
- `GET /zones/{zone_id}/cache/cache_reserve_clear` — Get Cache Reserve Clear  · required: zone_id
- `POST /zones/{zone_id}/cache/cache_reserve_clear` — Start Cache Reserve Clear  · required: zone_id
- `GET /zones/{zone_id}/cache/origin_cloud_regions` — List origin cloud region mappings  · required: zone_id
- `POST /zones/{zone_id}/cache/origin_cloud_regions` — Create an origin cloud region mapping  · required: zone_id  · body: ip:string, region:string, vendor:string
- `PATCH /zones/{zone_id}/cache/origin_cloud_regions` — Create or update an origin cloud region mapping  · required: zone_id  · body: ip:string, region:string, vendor:string
- `PATCH /zones/{zone_id}/cache/origin_cloud_regions/batch` — Batch create or update origin cloud region mappings  · required: zone_id  · body: (no required fields)
- `DELETE /zones/{zone_id}/cache/origin_cloud_regions/batch` — Batch delete origin cloud region mappings  · required: zone_id  · body: (no required fields)
- `GET /zones/{zone_id}/cache/origin_cloud_regions/supported_regions` — List supported cloud vendors and regions  · required: zone_id
- `GET /zones/{zone_id}/cache/origin_cloud_regions/{origin_ip}` — Get an origin cloud region mapping  · required: zone_id, origin_ip
- `DELETE /zones/{zone_id}/cache/origin_cloud_regions/{origin_ip}` — Delete an origin cloud region mapping  · required: zone_id, origin_ip
- `GET /zones/{zone_id}/cache/origin_post_quantum_encryption` — Get Origin Post-Quantum Encryption setting  · required: zone_id
- `PUT /zones/{zone_id}/cache/origin_post_quantum_encryption` — Change Origin Post-Quantum Encryption setting  · required: zone_id  · body: value:string
- `GET /zones/{zone_id}/cache/regional_tiered_cache` — Get Regional Tiered Cache setting  · required: zone_id
- `PATCH /zones/{zone_id}/cache/regional_tiered_cache` — Change Regional Tiered Cache setting  · required: zone_id  · body: value:string
- `GET /zones/{zone_id}/cache/tiered_cache_smart_topology_enable` — Get Smart Tiered Cache setting  · required: zone_id
- `POST /zones/{zone_id}/cache/tiered_cache_smart_topology_enable` — Create Smart Tiered Cache setting  · required: zone_id  · body: value:string
- `PATCH /zones/{zone_id}/cache/tiered_cache_smart_topology_enable` — Patch Smart Tiered Cache setting  · required: zone_id  · body: value:string
- `DELETE /zones/{zone_id}/cache/tiered_cache_smart_topology_enable` — Delete Smart Tiered Cache setting  · required: zone_id
- `GET /zones/{zone_id}/cache/variants` — Get variants setting  · required: zone_id
- `PATCH /zones/{zone_id}/cache/variants` — Change variants setting  · required: zone_id  · body: value:object
- `DELETE /zones/{zone_id}/cache/variants` — Delete variants setting  · required: zone_id
- `GET /zones/{zone_id}/smart_shield/cache_reserve_clear` — Get Cache Reserve Clear  · required: zone_id
- `POST /zones/{zone_id}/smart_shield/cache_reserve_clear` — Start Cache Reserve Clear  · required: zone_id
