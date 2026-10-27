# API reference — bots

> Exact REST endpoints for **bots**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 17 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /radar/ai/bots/summary/user_agent` — Get AI user agents summary  · required: 
- `GET /radar/ai/bots/summary/{dimension}` — Get AI bots HTTP requests distribution by dimension  · required: dimension
- `GET /radar/ai/bots/timeseries` — Get AI bots HTTP requests time series  · required: 
- `GET /radar/ai/bots/timeseries_groups/user_agent` — Get AI user agents time series  · required: 
- `GET /radar/ai/bots/timeseries_groups/{dimension}` — Get time series distribution of AI bots HTTP requests by dimension.  · required: dimension
- `GET /radar/bots` — List bots  · required: 
- `GET /radar/bots/crawlers/summary/{dimension}` — Get crawler HTTP request distribution by dimension  · required: dimension
- `GET /radar/bots/crawlers/timeseries_groups/{dimension}` — Get time series of crawler HTTP request distribution by dimension  · required: dimension
- `GET /radar/bots/summary/{dimension}` — Get bots HTTP requests distribution by dimension  · required: dimension
- `GET /radar/bots/timeseries` — Get bots HTTP requests time series  · required: 
- `GET /radar/bots/timeseries_groups/{dimension}` — Get time series distribution of bots HTTP requests by dimension.  · required: dimension
- `GET /radar/bots/{bot_slug}` — Get bot details  · required: bot_slug
- `GET /radar/verified_bots/top/bots` — Get top verified bots by HTTP requests  · required: 
- `GET /zones/{zone_id}/bot_management` — Get Zone Bot Management Config  · required: zone_id
- `PUT /zones/{zone_id}/bot_management` — Update Zone Bot Management Config  · required: zone_id  · body: (no required fields)
- `GET /zones/{zone_id}/bot_management/feedback` — List zone feedback reports  · required: zone_id
- `POST /zones/{zone_id}/bot_management/feedback` — Submit a feedback report  · required: zone_id  · body: description:string, expression:string, first_request_seen_at:string, last_request_seen_at:string, requests:integer, requests_by_attribute:object, requests_by_score:object, requests_by_score_src:object, type:string
