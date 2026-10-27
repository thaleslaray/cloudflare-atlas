# API reference — email-service

> Exact REST endpoints for **email-service**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 64 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /accounts/{account_id}/dlp/email/account_mapping` — Get mapping  · required: account_id
- `POST /accounts/{account_id}/dlp/email/account_mapping` — Create mapping  · required: account_id  · body: auth_requirements:object
- `GET /accounts/{account_id}/dlp/email/rules` — List all email scanner rules  · required: account_id
- `POST /accounts/{account_id}/dlp/email/rules` — Create email scanner rule  · required: account_id  · body: action:object, conditions:object[], enabled:boolean, name:string
- `PATCH /accounts/{account_id}/dlp/email/rules` — Update email scanner rule priorities  · required: account_id  · body: new_priorities:object
- `GET /accounts/{account_id}/dlp/email/rules/{rule_id}` — Get an email scanner rule  · required: account_id, rule_id
- `PUT /accounts/{account_id}/dlp/email/rules/{rule_id}` — Update email scanner rule  · required: account_id, rule_id  · body: action:object, conditions:object[], enabled:boolean, name:string
- `DELETE /accounts/{account_id}/dlp/email/rules/{rule_id}` — Delete email scanner rule  · required: account_id, rule_id
- `GET /accounts/{account_id}/email/sending/limits` — Get sending limits  · required: account_id
- `GET /accounts/{account_id}/email/sending/messages/{message_id}` — Fetch an email message  · required: account_id, message_id
- `GET /accounts/{account_id}/email/sending/reputation` — Get account reputation  · required: account_id
- `POST /accounts/{account_id}/email/sending/send` — Send an email  · required: account_id  · body: text:any, to:any
- `POST /accounts/{account_id}/email/sending/send_raw` — Send a raw MIME email  · required: account_id  · body: from:string, mime_message:string, recipients:string[]
- `GET /accounts/{account_id}/email/sending/suppression` — List account email suppressions  · required: account_id
- `POST /accounts/{account_id}/email/sending/suppression` — Create account email suppression  · required: account_id  · body: email:string
- `GET /accounts/{account_id}/email/sending/suppression/{suppression_id}` — Get account email suppression  · required: account_id, suppression_id
- `DELETE /accounts/{account_id}/email/sending/suppression/{suppression_id}` — Delete account email suppression  · required: account_id, suppression_id
- `GET /accounts/{account_id}/email/sending/suppressions` — List account Email Sending suppressions  · required: account_id
- `POST /accounts/{account_id}/email/sending/suppressions` — Create account Email Sending suppression  · required: account_id  · body: email:string
- `POST /accounts/{account_id}/email/sending/suppressions/bulk` — Bulk import account Email Sending suppressions  · required: account_id  · body: items:object[]
- `GET /accounts/{account_id}/email/sending/suppressions/{suppression_id}` — Get account Email Sending suppression  · required: account_id, suppression_id
- `PATCH /accounts/{account_id}/email/sending/suppressions/{suppression_id}` — Update account Email Sending suppression  · required: account_id, suppression_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/email/sending/suppressions/{suppression_id}` — Delete account Email Sending suppression  · required: account_id, suppression_id
- `GET /radar/email/security/summary/arc` — Get email ARC validation summary  · required: 
- `GET /radar/email/security/summary/dkim` — Get email DKIM validation summary  · required: 
- `GET /radar/email/security/summary/dmarc` — Get email DMARC validation summary  · required: 
- `GET /radar/email/security/summary/malicious` — Get email malicious classification summary  · required: 
- `GET /radar/email/security/summary/spam` — Get email spam classification summary  · required: 
- `GET /radar/email/security/summary/spf` — Get email SPF validation summary  · required: 
- `GET /radar/email/security/summary/spoof` — Get email spoof classification summary  · required: 
- `GET /radar/email/security/summary/threat_category` — Get email threat category summary  · required: 
- `GET /radar/email/security/summary/tls_version` — Get email TLS version summary  · required: 
- `GET /radar/email/security/summary/{dimension}` — Get email security summary by dimension  · required: dimension
- `GET /radar/email/security/timeseries_groups/arc` — Get email ARC validation time series  · required: 
- `GET /radar/email/security/timeseries_groups/dkim` — Get email DKIM validation time series  · required: 
- `GET /radar/email/security/timeseries_groups/dmarc` — Get email DMARC validation time series  · required: 
- `GET /radar/email/security/timeseries_groups/malicious` — Get email malicious classification time series  · required: 
- `GET /radar/email/security/timeseries_groups/spam` — Get email spam classification time series  · required: 
- `GET /radar/email/security/timeseries_groups/spf` — Get email SPF validation time series  · required: 
- `GET /radar/email/security/timeseries_groups/spoof` — Get email spoof classification time series  · required: 
- `GET /radar/email/security/timeseries_groups/threat_category` — Get email threat category time series  · required: 
- `GET /radar/email/security/timeseries_groups/tls_version` — Get email TLS version time series  · required: 
- `GET /radar/email/security/timeseries_groups/{dimension}` — Get email security time series grouped by dimension  · required: dimension
- `GET /radar/email/security/top/tlds` — Get top TLDs by email message volume  · required: 
- `GET /radar/email/security/top/tlds/malicious/{malicious}` — Get top TLDs by email malicious classification  · required: malicious
- `GET /radar/email/security/top/tlds/spam/{spam}` — Get top TLDs by email spam classification  · required: spam
- `GET /radar/email/security/top/tlds/spoof/{spoof}` — Get top TLDs by email spoof classification  · required: spoof
- `GET /zones/{zone_id}/email/auth/dmarc-reports` — Get DMARC Report Status  · required: 
- `PATCH /zones/{zone_id}/email/auth/dmarc-reports` — Configure DMARC Reports  · required:   · body: (no required fields)
- `GET /zones/{zone_id}/email/auth/spf/inspect` — Inspect SPF Record  · required: 
- `GET /zones/{zone_id}/email/sending/subdomains` — List sending subdomains  · required: zone_id
- `POST /zones/{zone_id}/email/sending/subdomains` — Create a sending subdomain  · required: zone_id  · body: name:string
- `POST /zones/{zone_id}/email/sending/subdomains/preview` — Preview sending subdomain DNS  · required: zone_id  · body: name:string
- `GET /zones/{zone_id}/email/sending/subdomains/{subdomain_id}` — Get a sending subdomain  · required: subdomain_id, zone_id
- `PATCH /zones/{zone_id}/email/sending/subdomains/{subdomain_id}` — Update a sending subdomain  · required: subdomain_id, zone_id  · body: preview_enabled:any
- `DELETE /zones/{zone_id}/email/sending/subdomains/{subdomain_id}` — Delete a sending subdomain  · required: subdomain_id, zone_id
- `GET /zones/{zone_id}/email/sending/subdomains/{subdomain_id}/dns` — Get sending subdomain DNS records  · required: subdomain_id, zone_id
- `POST /zones/{zone_id}/email/sending/subdomains/{subdomain_id}/dns` — Fix sending subdomain DNS records  · required: subdomain_id, zone_id
- `GET /zones/{zone_id}/email/sending/subdomains/{subdomain_id}/dns/status` — Get sending subdomain DNS status  · required: subdomain_id, zone_id
- `GET /zones/{zone_id}/email/sending/subdomains/{subdomain_id}/reputation/complaints` — Get sending subdomain complaint count  · required: subdomain_id, zone_id, start_at, end_at
- `GET /zones/{zone_id}/email/sending/suppression` — List zone email suppressions  · required: zone_id
- `POST /zones/{zone_id}/email/sending/suppression` — Create zone email suppression  · required: zone_id  · body: email:string
- `GET /zones/{zone_id}/email/sending/suppression/{suppression_id}` — Get zone email suppression  · required: zone_id, suppression_id
- `DELETE /zones/{zone_id}/email/sending/suppression/{suppression_id}` — Delete zone email suppression  · required: zone_id, suppression_id
