# API reference — zone-settings

> Exact REST endpoints for **zone-settings**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 44 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

> Note: the per-zone configuration surface (`/zones/{zone_id}/settings/*`) — one root, one endpoint
> pair per toggle. It is not a product in the catalog: the toggles belong to Speed, Cache, SSL/TLS,
> Images and others, and each product file explains its own. This slice exists so the endpoints are
> reachable at all; before 2026-08-17 no slice claimed the root and all 42 operations were reported
> as an in-scope gap. **This slice churns** — Cloudflare adds and retires zone toggles often, so
> treat a stale entry here as likely before assuming the API changed.

- `GET /zones/{zone_id}/settings` — Get all zone settings  · required: zone_id
- `PATCH /zones/{zone_id}/settings` — Edit multiple zone settings  · required: zone_id  · body: (no required fields)
- `GET /zones/{zone_id}/settings/aegis` — Get aegis setting  · required: zone_id
- `PATCH /zones/{zone_id}/settings/aegis` — Change aegis setting  · required: zone_id  · body: value:object
- `GET /zones/{zone_id}/settings/auto_origin_tls_kex` — Get Auto-Origin TLS KEX enrollment status for the given zone  · required: zone_id
- `PATCH /zones/{zone_id}/settings/auto_origin_tls_kex` — Patch Auto-Origin TLS KEX enrollment status for the given zone  · required: zone_id  · body: enabled:boolean
- `GET /zones/{zone_id}/settings/automatic_platform_optimization` — Get Automatic Platform Optimization setting  · required: zone_id
- `PATCH /zones/{zone_id}/settings/automatic_platform_optimization` — Change Automatic Platform Optimization setting  · required: zone_id  · body: value:string
- `GET /zones/{zone_id}/settings/binary_ast` — Get Binary AST setting  · required: zone_id
- `PATCH /zones/{zone_id}/settings/binary_ast` — Change Binary AST setting  · required: zone_id  · body: value:string
- `GET /zones/{zone_id}/settings/csam_scanner_third_party` — Get CSAM Scanner setting  · required: 
- `PATCH /zones/{zone_id}/settings/csam_scanner_third_party` — Update CSAM Scanner setting  · required:   · body: (no required fields)
- `GET /zones/{zone_id}/settings/fonts` — Get Cloudflare Fonts setting  · required: zone_id
- `PATCH /zones/{zone_id}/settings/fonts` — Change Cloudflare Fonts setting  · required: zone_id  · body: value:string
- `GET /zones/{zone_id}/settings/google-tag-gateway/config` — Get Google Tag Gateway configuration  · required: zone_id
- `PUT /zones/{zone_id}/settings/google-tag-gateway/config` — Update Google Tag Gateway configuration  · required: zone_id  · body: enabled:boolean, endpoint:string, hideOriginalIp:boolean, measurementId:string
- `GET /zones/{zone_id}/settings/h2_prioritization` — Get HTTP/2 Prioritization setting  · required: zone_id
- `PATCH /zones/{zone_id}/settings/h2_prioritization` — Change HTTP/2 Prioritization setting  · required: zone_id  · body: value:string
- `GET /zones/{zone_id}/settings/image_resizing` — Get Image Transformations setting  · required: zone_id
- `PATCH /zones/{zone_id}/settings/image_resizing` — Change Image Transformations setting  · required: zone_id  · body: value:string
- `GET /zones/{zone_id}/settings/nel` — Get NEL setting  · required: zone_id
- `PATCH /zones/{zone_id}/settings/nel` — Edit NEL setting  · required: zone_id  · body: value:object
- `GET /zones/{zone_id}/settings/origin_h2_max_streams` — Get Origin H2 Max Streams Setting  · required: zone_id
- `PATCH /zones/{zone_id}/settings/origin_h2_max_streams` — Change Origin H2 Max Streams Setting  · required: zone_id  · body: value:integer
- `GET /zones/{zone_id}/settings/origin_max_http_version` — Get Origin Max HTTP Version Setting  · required: zone_id
- `PATCH /zones/{zone_id}/settings/origin_max_http_version` — Change Origin Max HTTP Version Setting  · required: zone_id  · body: value:string
- `GET /zones/{zone_id}/settings/origin_tls_compliance_modes` — Get Origin TLS Compliance Modes setting  · required: zone_id
- `PUT /zones/{zone_id}/settings/origin_tls_compliance_modes` — Replace Origin TLS Compliance Modes setting  · required: zone_id  · body: value:string[]
- `PATCH /zones/{zone_id}/settings/origin_tls_compliance_modes` — Change Origin TLS Compliance Modes setting  · required: zone_id  · body: value:string[]
- `DELETE /zones/{zone_id}/settings/origin_tls_compliance_modes` — Delete Origin TLS Compliance Modes setting  · required: zone_id
- `GET /zones/{zone_id}/settings/rum` — Get RUM status for a zone  · required: zone_id
- `PATCH /zones/{zone_id}/settings/rum` — Toggle RUM on/off for a zone  · required: zone_id  · body: (no required fields)
- `GET /zones/{zone_id}/settings/speed_brain` — Get Cloudflare Speed Brain setting  · required: zone_id
- `PATCH /zones/{zone_id}/settings/speed_brain` — Change Cloudflare Speed Brain setting  · required: zone_id  · body: value:string
- `GET /zones/{zone_id}/settings/ssl_automatic_mode` — Get Automatic SSL/TLS enrollment status for the given zone  · required: zone_id
- `PATCH /zones/{zone_id}/settings/ssl_automatic_mode` — Patch Automatic SSL/TLS Enrollment status for given zone  · required: zone_id  · body: value:string
- `GET /zones/{zone_id}/settings/transformations_allowed_origins` — Get Image Transformations Allowed Origins setting  · required: zone_id
- `PATCH /zones/{zone_id}/settings/transformations_allowed_origins` — Change Image Transformations Allowed Origins setting  · required: zone_id  · body: value:string
- `GET /zones/{zone_id}/settings/transformations_c2pa` — Get Image Transformations C2PA setting  · required: zone_id
- `PATCH /zones/{zone_id}/settings/transformations_c2pa` — Change Image Transformations C2PA setting  · required: zone_id  · body: value:string
- `GET /zones/{zone_id}/settings/transformations_config` — Get Transformations configuration  · required: zone_id
- `PATCH /zones/{zone_id}/settings/transformations_config` — Change Transformations configuration  · required: zone_id  · body: value:object
- `GET /zones/{zone_id}/settings/{setting_id}` — Get zone setting  · required: zone_id, setting_id
- `PATCH /zones/{zone_id}/settings/{setting_id}` — Edit zone setting  · required: zone_id, setting_id  · body: (no required fields)
