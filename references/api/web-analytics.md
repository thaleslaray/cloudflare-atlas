# API reference — web-analytics

> Exact REST endpoints for **web-analytics**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 13 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

> Note: Web Analytics site and rule management lives under the `rum` root (Real User Monitoring),
> not under `web-analytics` — which is why no slice claimed these 13 operations until 2026-08-17.
> Metric *data* is not here: it is read through the GraphQL Analytics API, honouring `sampleInterval`.

- `POST /accounts/{account_id}/rum/site_info` — Create a Web Analytics site  · required: account_id  · body: (no required fields)
- `GET /accounts/{account_id}/rum/site_info/list` — List Web Analytics sites  · required: account_id
- `GET /accounts/{account_id}/rum/site_info/site_tag/list` — List Web Analytics site tags  · required: account_id
- `GET /accounts/{account_id}/rum/site_info/validate/{hostname}` — Validate a Web Analytics site hostname  · required: account_id, hostname
- `GET /accounts/{account_id}/rum/site_info/zone_tag/list` — List Web Analytics zone tags  · required: account_id
- `GET /accounts/{account_id}/rum/site_info/{site_id}` — Get a Web Analytics site  · required: account_id, site_id
- `PUT /accounts/{account_id}/rum/site_info/{site_id}` — Update a Web Analytics site  · required: account_id, site_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/rum/site_info/{site_id}` — Delete a Web Analytics site  · required: account_id, site_id
- `POST /accounts/{account_id}/rum/v2/{ruleset_id}/rule` — Create a Web Analytics rule  · required: account_id, ruleset_id  · body: (no required fields)
- `PUT /accounts/{account_id}/rum/v2/{ruleset_id}/rule/{rule_id}` — Update a Web Analytics rule  · required: account_id, ruleset_id, rule_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/rum/v2/{ruleset_id}/rule/{rule_id}` — Delete a Web Analytics rule  · required: account_id, ruleset_id, rule_id
- `GET /accounts/{account_id}/rum/v2/{ruleset_id}/rules` — List rules in Web Analytics ruleset  · required: account_id, ruleset_id
- `POST /accounts/{account_id}/rum/v2/{ruleset_id}/rules` — Update Web Analytics rules  · required: account_id, ruleset_id  · body: (no required fields)
