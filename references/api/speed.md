# API reference — speed

> Exact REST endpoints for **speed**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 10 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

> Note: Observatory endpoints (`/zones/{zone_id}/speed_api/…`). These lived in `pages.md` until
> 2026-08-17, where they had arrived by root collision: Speed tests a *webpage*, and the matcher read
> `/speed_api/pages` as Cloudflare Pages. `pages.md` now excludes the root via NOT_MINE, so the
> operations are listed here once rather than in two slices.

- `GET /zones/{zone_id}/speed_api/availabilities` — Get quota and availability  · required: zone_id
- `GET /zones/{zone_id}/speed_api/pages` — List tested webpages  · required: zone_id
- `GET /zones/{zone_id}/speed_api/pages/{url}/tests` — List page test history  · required: zone_id, url
- `POST /zones/{zone_id}/speed_api/pages/{url}/tests` — Start page test  · required: zone_id, url  · body: (no required fields)
- `DELETE /zones/{zone_id}/speed_api/pages/{url}/tests` — Delete all page tests  · required: zone_id, url
- `GET /zones/{zone_id}/speed_api/pages/{url}/tests/{test_id}` — Get a page test result  · required: zone_id, url, test_id
- `GET /zones/{zone_id}/speed_api/pages/{url}/trend` — List core web vital metrics trend  · required: zone_id, url, region, deviceType, start, tz, metrics
- `GET /zones/{zone_id}/speed_api/schedule/{url}` — Get a page test schedule  · required: zone_id, url
- `POST /zones/{zone_id}/speed_api/schedule/{url}` — Create scheduled page test  · required: zone_id, url
- `DELETE /zones/{zone_id}/speed_api/schedule/{url}` — Delete scheduled page test  · required: zone_id, url
