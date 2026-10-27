# API reference — email-routing

> Exact REST endpoints for **email-routing**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 46 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /accounts/{account_id}/email/routing/addresses` — List destination addresses  · required: account_id
- `POST /accounts/{account_id}/email/routing/addresses` — Create a destination address  · required: account_id  · body: email:string
- `GET /accounts/{account_id}/email/routing/addresses/{destination_address_identifier}` — Get a destination address  · required: destination_address_identifier, account_id
- `PATCH /accounts/{account_id}/email/routing/addresses/{destination_address_identifier}` — Update destination address  · required: destination_address_identifier, account_id  · body: status:string
- `DELETE /accounts/{account_id}/email/routing/addresses/{destination_address_identifier}` — Delete destination address  · required: destination_address_identifier, account_id
- `GET /accounts/{account_id}/email/routing/rules` — List account routing rules  · required: account_id
- `POST /accounts/{account_id}/email/routing/rules/plan` — Plan account routing rule changes  · required: account_id  · body: owner_worker_tag:string
- `GET /accounts/{account_id}/email/routing/suppression` — List account email suppressions  · required: account_id
- `POST /accounts/{account_id}/email/routing/suppression` — Create account email suppression  · required: account_id  · body: email:string
- `GET /accounts/{account_id}/email/routing/suppression/{suppression_id}` — Get account email suppression  · required: account_id, suppression_id
- `DELETE /accounts/{account_id}/email/routing/suppression/{suppression_id}` — Delete account email suppression  · required: account_id, suppression_id
- `GET /radar/email/routing/summary/arc` — Get email ARC validation summary  · required: 
- `GET /radar/email/routing/summary/dkim` — Get email DKIM validation summary  · required: 
- `GET /radar/email/routing/summary/dmarc` — Get email DMARC validation summary  · required: 
- `GET /radar/email/routing/summary/encrypted` — Get email encryption status summary  · required: 
- `GET /radar/email/routing/summary/ip_version` — Get email IP version summary  · required: 
- `GET /radar/email/routing/summary/spf` — Get email SPF validation summary  · required: 
- `GET /radar/email/routing/summary/{dimension}` — Get email routing summary by dimension  · required: dimension
- `GET /radar/email/routing/timeseries_groups/arc` — Get email ARC validation time series  · required: 
- `GET /radar/email/routing/timeseries_groups/dkim` — Get email DKIM validation time series  · required: 
- `GET /radar/email/routing/timeseries_groups/dmarc` — Get email DMARC validation time series  · required: 
- `GET /radar/email/routing/timeseries_groups/encrypted` — Get email encryption status time series  · required: 
- `GET /radar/email/routing/timeseries_groups/ip_version` — Get email IP version time series  · required: 
- `GET /radar/email/routing/timeseries_groups/spf` — Get email SPF validation time series  · required: 
- `GET /radar/email/routing/timeseries_groups/{dimension}` — Get email routing time series grouped by dimension  · required: dimension
- `GET /zones/{zone_id}/email/routing` — Get Email Routing settings  · required: zone_id
- `PUT /zones/{zone_id}/email/routing` — Update Email Routing settings  · required: zone_id  · body: (no required fields)
- `PATCH /zones/{zone_id}/email/routing` — Update Email Routing settings  · required: zone_id  · body: (no required fields)
- `POST /zones/{zone_id}/email/routing/disable` — Disable Email Routing  · required: zone_id
- `GET /zones/{zone_id}/email/routing/dns` — Email Routing - DNS settings  · required: zone_id
- `POST /zones/{zone_id}/email/routing/dns` — Enable Email Routing  · required: zone_id  · body: (no required fields)
- `PATCH /zones/{zone_id}/email/routing/dns` — Unlock Email Routing  · required: zone_id  · body: (no required fields)
- `DELETE /zones/{zone_id}/email/routing/dns` — Disable Email Routing  · required: zone_id  · body: (no required fields)
- `POST /zones/{zone_id}/email/routing/enable` — Enable Email Routing  · required: zone_id
- `GET /zones/{zone_id}/email/routing/rules` — List routing rules  · required: zone_id
- `POST /zones/{zone_id}/email/routing/rules` — Create routing rule  · required: zone_id  · body: actions:object[], matchers:object[]
- `GET /zones/{zone_id}/email/routing/rules/catch_all` — Get catch-all rule  · required: zone_id
- `PUT /zones/{zone_id}/email/routing/rules/catch_all` — Update catch-all rule  · required: zone_id  · body: actions:object[], matchers:object[]
- `GET /zones/{zone_id}/email/routing/rules/{rule_identifier}` — Get routing rule  · required: rule_identifier, zone_id
- `PUT /zones/{zone_id}/email/routing/rules/{rule_identifier}` — Update routing rule  · required: rule_identifier, zone_id  · body: actions:object[], matchers:object[]
- `DELETE /zones/{zone_id}/email/routing/rules/{rule_identifier}` — Delete routing rule  · required: rule_identifier, zone_id
- `GET /zones/{zone_id}/email/routing/suppression` — List zone email suppressions  · required: zone_id
- `POST /zones/{zone_id}/email/routing/suppression` — Create zone email suppression  · required: zone_id  · body: email:string
- `GET /zones/{zone_id}/email/routing/suppression/{suppression_id}` — Get zone email suppression  · required: zone_id, suppression_id
- `DELETE /zones/{zone_id}/email/routing/suppression/{suppression_id}` — Delete zone email suppression  · required: zone_id, suppression_id
- `POST /zones/{zone_id}/email/routing/unlock` — Unlock Email Routing  · required: zone_id  · body: (no required fields)
