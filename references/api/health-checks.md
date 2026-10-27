# API reference — health-checks

> Exact REST endpoints for **health-checks**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 15 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /zones/{zone_id}/healthchecks` — List Health Checks  · required: zone_id
- `POST /zones/{zone_id}/healthchecks` — Create Health Check  · required: zone_id  · body: address:string, name:string
- `POST /zones/{zone_id}/healthchecks/preview` — Create Preview Health Check  · required: zone_id  · body: address:string, name:string
- `GET /zones/{zone_id}/healthchecks/preview/{healthcheck_id}` — Health Check Preview Details  · required: healthcheck_id, zone_id
- `DELETE /zones/{zone_id}/healthchecks/preview/{healthcheck_id}` — Delete Preview Health Check  · required: healthcheck_id, zone_id  · body: (spec carries no schema — check the docs)
- `GET /zones/{zone_id}/healthchecks/{healthcheck_id}` — Health Check Details  · required: healthcheck_id, zone_id
- `PUT /zones/{zone_id}/healthchecks/{healthcheck_id}` — Update Health Check  · required: healthcheck_id, zone_id  · body: address:string, name:string
- `PATCH /zones/{zone_id}/healthchecks/{healthcheck_id}` — Patch Health Check  · required: healthcheck_id, zone_id  · body: address:string, name:string
- `DELETE /zones/{zone_id}/healthchecks/{healthcheck_id}` — Delete Health Check  · required: healthcheck_id, zone_id  · body: (spec carries no schema — check the docs)
- `GET /zones/{zone_id}/smart_shield/healthchecks` — List Health Checks  · required: zone_id
- `POST /zones/{zone_id}/smart_shield/healthchecks` — Create Health Check  · required: zone_id  · body: address:string, name:string
- `GET /zones/{zone_id}/smart_shield/healthchecks/{healthcheck_id}` — Health Check Details  · required: healthcheck_id, zone_id
- `PUT /zones/{zone_id}/smart_shield/healthchecks/{healthcheck_id}` — Update Health Check  · required: healthcheck_id, zone_id  · body: errors:object[], messages:object[], result:object, success:boolean
- `PATCH /zones/{zone_id}/smart_shield/healthchecks/{healthcheck_id}` — Patch Health Check  · required: healthcheck_id, zone_id  · body: address:string, name:string
- `DELETE /zones/{zone_id}/smart_shield/healthchecks/{healthcheck_id}` — Delete Health Check  · required: healthcheck_id, zone_id
