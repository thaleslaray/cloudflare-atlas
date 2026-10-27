# API reference — ssl

> Exact REST endpoints for **ssl**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 12 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `POST /zones/{zone_id}/ssl/analyze` — Analyze Certificate  · required: zone_id  · body: (no required fields)
- `GET /zones/{zone_id}/ssl/certificate_packs` — List Certificate Packs  · required: zone_id
- `POST /zones/{zone_id}/ssl/certificate_packs/order` — Order Advanced Certificate Manager Certificate Pack  · required: zone_id  · body: certificate_authority:string, hosts:string[], type:string, validation_method:string, validity_days:integer
- `GET /zones/{zone_id}/ssl/certificate_packs/quota` — Get Certificate Pack Quotas  · required: zone_id
- `GET /zones/{zone_id}/ssl/certificate_packs/{certificate_pack_id}` — Get Certificate Pack  · required: certificate_pack_id, zone_id
- `PATCH /zones/{zone_id}/ssl/certificate_packs/{certificate_pack_id}` — Restart Validation or Update Advanced Certificate Manager Certificate Pack  · required: certificate_pack_id, zone_id  · body: (no required fields)
- `DELETE /zones/{zone_id}/ssl/certificate_packs/{certificate_pack_id}` — Delete Advanced Certificate Manager Certificate Pack  · required: certificate_pack_id, zone_id
- `GET /zones/{zone_id}/ssl/recommendation` — SSL/TLS Recommendation  · required: zone_id
- `GET /zones/{zone_id}/ssl/universal/settings` — Universal SSL Settings Details  · required: zone_id
- `PATCH /zones/{zone_id}/ssl/universal/settings` — Edit Universal SSL Settings  · required: zone_id  · body: (no required fields)
- `GET /zones/{zone_id}/ssl/verification` — SSL Verification Details  · required: zone_id
- `PATCH /zones/{zone_id}/ssl/verification/{certificate_pack_id}` — Edit SSL Certificate Pack Validation Method  · required: certificate_pack_id, zone_id  · body: validation_method:string
