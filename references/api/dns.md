# API reference — dns

> Exact REST endpoints for **dns**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 60 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /accounts/{account_id}/dns_firewall` — List DNS Firewall Clusters  · required: account_id
- `POST /accounts/{account_id}/dns_firewall` — Create DNS Firewall Cluster  · required: account_id  · body: (no required fields)
- `GET /accounts/{account_id}/dns_firewall/{dns_firewall_id}` — DNS Firewall Cluster Details  · required: dns_firewall_id, account_id
- `PATCH /accounts/{account_id}/dns_firewall/{dns_firewall_id}` — Update DNS Firewall Cluster  · required: dns_firewall_id, account_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/dns_firewall/{dns_firewall_id}` — Delete DNS Firewall Cluster  · required: dns_firewall_id, account_id
- `GET /accounts/{account_id}/dns_firewall/{dns_firewall_id}/dns_analytics/report` — Table  · required: dns_firewall_id, account_id
- `GET /accounts/{account_id}/dns_firewall/{dns_firewall_id}/dns_analytics/report/bytime` — By Time  · required: dns_firewall_id, account_id
- `GET /accounts/{account_id}/dns_firewall/{dns_firewall_id}/reverse_dns` — Show DNS Firewall Cluster Reverse DNS  · required: dns_firewall_id, account_id
- `PATCH /accounts/{account_id}/dns_firewall/{dns_firewall_id}/reverse_dns` — Update DNS Firewall Cluster Reverse DNS  · required: dns_firewall_id, account_id  · body: (no required fields)
- `GET /accounts/{account_id}/dns_records/usage` — Get DNS Record Usage for Account  · required: account_id
- `GET /accounts/{account_id}/dns_settings` — Show DNS Settings  · required: account_id
- `PATCH /accounts/{account_id}/dns_settings` — Update DNS Settings  · required: account_id  · body: (no required fields)
- `GET /accounts/{account_id}/dns_settings/views` — List Internal DNS Views  · required: account_id
- `POST /accounts/{account_id}/dns_settings/views` — Create Internal DNS View  · required: account_id  · body: (no required fields)
- `GET /accounts/{account_id}/dns_settings/views/{view_id}` — DNS Internal View Details  · required: account_id, view_id
- `PATCH /accounts/{account_id}/dns_settings/views/{view_id}` — Update Internal DNS View  · required: account_id, view_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/dns_settings/views/{view_id}` — Delete Internal DNS View  · required: account_id, view_id
- `GET /radar/dns/summary/cache_hit` — Get DNS queries by cache status summary  · required: 
- `GET /radar/dns/summary/dnssec` — Get DNS queries by DNSSEC support summary  · required: 
- `GET /radar/dns/summary/dnssec_aware` — Get DNS queries by DNSSEC awareness summary  · required: 
- `GET /radar/dns/summary/dnssec_e2e` — Get DNS queries by DNSSEC end-to-end summary  · required: 
- `GET /radar/dns/summary/ip_version` — Get DNS queries by IP version summary  · required: 
- `GET /radar/dns/summary/matching_answer` — Get DNS queries by matching answer summary  · required: 
- `GET /radar/dns/summary/protocol` — Get DNS queries by protocol summary  · required: 
- `GET /radar/dns/summary/query_type` — Get DNS queries by type summary  · required: 
- `GET /radar/dns/summary/response_code` — Get DNS queries by response code summary  · required: 
- `GET /radar/dns/summary/response_ttl` — Get DNS queries by response TTL summary  · required: 
- `GET /radar/dns/summary/{dimension}` — Get DNS summary by dimension  · required: dimension
- `GET /radar/dns/timeseries` — Get DNS queries time series  · required: 
- `GET /radar/dns/timeseries_groups/cache_hit` — Get DNS queries by cache status time series  · required: 
- `GET /radar/dns/timeseries_groups/dnssec` — Get DNS queries by DNSSEC support time series  · required: 
- `GET /radar/dns/timeseries_groups/dnssec_aware` — Get DNS queries by DNSSEC awareness time series  · required: 
- `GET /radar/dns/timeseries_groups/dnssec_e2e` — Get DNS queries by DNSSEC end-to-end time series  · required: 
- `GET /radar/dns/timeseries_groups/ip_version` — Get DNS queries by IP version time series  · required: 
- `GET /radar/dns/timeseries_groups/matching_answer` — Get DNS queries by matching answer time series  · required: 
- `GET /radar/dns/timeseries_groups/protocol` — Get DNS queries by protocol time series  · required: 
- `GET /radar/dns/timeseries_groups/query_type` — Get DNS queries by type time series  · required: 
- `GET /radar/dns/timeseries_groups/response_code` — Get DNS queries by response code time series  · required: 
- `GET /radar/dns/timeseries_groups/response_ttl` — Get DNS queries by response TTL time series  · required: 
- `GET /radar/dns/timeseries_groups/{dimension}` — Get DNS time series grouped by dimension  · required: dimension
- `GET /radar/dns/top/ases` — Get top ASes by DNS queries  · required: 
- `GET /radar/dns/top/locations` — Get top locations by DNS queries  · required: 
- `GET /zones/{zone_id}/dns_analytics/report` — Table  · required: zone_id
- `GET /zones/{zone_id}/dns_analytics/report/bytime` — By Time  · required: zone_id
- `GET /zones/{zone_id}/dns_records` — List DNS Records  · required: zone_id
- `POST /zones/{zone_id}/dns_records` — Create DNS Record  · required: zone_id  · body: (no required fields)
- `POST /zones/{zone_id}/dns_records/batch` — Batch DNS Records  · required: zone_id  · body: (no required fields)
- `GET /zones/{zone_id}/dns_records/export` — Export DNS Records  · required: zone_id
- `POST /zones/{zone_id}/dns_records/import` — Import DNS Records  · required: zone_id  · body: file:string
- `POST /zones/{zone_id}/dns_records/scan` — Scan DNS Records  · required: zone_id
- `GET /zones/{zone_id}/dns_records/scan/review` — List Scanned DNS Records  · required: zone_id
- `POST /zones/{zone_id}/dns_records/scan/review` — Review Scanned DNS Records  · required: zone_id  · body: (no required fields)
- `POST /zones/{zone_id}/dns_records/scan/trigger` — Trigger DNS Record Scan  · required: zone_id
- `GET /zones/{zone_id}/dns_records/usage` — Get DNS Record Usage  · required: zone_id
- `GET /zones/{zone_id}/dns_records/{dns_record_id}` — DNS Record Details  · required: dns_record_id, zone_id
- `PUT /zones/{zone_id}/dns_records/{dns_record_id}` — Overwrite DNS Record  · required: dns_record_id, zone_id  · body: (no required fields)
- `PATCH /zones/{zone_id}/dns_records/{dns_record_id}` — Update DNS Record  · required: dns_record_id, zone_id  · body: (no required fields)
- `DELETE /zones/{zone_id}/dns_records/{dns_record_id}` — Delete DNS Record  · required: dns_record_id, zone_id
- `GET /zones/{zone_id}/dns_settings` — Show DNS Settings  · required: zone_id
- `PATCH /zones/{zone_id}/dns_settings` — Update DNS Settings  · required: zone_id  · body: (no required fields)
