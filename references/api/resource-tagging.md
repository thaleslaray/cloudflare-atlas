# API reference — resource-tagging

> Exact REST endpoints for **resource-tagging**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 54 operations. Base: `https://api.cloudflare.com/client/v4`.

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
- `GET /accounts/{account_id}/magic/cloud/resources` — List Resources  · required: account_id
- `GET /accounts/{account_id}/magic/cloud/resources/export` — Export Resources  · required: account_id
- `POST /accounts/{account_id}/magic/cloud/resources/policy-preview` — Preview Rego Query  · required: account_id  · body: policy:string
- `GET /accounts/{account_id}/magic/cloud/resources/{resource_id}` — Read Resource  · required: account_id, resource_id
- `GET /accounts/{account_id}/resource-library/applications` — List applications  · required: account_id
- `POST /accounts/{account_id}/resource-library/applications` — Create application  · required: account_id  · body: category_id:integer, human_id:string, name:string
- `GET /accounts/{account_id}/resource-library/applications/{id}` — Get application  · required: account_id, id
- `PATCH /accounts/{account_id}/resource-library/applications/{id}` — Update application  · required: account_id, id  · body: (no required fields)
- `DELETE /accounts/{account_id}/resource-library/applications/{id}` — Delete application  · required: account_id, id
- `GET /accounts/{account_id}/resource-library/categories` — List application categories  · required: account_id
- `GET /accounts/{account_id}/resource-library/categories/{id}` — Get application category  · required: account_id, id
- `GET /accounts/{account_id}/scim/v2/ResourceTypes` — List SCIM Resource Types  · required: account_id
- `GET /accounts/{account_id}/scim/v2/ResourceTypes/{resource_type_id}` — Get SCIM Resource Type  · required: account_id, resource_type_id
- `GET /accounts/{account_id}/shares` — List account shares  · required: account_id
- `POST /accounts/{account_id}/shares` — Create a new share  · required: account_id  · body: name:string, recipients:object[], resources:object[]
- `GET /accounts/{account_id}/shares/{share_id}` — Get account share by ID  · required: account_id, share_id
- `PUT /accounts/{account_id}/shares/{share_id}` — Update a share  · required: account_id, share_id  · body: name:string
- `DELETE /accounts/{account_id}/shares/{share_id}` — Delete a share  · required: account_id, share_id
- `GET /accounts/{account_id}/shares/{share_id}/excluded-recipients` — List share excluded recipients by share ID  · required: account_id, share_id
- `POST /accounts/{account_id}/shares/{share_id}/excluded-recipients` — Create a new share excluded recipient  · required: account_id, share_id  · body: account_id:object
- `PUT /accounts/{account_id}/shares/{share_id}/excluded-recipients` — Update a share's excluded recipients  · required: account_id, share_id  · body: (no required fields)
- `GET /accounts/{account_id}/shares/{share_id}/excluded-recipients/{excluded_recipient_id}` — Get share excluded recipient by ID  · required: account_id, share_id, excluded_recipient_id
- `DELETE /accounts/{account_id}/shares/{share_id}/excluded-recipients/{excluded_recipient_id}` — Delete a share excluded recipient  · required: account_id, share_id, excluded_recipient_id
- `GET /accounts/{account_id}/shares/{share_id}/recipients` — List share recipients by share ID  · required: account_id, share_id
- `POST /accounts/{account_id}/shares/{share_id}/recipients` — Create a new share recipient  · required: account_id, share_id  · body: (no required fields)
- `PUT /accounts/{account_id}/shares/{share_id}/recipients` — Update a share's recipients  · required: account_id, share_id  · body: (no required fields)
- `GET /accounts/{account_id}/shares/{share_id}/recipients/{recipient_id}` — Get share recipient by ID  · required: account_id, share_id, recipient_id
- `DELETE /accounts/{account_id}/shares/{share_id}/recipients/{recipient_id}` — Delete a share recipient  · required: account_id, share_id, recipient_id
- `GET /accounts/{account_id}/shares/{share_id}/resources` — List share resources by share ID  · required: account_id, share_id
- `POST /accounts/{account_id}/shares/{share_id}/resources` — Create a new share resource  · required: account_id, share_id  · body: meta:object, resource_account_id:string, resource_id:string, resource_type:string
- `GET /accounts/{account_id}/shares/{share_id}/resources/{share_resource_id}` — Get share resource by ID  · required: account_id, share_id, share_resource_id
- `PUT /accounts/{account_id}/shares/{share_id}/resources/{share_resource_id}` — Update a share resource  · required: account_id, share_id, share_resource_id  · body: meta:object
- `DELETE /accounts/{account_id}/shares/{share_id}/resources/{share_resource_id}` — Delete a share resource  · required: account_id, share_id, share_resource_id
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
