# API reference — smart-shield

> Exact REST endpoints for **smart-shield**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 2 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

> Note: Smart Shield is a zone-level toggle, so its whole API surface is two operations on
> `/zones/{zone_id}/smart_shield` (read + patch settings). Sliced 2026-08-17; before that the two
> operations belonged to no slice, and the segment was being reported as a gap under `health-checks`,
> which merely touched it.

- `GET /zones/{zone_id}/smart_shield` — Get Smart Shield Settings  · required: zone_id
- `PATCH /zones/{zone_id}/smart_shield` — Patch Smart Shield Settings  · required: zone_id  · body: (no required fields)
