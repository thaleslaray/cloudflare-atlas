# API reference — spectrum

> Exact REST endpoints for **spectrum**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 9 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /zones/{zone_id}/spectrum/analytics/aggregate/current` — Get current aggregated analytics  · required: zone_id
- `GET /zones/{zone_id}/spectrum/analytics/events/bytime` — Get analytics by time  · required: zone_id, time_delta
- `GET /zones/{zone_id}/spectrum/analytics/events/summary` — Get analytics summary  · required: zone_id
- `GET /zones/{zone_id}/spectrum/apps` — List Spectrum applications  · required: zone_id
- `POST /zones/{zone_id}/spectrum/apps` — Create Spectrum application using a name for the origin  · required: zone_id  · body: created_on:object, dns:object, id:object, modified_on:object, protocol:string, traffic_type:string
- `GET /zones/{zone_id}/spectrum/apps/{app_id}` — Get Spectrum application configuration  · required: app_id, zone_id
- `PUT /zones/{zone_id}/spectrum/apps/{app_id}` — Update Spectrum application configuration using a name for the origin  · required: app_id, zone_id  · body: created_on:object, dns:object, id:object, modified_on:object, protocol:string, traffic_type:string
- `DELETE /zones/{zone_id}/spectrum/apps/{app_id}` — Delete Spectrum application  · required: app_id, zone_id
- `GET /zones/{zone_id}/spectrum/protocols` — List Spectrum application protocols  · required: zone_id
