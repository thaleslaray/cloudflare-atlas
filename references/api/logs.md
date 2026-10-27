# API reference — logs

> Exact REST endpoints for **logs**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 69 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /accounts/{account_id}/access/logs/access_requests` — Get Access authentication logs  · required: account_id
- `GET /accounts/{account_id}/access/logs/scim/updates` — List Access SCIM update logs  · required: account_id, idp_id
- `GET /accounts/{account_id}/logpush/datasets/{dataset_id}/fields` — List fields  · required: dataset_id, account_id
- `GET /accounts/{account_id}/logpush/datasets/{dataset_id}/jobs` — List Logpush jobs for a dataset  · required: dataset_id, account_id
- `GET /accounts/{account_id}/logpush/jobs` — List Logpush jobs  · required: account_id
- `POST /accounts/{account_id}/logpush/jobs` — Create Logpush job  · required: account_id  · body: destination_conf:string
- `GET /accounts/{account_id}/logpush/jobs/{job_id}` — Get Logpush job details  · required: job_id, account_id
- `PUT /accounts/{account_id}/logpush/jobs/{job_id}` — Update Logpush job  · required: job_id, account_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/logpush/jobs/{job_id}` — Delete Logpush job  · required: job_id, account_id
- `POST /accounts/{account_id}/logpush/ownership` — Get ownership challenge  · required: account_id  · body: destination_conf:string
- `POST /accounts/{account_id}/logpush/ownership/validate` — Validate ownership challenge  · required: account_id  · body: destination_conf:string, ownership_challenge:string
- `GET /accounts/{account_id}/logpush/transformers` — List transformers  · required: account_id
- `POST /accounts/{account_id}/logpush/transformers` — Create transformer  · required: account_id  · body: code:string, name:string
- `POST /accounts/{account_id}/logpush/transformers/preview` — Preview transformer  · required: account_id  · body: input:object, sql:string
- `GET /accounts/{account_id}/logpush/transformers/{transformer_id}` — Get transformer  · required: account_id, transformer_id
- `PUT /accounts/{account_id}/logpush/transformers/{transformer_id}` — Update transformer  · required: account_id, transformer_id  · body: name:string
- `DELETE /accounts/{account_id}/logpush/transformers/{transformer_id}` — Delete transformer  · required: account_id, transformer_id
- `GET /accounts/{account_id}/logpush/transformers/{transformer_id}/content` — Get transformer content  · required: account_id, transformer_id
- `GET /accounts/{account_id}/logpush/transformers/{transformer_id}/versions` — List transformer versions  · required: account_id, transformer_id
- `POST /accounts/{account_id}/logpush/validate/destination` — Validate destination  · required: account_id  · body: destination_conf:string
- `POST /accounts/{account_id}/logpush/validate/destination/exists` — Check destination exists  · required: account_id  · body: destination_conf:string
- `POST /accounts/{account_id}/logpush/validate/origin` — Validate origin  · required: account_id  · body: logpull_options:string
- `GET /accounts/{account_id}/logs/audit` — Get account audit logs (Version 2)  · required: account_id, since, before
- `GET /accounts/{account_id}/logs/audit/product_categories` — List account audit log product categories (Version 2)  · required: account_id
- `GET /accounts/{account_id}/logs/audit/{id}/history` — Get resource change history from an account audit log entry (Version 2)  · required: account_id, id, action_time, since, before
- `GET /accounts/{account_id}/logs/control/cmb/config` — Get CMB config  · required: account_id
- `POST /accounts/{account_id}/logs/control/cmb/config` — Update CMB config  · required: account_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/logs/control/cmb/config` — Delete CMB config  · required: account_id
- `GET /accounts/{account_id}/logs/explorer/datasets` — List account datasets  · required: 
- `POST /accounts/{account_id}/logs/explorer/datasets` — Create an account dataset  · required:   · body: dataset:string
- `GET /accounts/{account_id}/logs/explorer/datasets/available` — List available account datasets  · required: 
- `GET /accounts/{account_id}/logs/explorer/datasets/{dataset_id}` — Get an account dataset  · required: 
- `PUT /accounts/{account_id}/logs/explorer/datasets/{dataset_id}` — Update an account dataset  · required:   · body: enabled:boolean
- `DELETE /accounts/{account_id}/logs/explorer/datasets/{dataset_id}` — Delete an account dataset  · required: 
- `GET /accounts/{account_id}/logs/explorer/query/sql` — Run a log query  · required: query
- `POST /accounts/{account_id}/logs/explorer/query/sql` — Run a log query  · required:   · body: (no required fields)
- `GET /accounts/{account_id}/logs/list` — List log files  · required: 
- `GET /accounts/{account_id}/logs/retrieve` — Retrieve logs  · required: 
- `GET /organizations/{organization_id}/logs/audit` — Get organization audit logs (Version 2)  · required: organization_id, since, before
- `GET /organizations/{organization_id}/logs/audit/{id}/history` — Get resource change history from an organization audit log entry (Version 2)  · required: organization_id, id, action_time, since, before
- `GET /radar/ct/logs` — List certificate logs  · required: 
- `GET /radar/ct/logs/{log_slug}` — Get certificate log details  · required: log_slug
- `GET /zones/{zone_id}/logpush/datasets/{dataset_id}/fields` — List fields  · required: dataset_id, zone_id
- `GET /zones/{zone_id}/logpush/datasets/{dataset_id}/jobs` — List Logpush jobs for a dataset  · required: dataset_id, zone_id
- `GET /zones/{zone_id}/logpush/edge/jobs` — List Instant Logs jobs  · required: zone_id
- `POST /zones/{zone_id}/logpush/edge/jobs` — Create Instant Logs job  · required: zone_id  · body: (no required fields)
- `GET /zones/{zone_id}/logpush/jobs` — List Logpush jobs  · required: zone_id
- `POST /zones/{zone_id}/logpush/jobs` — Create Logpush job  · required: zone_id  · body: destination_conf:string
- `GET /zones/{zone_id}/logpush/jobs/{job_id}` — Get Logpush job details  · required: job_id, zone_id
- `PUT /zones/{zone_id}/logpush/jobs/{job_id}` — Update Logpush job  · required: job_id, zone_id  · body: (no required fields)
- `DELETE /zones/{zone_id}/logpush/jobs/{job_id}` — Delete Logpush job  · required: job_id, zone_id
- `POST /zones/{zone_id}/logpush/ownership` — Get ownership challenge  · required: zone_id  · body: destination_conf:string
- `POST /zones/{zone_id}/logpush/ownership/validate` — Validate ownership challenge  · required: zone_id  · body: destination_conf:string, ownership_challenge:string
- `POST /zones/{zone_id}/logpush/validate/destination` — Validate destination  · required: zone_id  · body: destination_conf:string
- `POST /zones/{zone_id}/logpush/validate/destination/exists` — Check destination exists  · required: zone_id  · body: destination_conf:string
- `POST /zones/{zone_id}/logpush/validate/origin` — Validate origin  · required: zone_id  · body: logpull_options:string
- `GET /zones/{zone_id}/logs/control/retention/flag` — Get log retention flag  · required: zone_id
- `POST /zones/{zone_id}/logs/control/retention/flag` — Update log retention flag  · required: zone_id  · body: (no required fields)
- `GET /zones/{zone_id}/logs/explorer/datasets` — List zone datasets  · required: 
- `POST /zones/{zone_id}/logs/explorer/datasets` — Create a zone dataset  · required:   · body: dataset:string
- `GET /zones/{zone_id}/logs/explorer/datasets/available` — List available zone datasets  · required: 
- `GET /zones/{zone_id}/logs/explorer/datasets/{dataset_id}` — Get a zone dataset  · required: 
- `PUT /zones/{zone_id}/logs/explorer/datasets/{dataset_id}` — Update a zone dataset  · required:   · body: enabled:boolean
- `DELETE /zones/{zone_id}/logs/explorer/datasets/{dataset_id}` — Delete a zone dataset  · required: 
- `GET /zones/{zone_id}/logs/explorer/query/sql` — Run a log query  · required: query
- `POST /zones/{zone_id}/logs/explorer/query/sql` — Run a log query  · required:   · body: (no required fields)
- `GET /zones/{zone_id}/logs/rayids/{ray_id}` — Get logs RayIDs  · required: zone_id, ray_id
- `GET /zones/{zone_id}/logs/received` — Get logs received  · required: zone_id, end
- `GET /zones/{zone_id}/logs/received/fields` — List fields  · required: zone_id
