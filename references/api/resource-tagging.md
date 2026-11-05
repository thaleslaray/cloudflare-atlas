# API reference — resource-tagging

> Exact REST endpoints for **resource-tagging**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 51 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /accounts/{account_id}/access/tags` — List tags  · required: account_id
- `POST /accounts/{account_id}/access/tags` — Create a tag  · required: account_id  · body: (no required fields)
- `GET /accounts/{account_id}/access/tags/{tag_name}` — Get a tag  · required: account_id, tag_name
- `PUT /accounts/{account_id}/access/tags/{tag_name}` — Update a tag  · required: account_id, tag_name  · body: name:string
- `DELETE /accounts/{account_id}/access/tags/{tag_name}` — Delete a tag  · required: account_id, tag_name
- `GET /accounts/{account_id}/iam/resource_groups` — List Resource Groups  · required: account_id
- `POST /accounts/{account_id}/iam/resource_groups` — Create Resource Group  · required: account_id  · body: name:string, scope:object
- `GET /accounts/{account_id}/iam/resource_groups/{resource_group_id}` — Resource Group Details  · required: account_id, resource_group_id
- `PUT /accounts/{account_id}/iam/resource_groups/{resource_group_id}` — Update Resource Group  · required: account_id, resource_group_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/iam/resource_groups/{resource_group_id}` — Remove Resource Group  · required: account_id, resource_group_id
- `GET /accounts/{account_id}/resource-library/applications` — List applications  · required: account_id
- `POST /accounts/{account_id}/resource-library/applications` — Create application  · required: account_id  · body: hostnames:object
- `POST /accounts/{account_id}/resource-library/applications/lookup` — Look up applications in a rule sentence  · required: account_id  · body: lookup:string
- `GET /accounts/{account_id}/resource-library/applications/{id}` — Get application  · required: account_id, id
- `PATCH /accounts/{account_id}/resource-library/applications/{id}` — Update application  · required: account_id, id  · body: (no required fields)
- `DELETE /accounts/{account_id}/resource-library/applications/{id}` — Delete application  · required: account_id, id
- `GET /accounts/{account_id}/resource-library/categories` — List application categories  · required: account_id
- `GET /accounts/{account_id}/resource-library/categories/{id}` — Get application category  · required: account_id, id
- `GET /accounts/{account_id}/scim/v2/ResourceTypes` — List SCIM Resource Types  · required: account_id
- `GET /accounts/{account_id}/scim/v2/ResourceTypes/{resource_type_id}` — Get SCIM Resource Type  · required: account_id, resource_type_id
- `GET /accounts/{account_id}/shares` — List account shares  · required: account_id
- `POST /accounts/{account_id}/shares` — Trigger a share creation  · required: account_id  · body: name:string, recipients:object[], resources:object[]
- `GET /accounts/{account_id}/shares/{share_id}` — Get account share by ID  · required: account_id, share_id
- `PUT /accounts/{account_id}/shares/{share_id}` — Trigger a share rename  · required: account_id, share_id  · body: name:string
- `DELETE /accounts/{account_id}/shares/{share_id}` — Trigger a share deletion  · required: account_id, share_id
- `GET /accounts/{account_id}/shares/{share_id}/excluded-recipients` — List share excluded recipients by share ID  · required: account_id, share_id
- `POST /accounts/{account_id}/shares/{share_id}/excluded-recipients` — Trigger an account exclusion from a share  · required: account_id, share_id  · body: account_id:object
- `PUT /accounts/{account_id}/shares/{share_id}/excluded-recipients` — Trigger excluded-account reconciliation on a share  · required: account_id, share_id  · body: (no required fields)
- `GET /accounts/{account_id}/shares/{share_id}/excluded-recipients/{excluded_recipient_id}` — Get share excluded recipient by ID  · required: account_id, share_id, excluded_recipient_id
- `DELETE /accounts/{account_id}/shares/{share_id}/excluded-recipients/{excluded_recipient_id}` — Trigger an account un-exclusion from a share  · required: account_id, share_id, excluded_recipient_id
- `GET /accounts/{account_id}/shares/{share_id}/recipients` — List share recipients by share ID  · required: account_id, share_id
- `POST /accounts/{account_id}/shares/{share_id}/recipients` — Trigger a recipient addition to a share  · required: account_id, share_id  · body: (no required fields)
- `PUT /accounts/{account_id}/shares/{share_id}/recipients` — Trigger recipient reconciliation on a share  · required: account_id, share_id  · body: (no required fields)
- `GET /accounts/{account_id}/shares/{share_id}/recipients/{recipient_id}` — Get share recipient by ID  · required: account_id, share_id, recipient_id
- `DELETE /accounts/{account_id}/shares/{share_id}/recipients/{recipient_id}` — Trigger a recipient removal from a share  · required: account_id, share_id, recipient_id
- `GET /accounts/{account_id}/shares/{share_id}/resources` — List share resources by share ID  · required: account_id, share_id
- `POST /accounts/{account_id}/shares/{share_id}/resources` — Trigger a resource addition to a share  · required: account_id, share_id  · body: meta:object, resource_account_id:string, resource_id:string, resource_type:string
- `GET /accounts/{account_id}/shares/{share_id}/resources/{share_resource_id}` — Get share resource by ID  · required: account_id, share_id, share_resource_id
- `PUT /accounts/{account_id}/shares/{share_id}/resources/{share_resource_id}` — Trigger a resource metadata update in a share  · required: account_id, share_id, share_resource_id  · body: meta:object
- `DELETE /accounts/{account_id}/shares/{share_id}/resources/{share_resource_id}` — Trigger a resource deletion from a share  · required: account_id, share_id, share_resource_id
- `GET /accounts/{account_id}/tags` — Get tags for an account-level resource  · required: account_id, resource_id, resource_type
- `PUT /accounts/{account_id}/tags` — Set tags for an account-level resource  · required: account_id  · body: resource_id:string, resource_type:string, worker_id:string
- `DELETE /accounts/{account_id}/tags` — Delete tags from an account-level resource  · required: account_id  · body: resource_id:string, resource_type:string, worker_id:string
- `GET /accounts/{account_id}/tags/keys` — List tag keys  · required: account_id
- `GET /accounts/{account_id}/tags/resources` — List tagged resources  · required: account_id
- `GET /accounts/{account_id}/tags/summary` — List tag key summary  · required: account_id
- `GET /accounts/{account_id}/tags/values/{tag_key}` — List tag values  · required: account_id, tag_key
- `GET /organizations/{organization_id}/shares` — List organization shares  · required: organization_id
- `GET /zones/{zone_id}/tags` — Get tags for a zone-level resource  · required: zone_id, resource_id, resource_type
- `PUT /zones/{zone_id}/tags` — Set tags for a zone-level resource  · required: zone_id  · body: resource_id:string, resource_type:string
- `DELETE /zones/{zone_id}/tags` — Delete tags from a zone-level resource  · required: zone_id  · body: resource_id:string, resource_type:string
