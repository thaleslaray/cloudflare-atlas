# API reference — analytics

> Exact REST endpoints for **analytics**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 16 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `POST /accounts/{account_id}/analytics/query/data-security/content-findings/top-n` — Top integrations by content findings  · required:   · body: filters:object[], from:string, n:integer, to:string
- `POST /accounts/{account_id}/analytics/query/data-security/findings/summary` — Data security findings summary  · required:   · body: filters:object[], from:string, to:string
- `POST /accounts/{account_id}/analytics/query/data-security/findings/timeseries` — Data security findings timeseries  · required:   · body: filters:object[], from:string, to:string
- `POST /accounts/{account_id}/analytics/query/{dataset}/summary` — Query analytics summary  · required: dataset  · body: filters:object[], from:string, groupBy:string[], stats:string[], to:string
- `POST /accounts/{account_id}/analytics/query/{dataset}/timeseries` — Query analytics timeseries  · required: dataset  · body: filters:object[], from:string, groupBy:string[], resolution:string, stats:string[], to:string
- `POST /accounts/{account_id}/analytics/query/{dataset}/top-n` — Query analytics top-N  · required: dataset  · body: filters:object[], from:string, groupBy:string[], n:integer, orderBy:string, stats:string[], to:string
- `GET /accounts/{account_id}/analytics_engine/sql` — Execute an Analytics Engine SQL query via query parameter  · required: query
- `POST /accounts/{account_id}/analytics_engine/sql` — Execute an Analytics Engine SQL query via request body  · required:   · body: (no required fields)
- `GET /analytics/sql` — Query analytics datasets  · required: query
- `POST /analytics/sql` — Query analytics datasets  · required:   · body: query:string
- `GET /analytics/sql/introspection` — List available analytics datasets  · required: account_tag
- `GET /user/analytics/dashboard` — Get user analytics dashboard  · required: 
- `GET /zones/{zone_identifier}/analytics/colos` — Get analytics by Co-locations  · required: zone_identifier
- `GET /zones/{zone_identifier}/analytics/dashboard` — Get dashboard  · required: zone_identifier
- `GET /zones/{zone_id}/analytics/latency` — Argo Analytics for a zone  · required: zone_id
- `GET /zones/{zone_id}/analytics/latency/colos` — Argo Analytics for a zone at different PoPs  · required: zone_id
