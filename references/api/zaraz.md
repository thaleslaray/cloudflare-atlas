# API reference — zaraz

> Exact REST endpoints for **zaraz**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 10 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /zones/{zone_id}/settings/zaraz/config` — Get Zaraz configuration  · required: zone_id
- `PUT /zones/{zone_id}/settings/zaraz/config` — Update Zaraz configuration  · required: zone_id  · body: dataLayer:boolean, debugKey:string, settings:object, tools:object, triggers:object, variables:object, zarazVersion:integer
- `GET /zones/{zone_id}/settings/zaraz/default` — Get default Zaraz configuration  · required: zone_id
- `GET /zones/{zone_id}/settings/zaraz/export` — Export Zaraz configuration  · required: zone_id
- `GET /zones/{zone_id}/settings/zaraz/history` — List Zaraz historical configuration records  · required: zone_id
- `PUT /zones/{zone_id}/settings/zaraz/history` — Restore Zaraz historical configuration by ID  · required: zone_id  · body: (no required fields)
- `GET /zones/{zone_id}/settings/zaraz/history/configs` — Get Zaraz historical configurations by ID(s)  · required: zone_id, ids
- `POST /zones/{zone_id}/settings/zaraz/publish` — Publish Zaraz preview configuration  · required: zone_id  · body: (no required fields)
- `GET /zones/{zone_id}/settings/zaraz/workflow` — Get Zaraz workflow  · required: zone_id
- `PUT /zones/{zone_id}/settings/zaraz/workflow` — Update Zaraz workflow  · required: zone_id  · body: (no required fields)
